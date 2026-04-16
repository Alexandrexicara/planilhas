import os
import sqlite3
import secrets
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from planilhas_paths import ensure_from_resource


DB_FILENAME = "acesso_web.db"


def _utcnow_str():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def get_db_path():
    return ensure_from_resource(DB_FILENAME)


def connect():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            created_at TEXT NOT NULL,

            payment_status TEXT NOT NULL DEFAULT 'unpaid', -- unpaid | pending | paid
            payment_amount REAL NOT NULL DEFAULT 4500.00,
            payment_txid TEXT,
            payment_qr_base64 TEXT,
            payment_pix_key TEXT,
            payment_updated_at TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'collab', -- superadmin | owner | admin | collab
            ativo INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            FOREIGN KEY (organization_id) REFERENCES organizations (id)
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS invites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization_id INTEGER NOT NULL,
            code TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL DEFAULT 'collab',
            email TEXT,
            created_at TEXT NOT NULL,
            used_at TEXT,
            used_by_user_id INTEGER,
            FOREIGN KEY (organization_id) REFERENCES organizations (id),
            FOREIGN KEY (used_by_user_id) REFERENCES users (id)
        )
        """
    )

    conn.commit()
    conn.close()


def any_organization_exists():
    conn = connect()
    try:
        row = conn.execute("SELECT 1 FROM organizations LIMIT 1").fetchone()
        return bool(row)
    finally:
        conn.close()


def create_organization(nome, payment_amount=4500.00):
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO organizations (nome, created_at, payment_status, payment_amount)
            VALUES (?, ?, 'unpaid', ?)
            """,
            (nome.strip(), _utcnow_str(), float(payment_amount)),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def create_user(organization_id, nome, email, senha, role="collab", ativo=1):
    conn = connect()
    try:
        password_hash = generate_password_hash(senha)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (organization_id, nome, email, password_hash, role, ativo, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                organization_id,
                nome.strip(),
                email.strip().lower(),
                password_hash,
                role,
                int(ativo),
                _utcnow_str(),
            ),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def ensure_superadmin(email, senha):
    if not email or not senha:
        return None

    email_norm = email.strip().lower()
    conn = connect()
    try:
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email_norm,)).fetchone()
        password_hash = generate_password_hash(senha)
        if existing:
            conn.execute(
                """
                UPDATE users
                SET password_hash = ?, role = 'superadmin', ativo = 1
                WHERE id = ?
                """,
                (password_hash, existing["id"]),
            )
            conn.commit()
            return existing["id"]

        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (organization_id, nome, email, password_hash, role, ativo, created_at)
            VALUES (NULL, 'Criador', ?, ?, 'superadmin', 1, ?)
            """,
            (email_norm, password_hash, _utcnow_str()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def authenticate(email, senha):
    if not email or not senha:
        return None

    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT id, organization_id, nome, email, password_hash, role, ativo
            FROM users
            WHERE email = ?
            """,
            (email.strip().lower(),),
        ).fetchone()

        if not row or int(row["ativo"]) != 1:
            return None

        if not check_password_hash(row["password_hash"], senha):
            return None

        return {
            "id": row["id"],
            "organization_id": row["organization_id"],
            "nome": row["nome"],
            "email": row["email"],
            "role": row["role"],
        }
    finally:
        conn.close()


def get_user(user_id):
    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT id, organization_id, nome, email, role, ativo
            FROM users
            WHERE id = ?
            """,
            (int(user_id),),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_organization(org_id):
    if org_id is None:
        return None

    conn = connect()
    try:
        row = conn.execute(
            """
            SELECT id, nome, payment_status, payment_amount, payment_txid,
                   payment_qr_base64, payment_pix_key, payment_updated_at
            FROM organizations
            WHERE id = ?
            """,
            (int(org_id),),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def organization_has_access(org_id):
    org = get_organization(org_id)
    if not org:
        return False
    return org.get("payment_status") == "paid"


def set_organization_payment_pending(org_id, txid, qr_base64=None, pix_key=None):
    conn = connect()
    try:
        conn.execute(
            """
            UPDATE organizations
            SET payment_status = 'pending',
                payment_txid = ?,
                payment_qr_base64 = ?,
                payment_pix_key = ?,
                payment_updated_at = ?
            WHERE id = ?
            """,
            (txid, qr_base64, pix_key, _utcnow_str(), int(org_id)),
        )
        conn.commit()
    finally:
        conn.close()


def set_organization_paid(org_id):
    conn = connect()
    try:
        conn.execute(
            """
            UPDATE organizations
            SET payment_status = 'paid',
                payment_updated_at = ?
            WHERE id = ?
            """,
            (_utcnow_str(), int(org_id)),
        )
        conn.commit()
    finally:
        conn.close()


def create_invite(organization_id, role="collab", email=None):
    code = secrets.token_urlsafe(10).replace("-", "").replace("_", "")
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO invites (organization_id, code, role, email, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(organization_id),
                code,
                role,
                email.strip().lower() if email else None,
                _utcnow_str(),
            ),
        )
        conn.commit()
        return code
    finally:
        conn.close()


def redeem_invite(code, nome, email, senha):
    if not code:
        return False, "Código de convite obrigatório", None

    code_norm = code.strip()
    email_norm = (email or "").strip().lower()
    conn = connect()
    try:
        invite = conn.execute(
            """
            SELECT id, organization_id, role, email, used_at
            FROM invites
            WHERE code = ?
            """,
            (code_norm,),
        ).fetchone()

        if not invite:
            return False, "Convite inválido", None
        if invite["used_at"]:
            return False, "Convite já utilizado", None
        if invite["email"] and invite["email"] != email_norm:
            return False, "Este convite é para outro email", None

        user_id = create_user(invite["organization_id"], nome, email_norm, senha, role=invite["role"])
        conn.execute(
            """
            UPDATE invites
            SET used_at = ?, used_by_user_id = ?
            WHERE id = ?
            """,
            (_utcnow_str(), int(user_id), int(invite["id"])),
        )
        conn.commit()
        return True, "Cadastro realizado", user_id
    except sqlite3.IntegrityError:
        return False, "Este email já está cadastrado", None
    finally:
        conn.close()


def list_invites(organization_id, limit=50):
    conn = connect()
    try:
        rows = conn.execute(
            """
            SELECT id, code, role, email, created_at, used_at, used_by_user_id
            FROM invites
            WHERE organization_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(organization_id), int(limit)),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def list_users(organization_id, limit=200):
    conn = connect()
    try:
        rows = conn.execute(
            """
            SELECT id, nome, email, role, ativo, created_at
            FROM users
            WHERE organization_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (int(organization_id), int(limit)),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

