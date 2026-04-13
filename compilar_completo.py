#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para compilar app.py com TODAS as dependências"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def main():
    projeto = Path("e:/planilhas.com")
    desktop = Path(os.path.expanduser("~/Desktop"))
    dist_dir = projeto / "dist"
    
    print("=" * 70)
    print("🔨 COMPILÇÃO COMPLETA - Planilhas.com")
    print("=" * 70)
    print(f"📁 Projeto: {projeto}")
    print(f"🖥️  Desktop: {desktop}")
    print(f"⏰ Horário: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    
    try:
        # Limpar build anterior
        print("\n1️⃣  Limpando builds anteriores...")
        print("-" * 70)
        
        for folder in ["build", "dist", "__pycache__"]:
            folder_path = projeto / folder
            if folder_path.exists():
                shutil.rmtree(folder_path)
                print(f"✅ Removido: {folder}")
        
        # Comando PyInstaller COMPLETO
        print("\n2️⃣  Compilando com PyInstaller (isso pode levar 2-5 minutos)...")
        print("-" * 70)
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=Planilhas",
            "--add-data=templates;templates",
            "--add-data=static;static",
            "--add-data=banco_plus.db;.",
            "--add-data=banco.db;.",
            "--add-data=usuarios.db;.",
            "--hidden-import=sistema",
            "--hidden-import=sistema_plus",
            "--hidden-import=menu_principal",
            "--hidden-import=usuarios_db",
            "--hidden-import=gerenciamento_usuarios",
            "--hidden-import=sistema_online_offline",
            "--hidden-import=banco_offline",
            "--hidden-import=flask",
            "--hidden-import=werkzeug",
            "--hidden-import=jinja2",
            "--hidden-import=openpyxl",
            "--hidden-import=PIL",
            "--hidden-import=sqlite3",
            "--collect-all=flask",
            "--collect-all=werkzeug",
            "--collect-all=jinja2",
            "--collect-all=openpyxl",
            "--noupx",
            "app.py"
        ]
        
        print(f"🚀 Executando: {' '.join(cmd[:5])}...")
        print("   (aguarde, isso pode levar alguns minutos...)\n")
        
        result = subprocess.run(cmd, cwd=str(projeto))
        
        if result.returncode != 0:
            print("\n❌ Erro na compilação!")
            return False
        
        # Verificar EXE criado
        print("\n3️⃣  Verificando EXE gerado...")
        print("-" * 70)
        
        exe_src = dist_dir / "Planilhas.exe"
        
        if exe_src.exists():
            size_mb = exe_src.stat().st_size / (1024 * 1024)
            print(f"✅ EXE encontrado!")
            print(f"📦 Tamanho: {size_mb:.2f} MB")
            print(f"📍 Local: {exe_src}")
        else:
            print(f"❌ EXE não encontrado em: {exe_src}")
            return False
        
        # Copiar para Desktop
        print("\n4️⃣  Copiando para Desktop...")
        print("-" * 70)
        
        exe_dest = desktop / "Planilhas.exe"
        
        if exe_dest.exists():
            exe_dest.unlink()
            print(f"🗑️  Removida versão anterior")
        
        shutil.copy2(exe_src, exe_dest)
        print(f"✅ Copiado com sucesso!")
        print(f"📍 Desktop: {exe_dest}")
        
        # Copiar para releases
        print("\n5️⃣  Atualizando releases...")
        print("-" * 70)
        
        releases_dir = projeto / "releases"
        releases_dir.mkdir(exist_ok=True)
        exe_releases = releases_dir / "Planilhas.exe"
        
        if exe_releases.exists():
            exe_releases.unlink()
        
        shutil.copy2(exe_src, exe_releases)
        print(f"✅ Atualizado: {exe_releases}")
        
        # Resumo final
        print("\n" + "=" * 70)
        print("✨ SUCESSO! Compilação completa!")
        print("=" * 70)
        print(f"📂 Desktop: {exe_dest} ({size_mb:.2f} MB)")
        print(f"📂 Releases: {exe_releases}")
        print(f"\n🎯 PRÓXIMOS PASSOS:")
        print(f"   1. Clique 2x no Planilhas.exe no Desktop")
        print(f"   2. Abra: http://127.0.0.1:5000 no navegador")
        print(f"   3. Teste todas as funcionalidades")
        print(f"\n⏰ Concluído em: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
