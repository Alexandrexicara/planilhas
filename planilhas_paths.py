import os
import sys
import shutil
from pathlib import Path
from datetime import datetime


APP_ID = "planilhas.com"


def is_frozen():
    """True quando rodando empacotado (PyInstaller)."""
    return bool(getattr(sys, "frozen", False))


def resource_base_dir():
    """Base somente-leitura para arquivos empacotados (templates/db/etc)."""
    if is_frozen() and hasattr(sys, "_MEIPASS"):
        return getattr(sys, "_MEIPASS")
    return os.path.dirname(os.path.abspath(__file__))


def user_data_dir(app_id=APP_ID):
    """Diretorio gravavel pelo usuario (evita Program Files).

    Em alguns ambientes (sandbox/restricoes), LOCALAPPDATA pode falhar; neste caso,
    faz fallback para TEMP ou para um diretorio local gravavel.
    """
    candidates = []
    for env in ("LOCALAPPDATA", "APPDATA", "USERPROFILE", "TEMP", "TMP"):
        val = os.environ.get(env)
        if val:
            candidates.append(os.path.join(val, app_id))

    # Home como fallback adicional
    candidates.append(os.path.join(str(Path.home()), app_id))
    # Fallback final: um diretorio local perto do app (pode falhar em Program Files).
    candidates.append(os.path.join(os.getcwd(), f"{app_id}_data"))

    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            # Smoke-test de escrita para evitar "pasta existe mas nao grava".
            probe = os.path.join(path, "._write_probe")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            try:
                os.remove(probe)
            except Exception:
                pass
            return path
        except Exception:
            continue

    # Ultimo recurso
    return os.path.join(os.getcwd(), f"{app_id}_data")


def runtime_dir():
    """Diretorio onde o app deve gravar DB/config/logs/exportacoes."""
    override = os.environ.get("PLANILHAS_DATA_DIR")
    if override:
        os.makedirs(override, exist_ok=True)
        return override
    return user_data_dir() if is_frozen() else resource_base_dir()


def resource_path(*parts):
    return os.path.join(resource_base_dir(), *parts)


def data_path(*parts):
    return os.path.join(runtime_dir(), *parts)


def ensure_from_resource(filename):
    """Garante que um arquivo exista em data_dir, copiando do bundle se possivel."""
    dst = data_path(filename)
    if os.path.exists(dst):
        return dst

    src = resource_path(filename)
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    except Exception:
        # Melhor esforço: nao falhar por causa de copy
        pass
    return dst


def log_desktop(msg, logfile="planilhas_desktop.log"):
    """Log para diagnostico quando o exe roda sem console."""
    try:
        log_dir = os.path.join(user_data_dir(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, logfile)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {msg}\n")
    except Exception:
        pass
