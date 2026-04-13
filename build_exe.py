import subprocess
import sys
import os
import shutil
from pathlib import Path

def get_desktop_path():
    """Retorna o caminho da área de trabalho"""
    desktop = Path.home() / "Desktop"
    return str(desktop)

def build_executable():
    """Gera o executável Windows do sistema"""
    print("🚀 Gerando executável Windows...")
    
    # Comando pyinstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',           # Gera um único arquivo
        '--windowed',          # Sem console
        '--name=SistemaPlanilhas',  # Nome do executável
        'app.py'
    ]
    
    # Adiciona ícone se existir
    if os.path.exists('icon.ico'):
        cmd.insert(-1, '--icon=icon.ico')
        print("🎨 Usando ícone personalizado...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Executável gerado com sucesso!")
        
        # Copia para Desktop
        exe_path = "dist/SistemaPlanilhas.exe"
        desktop_path = get_desktop_path()
        desktop_exe = os.path.join(desktop_path, "SistemaPlanilhas.exe")
        
        if os.path.exists(exe_path):
            shutil.copy2(exe_path, desktop_exe)
            print(f"📁 Copiado para Desktop: {desktop_exe}")
            print(f"🎯 Acesse o atalho na área de trabalho!")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar executável: {e}")
        print(f"Saída: {e.stdout}")
        print(f"Erro: {e.stderr}")
        return False

if __name__ == "__main__":
    # Verifica se pyinstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Gera o executável
    build_executable()
    
    input("\nPressione Enter para sair...")
