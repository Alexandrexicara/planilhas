import subprocess
import sys
import os

def build_executable():
    """Gera o executável Windows do sistema"""
    print("🚀 Gerando executável Windows...")
    
    # Comando pyinstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',           # Gera um único arquivo
        '--windowed',          # Sem console
        '--name=SistemaPlanilhas',  # Nome do executável
        '--icon=icon.ico' if os.path.exists('icon.ico') else '',  # Ícone se existir
        '--add-data=planilhas;planilhas',  # Inclui pasta planilhas se existir
        'sistema.py'
    ]
    
    # Remove ícone se não existir
    if not os.path.exists('icon.ico'):
        cmd.remove('--icon=icon.ico')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Executável gerado com sucesso!")
        print(f"📁 Local: dist/SistemaPlanilhas.exe")
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
