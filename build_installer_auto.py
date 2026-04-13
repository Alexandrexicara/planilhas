import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

print("=" * 60)
print("🚀 COMPILADOR AUTOMÁTICO DE INSTALADOR")
print("=" * 60)

# Caminho do Inno Setup
inno_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

# 1. Verificar se Inno Setup já está instalado
print("\n[1/3] Verificando Inno Setup...")
if os.path.exists(inno_path):
    print(f"✓ Inno Setup encontrado em: {inno_path}")
else:
    print("✗ Inno Setup não encontrado!")
    print("Procurando em locais alternativos...")
    
    # Procurar em locais comuns
    alt_paths = [
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    ]
    
    inno_found = False
    for alt_path in alt_paths:
        if os.path.exists(alt_path):
            inno_path = alt_path
            print(f"✓ Inno Setup encontrado em: {inno_path}")
            inno_found = True
            break
    
    if not inno_found:
        print("✗ Inno Setup não está instalado!")
        print("\n⚠️  Por favor, instale o Inno Setup manualmente de:")
        print("   https://jrsoftware.org/isinfo.php")
        sys.exit(1)

# 2. Compilar o instalador
print("\n[2/3] Compilando instalador...")
setup_file = "setup.iss"

if not os.path.exists(setup_file):
    print(f"✗ Arquivo {setup_file} não encontrado!")
    sys.exit(1)

try:
    cmd = [inno_path, setup_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Instalador compilado com sucesso!")
    else:
        print(f"✗ Erro na compilação: {result.stderr}")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Erro ao executar compilador: {e}")
    sys.exit(1)

# 3. Verificar se o arquivo foi criado
print("\n[3/3] Verificando resultado...")
output_dir = "dist\\instalador"
installer_path = os.path.join(output_dir, "Planilhas_Setup.exe")

if os.path.exists(installer_path):
    file_size = os.path.getsize(installer_path)
    file_size_mb = file_size / (1024 * 1024)
    print(f"✓ Instalador gerado com sucesso!")
    print(f"  Arquivo: {installer_path}")
    print(f"  Tamanho: {file_size_mb:.2f} MB")
    
    # Copiar para Desktop também
    desktop_path = str(Path.home() / "Desktop" / "Planilhas_Setup.exe")
    import shutil
    shutil.copy2(installer_path, desktop_path)
    print(f"✓ Copiado para Desktop: {desktop_path}")
    
    print("\n" + "=" * 60)
    print("🎉 PRONTO!")
    print("=" * 60)
    print(f"\nSeu instalador está em:")
    print(f"  {installer_path}")
    print(f"\nOu no Desktop para fácil acesso!")
    print("\nAgora é só compartilhar e instalar em outros PCs!")
    
else:
    print(f"✗ Instalador não foi criado em: {installer_path}")
    sys.exit(1)
