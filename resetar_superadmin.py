#!/usr/bin/env python3
"""
Script para resetar/recuperar senha do superadmin
"""
import sys
sys.path.append('.')

from web_access_db import init_db, ensure_superadmin

def main():
    email = "santossilvac992@gmail.com"
    senha = "celio48santos"
    
    print("🚀 Resetando Superadmin...")
    print("=" * 50)
    
    init_db()
    ensure_superadmin(email, senha)
    
    print("✅ Superadmin criado/atualizado!")
    print(f"📧 Email: {email}")
    print(f"🔑 Senha: {senha}")
    print("=" * 50)
    print("\n💡 Agora você pode fazer login com estas credenciais:")
    print("   Email: santossilvac992@gmail.com")
    print("   Senha: celio48santos")

if __name__ == "__main__":
    main()
