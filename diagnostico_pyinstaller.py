#!/usr/bin/env python
"""
Script de diagnóstico para problemas de compilação com PyInstaller
Ajuda a identificar e resolver MemoryError
"""

import sys
import os
import subprocess
import psutil
from pathlib import Path

def check_python_environment():
    """Verifica configuração do ambiente Python"""
    print("=" * 60)
    print("📋 DIAGNÓSTICO DO AMBIENTE PYTHON")
    print("=" * 60)
    
    print(f"\n✓ Python: {sys.version}")
    print(f"✓ Executável: {sys.executable}")
    print(f"✓ Plataforma: {sys.platform}")
    
    # Verifica RAM
    ram = psutil.virtual_memory()
    print(f"\n💾 MEMÓRIA:")
    print(f"   Total: {ram.total / (1024**3):.1f} GB")
    print(f"   Disponível: {ram.available / (1024**3):.1f} GB")
    print(f"   Uso: {ram.percent}%")
    
    if ram.available / (1024**3) < 2:
        print("\n⚠️  AVISO: Menos de 2GB de RAM disponível!")
        print("   Use: python build_exe_light.py")
    
    return ram.available / (1024**3) >= 2

def check_pyinstaller():
    """Verifica PyInstaller"""
    print("\n" + "=" * 60)
    print("📦 VERIFICAÇÃO DO PYINSTALLER")
    print("=" * 60)
    
    try:
        import PyInstaller
        print(f"✓ PyInstaller: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("✗ PyInstaller não instalado")
        print("\nInstalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        return True

def check_dependencies():
    """Verifica dependências obrigatórias"""
    print("\n" + "=" * 60)
    print("📚 VERIFICAÇÃO DE DEPENDÊNCIAS")
    print("=" * 60)
    
    dependencies = [
        'flask',
        'werkzeug',
        'click',
        'jinja2',
        'openpyxl',
        'psutil'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep}")
        except ImportError:
            print(f"✗ {dep} FALTANDO")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Instalando dependências faltantes: {', '.join(missing)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
    
    return len(missing) == 0

def check_flask_import():
    """Testa importação do Flask"""
    print("\n" + "=" * 60)
    print("🧪 TESTE DE IMPORTAÇÃO")
    print("=" * 60)
    
    try:
        from flask import Flask
        print("✓ Flask importado com sucesso")
        return True
    except MemoryError:
        print("✗ MemoryError ao importar Flask")
        print("  Aumentar arquivo de paginação (Página 1 do guia)")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

def recommend_build_method(has_memory):
    """Recomenda método de compilação"""
    print("\n" + "=" * 60)
    print("💡 RECOMENDAÇÃO")
    print("=" * 60)
    
    if has_memory:
        print("\n✅ Seu sistema está OK para compilação normal:")
        print("\n   python build_exe.py\n")
    else:
        print("\n⚠️  Seu sistema precisa do modo leve:")
        print("\n   python build_exe_light.py\n")

def main():
    print("\n🔧 Iniciando diagnóstico...\n")
    
    # Executa verificações
    has_memory = check_python_environment()
    check_pyinstaller()
    check_dependencies()
    check_flask_import()
    recommend_build_method(has_memory)
    
    print("=" * 60)
    print("✓ Diagnóstico concluído!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erro durante diagnóstico: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("Pressione Enter para sair...")
