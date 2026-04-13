import os
import subprocess
import sys


def build_executable_light():
    """
    Build em modo leve (--onedir), util para maquinas com pouca memoria.
    """
    print("Gerando executavel em modo leve...")

    hidden_imports = [
        "sistema",
        "sistema_plus",
        "menu_principal",
        "usuarios_db",
        "gerenciamento_usuarios",
        "sistema_online_offline",
        "banco_offline",
        "flask",
        "werkzeug",
        "click",
        "jinja2",
        "openpyxl",
    ]

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onedir",
        "--windowed",
        "--name=Planilhas",
        "--add-data=templates;templates",
        "--add-data=static;static",
        "--add-data=banco_plus.db;.",
        "--add-data=banco.db;.",
        "--add-data=usuarios.db;.",
        "--collect-all=flask",
        "--collect-all=werkzeug",
        "--collect-all=jinja2",
        "--collect-all=openpyxl",
        "--noupx",
        "--distpath=dist",
        "--buildpath=build",
        "--specpath=.",
        "--noconfirm",
        "--clean",
    ]

    for hidden_import in hidden_imports:
        cmd.extend(["--hidden-import", hidden_import])

    if os.path.exists("icon.ico"):
        cmd.extend(["--icon", "icon.ico"])

    cmd.append("app.py")

    try:
        subprocess.run(cmd, check=True)
        exe_path = os.path.join("dist", "Planilhas", "Planilhas.exe")
        if os.path.exists(exe_path):
            print(f"Executavel gerado: {exe_path}")
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False


if __name__ == "__main__":
    build_executable_light()
    input("Pressione Enter...")
