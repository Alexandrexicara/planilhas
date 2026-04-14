#!/usr/bin/env python3
"""
Instalador Profissional - Planilhas.com
Copia para Program Files, cria atalhos, etc.
"""
import os
import sys
import shutil
import subprocess
import json
from pathlib import Path
from winreg import CreateKey, SetValueEx, REG_SZ, HKEY_LOCAL_MACHINE

def criar_atalho_vbs(target_exe, link_path, icon_path=None):
    """Cria atalho .lnk usando VBScript"""
    vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
Set oLink = oWS.CreateShortcut("{link_path}")
oLink.TargetPath = "{target_exe}"
oLink.WorkingDirectory = "{os.path.dirname(target_exe)}"
oLink.Description = "Planilhas - Importação Automática de Excel"
oLink.WindowStyle = 1
'''
    if icon_path and os.path.exists(icon_path):
        vbs_script += f'oLink.IconLocation = "{icon_path}"\n'
    
    vbs_script += 'oLink.Save\n'
    
    # Salvar e executar VBS
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
        f.write(vbs_script)
        vbs_path = f.name
    
    try:
        subprocess.run(['cscript.exe', vbs_path], capture_output=True, timeout=5)
    finally:
        os.unlink(vbs_path)

def main():
    print("\n" + "="*60)
    print("  🚀 INSTALADOR PLANILHAS v1.0")
    print("="*60 + "\n")
    
    # Caminhos
    app_dir = Path(__file__).parent
    install_dir = Path.home() / "AppData" / "Local" / "Planilhas"
    
    print(f"📦 Instalando em: {install_dir}")
    print(f"📁 Origem: {app_dir}\n")
    
    try:
        # ETAPA 1: Limpar e criar pasta
        print("1️⃣  Preparando pasta de instalação...")
        if install_dir.exists():
            shutil.rmtree(install_dir, ignore_errors=True)
        install_dir.mkdir(parents=True, exist_ok=True)
        
        # ETAPA 2: Copiar arquivos
        print("2️⃣  Copiando arquivos...")
        
        files_to_copy = [
            'Planilhas.exe',
            'icon.ico',
            'app.py',
            'launcher.py',
            'banco.db',
            'banco_plus.db',
            'usuarios.db',
            'config_sistema.json',
        ]
        
        for file in files_to_copy:
            src = app_dir / file
            if src.exists():
                shutil.copy2(src, install_dir / file)
                print(f"   ✓ {file}")
        
        # ETAPA 3: Copiar pastas
        print("3️⃣  Copiando recursos...")
        
        dirs_to_copy = ['templates', 'static']
        for dir_name in dirs_to_copy:
            src_dir = app_dir / dir_name
            if src_dir.exists():
                shutil.copytree(src_dir, install_dir / dir_name, dirs_exist_ok=True)
                print(f"   ✓ {dir_name}/")
        
        # ETAPA 4: Criar atalhos
        print("4️⃣  Criando atalhos...")
        
        desktop = Path.home() / "Desktop"
        start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Planilhas"
        start_menu.mkdir(parents=True, exist_ok=True)
        
        exe_path = str(install_dir / "Planilhas.exe")
        icon_path = str(install_dir / "icon.ico")
        
        # Atalho Desktop
        criar_atalho_vbs(exe_path, str(desktop / "Planilhas.lnk"), icon_path)
        print("   ✓ Atalho na área de trabalho")
        
        # Atalho Start Menu
        criar_atalho_vbs(exe_path, str(start_menu / "Planilhas.lnk"), icon_path)
        print("   ✓ Atalho no Menu Iniciar")
        
        # ETAPA 5: Registrar no Painel de Controle (opcional)
        print("5️⃣  Registrando aplicação...")
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Planilhas"
            key = CreateKey(HKEY_LOCAL_MACHINE, reg_path)
            SetValueEx(key, "DisplayName", 0, REG_SZ, "Planilhas")
            SetValueEx(key, "DisplayVersion", 0, REG_SZ, "1.0.0")
            SetValueEx(key, "InstallLocation", 0, REG_SZ, str(install_dir))
            SetValueEx(key, "Publisher", 0, REG_SZ, "planilhas.com")
            print("   ✓ Registrado no sistema")
        except Exception as e:
            print(f"   ⚠ Aviso: {e}")
        
        # ETAPA 6: Abrir aplicação
        print("\n6️⃣  Iniciando aplicação...")
        subprocess.Popen([exe_path], cwd=str(install_dir))
        
        print("\n" + "="*60)
        print("  ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*60)
        print(f"\n📍 Localização: {install_dir}")
        print(f"🖥  Atalho criado na área de trabalho")
        print(f"📋 Menu Iniciar -> Programas -> Planilhas")
        print("\n💡 A aplicação está abrindo...\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione ENTER para sair...")
        return 1

if __name__ == '__main__':
    sys.exit(main())
