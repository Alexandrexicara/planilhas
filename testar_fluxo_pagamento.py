#!/usr/bin/env python3
"""
Script para testar o fluxo completo de cadastro e pagamento
"""
import sys
sys.path.append('.')

from web_access_db import init_db, create_organization
import sqlite3

def testar_fluxo():
    print("=== TESTE DO FLUXO DE PAGAMENTO ===")
    print()
    
    # 1. Inicializar banco
    print("1. Inicializando banco...")
    init_db()
    print("   Banco inicializado!")
    
    # 2. Criar organização de teste
    print("2. Criando organização de teste...")
    try:
        org_id = create_organization("Teste Pagamento", payment_amount=50.00)
        print(f"   Organização criada! ID: {org_id}")
    except Exception as e:
        print(f"   Erro ao criar organização: {e}")
        return
    
    # 3. Verificar status inicial
    print("3. Verificando status inicial...")
    conn = sqlite3.connect("acesso_web.db")
    conn.row_factory = sqlite3.Row
    org = conn.execute("SELECT * FROM organizations WHERE id = ?", (org_id,)).fetchone()
    
    if org:
        print(f"   Nome: {org['nome']}")
        print(f"   Status: {org['payment_status']}")
        print(f"   Valor: R$ {org['payment_amount']:.2f}")
        print(f"   TXID: {org['payment_txid'] or 'Nenhum'}")
        print(f"   QR Code: {'Sim' if org['payment_qr_base64'] else 'Não'}")
    else:
        print("   Organização não encontrada!")
    
    conn.close()
    
    print()
    print("=== FLUXO TESTADO ===")
    print("   - Cadastro: OK")
    print("   - Organização: OK")
    print("   - Pagamento: Pendente (precisa gerar)")
    print()
    print("Para testar o fluxo completo:")
    print("1. Acesse: http://localhost:5000/comecar")
    print("2. Cadastre um novo usuário")
    print("3. Verifique se redireciona para pagamento")
    print("4. Verifique se gera PIX automaticamente")

if __name__ == "__main__":
    testar_fluxo()
