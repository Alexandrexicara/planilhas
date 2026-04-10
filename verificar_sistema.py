#!/usr/bin/env python3
"""
Verificação do sistema Plus
"""
import os

def main():
    print("🚀 SISTEMA PLUS - VERIFICAÇÃO")
    print("=" * 50)
    
    files = [
        'sistema_plus.py',
        'banco_plus.db', 
        'SISTEMA_PLUS.html',
        'flask_integration.py',
        'extrator_imagens_excel.py'
    ]
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file}")
    
    print("\n💡 COMO USAR:")
    print("1. Python: python sistema_plus.py")
    print("2. HTML: Abra SISTEMA_PLUS.html")
    print("3. Flask: python flask_integration.py")
    print("\n✅ Sistema pronto!")

if __name__ == "__main__":
    main()
