#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script para compilar app.py e copiar para Desktop"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def main():
    # Diretórios
    projeto = Path("e:/planilhas.com")
    desktop = Path(os.path.expanduser("~/Desktop"))
    dist_dir = projeto / "dist"
    exe_src = dist_dir / "app.exe"
    exe_dest = desktop / "Planilhas.exe"
    
    print("=" * 60)
    print("🔨 COMPILADOR - Planilhas.com")
    print("=" * 60)
    print(f"📁 Projeto: {projeto}")
    print(f"🖥️  Desktop: {desktop}")
    print(f"⏰ Horário: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Passo 1: Compilar com PyInstaller
        print("\n1️⃣  Compilando app.py com PyInstaller...")
        print("-" * 60)
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name=Planilhas",
            "--collect-all=flask",
            "--collect-all=werkzeug",
            "--collect-all=openpyxl",
            "--hidden-import=sistema",
            "--hidden-import=sistema_plus",
            "--clean",
            "app.py"
        ]
        
        result = subprocess.run(cmd, cwd=str(projeto), capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Compilação concluída com sucesso!")
        else:
            print("❌ Erro na compilação:")
            print(result.stderr)
            return False
        
        # Passo 2: Verificar se o EXE foi criado
        print("\n2️⃣  Verificando EXE gerado...")
        print("-" * 60)
        
        if exe_src.exists():
            size_mb = exe_src.stat().st_size / (1024 * 1024)
            print(f"✅ EXE encontrado: {exe_src}")
            print(f"📦 Tamanho: {size_mb:.2f} MB")
        else:
            print(f"❌ EXE não encontrado em: {exe_src}")
            return False
        
        # Passo 3: Copiar para Desktop
        print("\n3️⃣  Copiando para Desktop...")
        print("-" * 60)
        
        # Se já existe, remover
        if exe_dest.exists():
            exe_dest.unlink()
            print(f"🗑️  Removendo versão antiga: {exe_dest}")
        
        shutil.copy2(exe_src, exe_dest)
        print(f"✅ Copiado com sucesso!")
        print(f"📍 Arquivo: {exe_dest}")
        
        # Passo 4: Copiar também para releases
        print("\n4️⃣  Atualizando releases...")
        print("-" * 60)
        releases_dir = projeto / "releases"
        releases_dir.mkdir(exist_ok=True)
        exe_releases = releases_dir / "Planilhas.exe"
        
        if exe_releases.exists():
            exe_releases.unlink()
        
        shutil.copy2(exe_src, exe_releases)
        print(f"✅ Atualizado: {exe_releases}")
        
        # Resumo final
        print("\n" + "=" * 60)
        print("✨ SUCESSO! Seu aplicativo está pronto!")
        print("=" * 60)
        print(f"📂 Desktop: {exe_dest}")
        print(f"📂 Releases: {exe_releases}")
        print(f"⏰ Concluído em: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
