import os
import sys
from pathlib import Path
import shutil

# Copiar arquivo batch para Desktop
desktop_path = str(Path.home() / "Desktop")
bat_file = os.path.join(os.getcwd(), "Planilhas.bat")
desktop_bat = os.path.join(desktop_path, "Planilhas.bat")

if os.path.exists(bat_file):
    shutil.copy2(bat_file, desktop_bat)
    print(f"✓ Arquivo copiado para Desktop: {desktop_bat}")
    print("✓ Pronto! Você pode executar 'Planilhas.bat' do Desktop")
else:
    print("✗ Arquivo Planilhas.bat não encontrado")
