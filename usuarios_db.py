import sqlite3
import hashlib
import os

from planilhas_paths import ensure_from_resource, is_frozen, log_desktop

# ==============================
# BANCO DE DADOS DE USUÁRIOS
# ==============================

def inicializar_banco_usuarios():
    """Cria o banco de dados de usuários se não existir"""
    if is_frozen():
        db_path = ensure_from_resource("usuarios.db")
    else:
        # Em dev, manter o DB ao lado do codigo para nao variar por CWD.
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.db")

    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    except Exception:
        pass

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        nivel_acesso TEXT DEFAULT 'usuario',
        data_cadastro TEXT NOT NULL,
        ativo INTEGER DEFAULT 1
    )
    """)
    
    conn.commit()
    return conn, cursor

def hash_senha(senha):
    """Cria hash da senha usando SHA-256"""
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha_digitada, senha_hash):
    """Verifica se a senha digitada corresponde ao hash"""
    return hash_senha(senha_digitada) == senha_hash

def criar_usuario(nome, email, senha, nivel_acesso='usuario'):
    """Cria um novo usuário"""
    conn, cursor = inicializar_banco_usuarios()
    
    try:
        senha_hash = hash_senha(senha)
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
        INSERT INTO usuarios (nome, email, senha, nivel_acesso, data_cadastro)
        VALUES (?, ?, ?, ?, ?)
        """, (nome, email, senha_hash, nivel_acesso, data_cadastro))
        
        conn.commit()
        return True, "Usuário criado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Este email já está cadastrado!"
    except Exception as e:
        return False, f"Erro ao criar usuário: {str(e)}"
    finally:
        conn.close()

def autenticar_usuario(email, senha):
    """Autentica usuário"""
    conn, cursor = inicializar_banco_usuarios()
    
    try:
        senha_hash = hash_senha(senha)
        
        cursor.execute("""
        SELECT id, nome, email, nivel_acesso, ativo 
        FROM usuarios 
        WHERE email = ? AND senha = ?
        """, (email, senha_hash))
        
        usuario = cursor.fetchone()
        
        if usuario and usuario[4] == 1:  # ativo = 1
            return {
                'id': usuario[0],
                'nome': usuario[1], 
                'email': usuario[2],
                'nivel_acesso': usuario[3]
            }
        elif usuario and usuario[4] == 0:
            return None  # Usuário inativo
        else:
            return None  # Credenciais inválidas
            
    except Exception as e:
        print(f"Erro na autenticação: {str(e)}")
        return None
    finally:
        conn.close()

def criar_admin_default():
    """Cria usuário admin padrão se não existir"""
    conn, cursor = inicializar_banco_usuarios()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = 'admin@planilhas.com'")
        if cursor.fetchone()[0] == 0:
            criar_usuario("Administrador", "admin@planilhas.com", "admin123", "admin")
            print("Usuário admin criado: admin@planilhas.com / admin123")
    except Exception as e:
        print(f"Erro ao criar admin: {str(e)}")
    finally:
        conn.close()

def ensure_inicializado():
    """Inicializa banco e admin default sem derrubar o exe."""
    try:
        inicializar_banco_usuarios()
        criar_admin_default()
    except Exception as e:
        log_desktop(f"[ERRO] Falha ao inicializar usuarios.db: {repr(e)}")


# Import necessario para datetime (mantido no fim como estava)
from datetime import datetime
