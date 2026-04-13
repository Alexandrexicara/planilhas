#!/usr/bin/env python3
import os, shutil, sys, ctypes, subprocess, json, tempfile
from pathlib import Path

install_dir = Path.home() / "AppData/Local/Programs/Planilhas"
source_dir = Path(__file__).parent

print("📦 Instalador do Planilhas\n")

try:
    print("📂 Criando pasta de instalacao...")
    # Matar processos abertos
    subprocess.run(["taskkill", "/F", "/IM", "Planilhas.exe"], capture_output=True)
    subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
    
    if install_dir.exists():
        import time; time.sleep(1)  # Espera libertar arquivos
        shutil.rmtree(install_dir, ignore_errors=True)
    install_dir.mkdir(parents=True, exist_ok=True)
    
    print("📁 Copiando arquivos...")
    for item in source_dir.iterdir():
        if item.name.startswith("Instalar") or item.name == "__pycache__":
            continue
        if item.is_file():
            shutil.copy2(item, install_dir)
        elif item.is_dir():
            shutil.copytree(item, install_dir / item.name, dirs_exist_ok=True)
    
    print("🔗 Criando atalhos...")
    exe_path = install_dir / "Planilhas.exe"
    icon_path = install_dir / "icon.ico"
    
    # Desktop
    desktop = Path.home() / "Desktop"
    link_path = desktop / "Planilhas.lnk"
    
    # Start Menu
    start_menu = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Planilhas"
    start_menu.mkdir(parents=True, exist_ok=True)
    link_menu = start_menu / "Planilhas.lnk"
    
    # Criar atalhos com VBScript
    for link_file in [link_path, link_menu]:
        if link_file.exists():
            link_file.unlink()
        
        vbs_content = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{str(link_file).replace(chr(92), chr(92)*2)}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{str(exe_path).replace(chr(92), chr(92)*2)}"
oLink.WorkingDirectory = "{str(install_dir).replace(chr(92), chr(92)*2)}"
oLink.IconLocation = "{str(icon_path).replace(chr(92), chr(92)*2)}"
oLink.Save()
'''
        
        vbs_file = tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False)
        vbs_file.write(vbs_content)
        vbs_file.close()
        
        try:
            subprocess.run(["cscript.exe", vbs_file.name], capture_output=True, timeout=5)
        finally:
            Path(vbs_file.name).unlink()
    
    print("✅ Instalacao concluida!")
    print(f"📍 Local: {install_dir}")
    print(f"🚀 Iniciando aplicacao...\n")
    
    subprocess.Popen([str(exe_path)], cwd=str(install_dir))
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
    input("Pressione ENTER para sair...")
