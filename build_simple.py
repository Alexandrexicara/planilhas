import subprocess
import sys
import os
from pathlib import Path

# Instalar PyInstaller se necessário
try:
    import PyInstaller
except ImportError:
    print("Instalando PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

print("Gerando executável...")

desktop_path = str(Path.home() / "Desktop")

# Comando do PyInstaller - versão simples e rápida
cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--onefile",
    "--windowed",
    "--name=Planilhas",
    "--distpath=dist",
    "--specpath=.",
    "--noconfirm",
    "--noupx",
    "menu_principal.py"
]

result = subprocess.run(cmd, capture_output=True, text=True)

if result.returncode == 0:
    print("✓ Executável gerado com sucesso!")
    
    # Copiar para Desktop
    exe_path = os.path.join("dist", "Planilhas.exe")
    if os.path.exists(exe_path):
        import shutil
        desktop_exe = os.path.join(desktop_path, "Planilhas.exe")
        shutil.copy2(exe_path, desktop_exe)
        print(f"✓ Copiado para Desktop: {desktop_exe}")
else:
    print("✗ Erro ao gerar executável:")
    print(result.stderr)
