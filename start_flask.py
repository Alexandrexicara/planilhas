#!/usr/bin/env python3
"""
Script para iniciar o Sistema Plus com Flask
"""
import os
import sys

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = [
        'flask', 'openpyxl', 'pillow', 'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Dependências faltando:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Instale com: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas")
    return True

def check_directories():
    """Verifica se as pastas necessárias existem"""
    required_dirs = [
        'static/uploads',
        'static/images', 
        'templates',
        'uploads'
    ]
    
    for dir_path in required_dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("✅ Estrutura de pastas verificada")

def main():
    """Função principal"""
    print("🚀 Iniciando Sistema Plus com Flask")
    print("=" * 50)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar pastas
    check_directories()
    
    # Importar e iniciar o app
    try:
        from app import app
        print("✅ Aplicação Flask carregada com sucesso")
        print("\n🌐 Acessando o sistema:")
        print("   - Local: http://localhost:5000")
        print("   - Rede: http://0.0.0.0:5000")
        print("\n📋 Funcionalidades disponíveis:")
        print("   - Página inicial com design moderno")
        print("   - Importação de Excel com extração de imagens")
        print("   - Catálogo web de produtos")
        print("   - Sistema de R$5.000 por R$4.500")
        print("\n⚠️  Pressione Ctrl+C para parar o servidor")
        print("=" * 50)
        
        # Iniciar servidor
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar a aplicação: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
