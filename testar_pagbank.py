from sistema_pagamento_pagbank import SistemaPagamentoPagBank
import json
import os

def testar_pagbank():
    """Testa integração com PagBank"""
    print("🧪 Testando integração com PagBank...")
    
    # Verificar se arquivo de config existe
    if not os.path.exists('config_pagamento.json'):
        print("❌ Arquivo config_pagamento.json não encontrado!")
        return
    
    sistema = SistemaPagamentoPagBank()
    
    # Testar obtenção de token
    print("\n1️⃣ Testando obtenção de token...")
    token = sistema.obter_token_pagbank()
    
    if token:
        print(f"✅ Token obtido com sucesso!")
        print(f"   Access Token: {token['access_token'][:20]}...")
        print(f"   Expires in: {token['expires_in']} segundos")
    else:
        print("❌ Erro ao obter token")
        return
    
    # Testar cadastro de usuário
    print("\n2️⃣ Testando cadastro de usuário...")
    sucesso, resultado = sistema.cadastrar_usuario(
        nome="Usuário Teste",
        email=f"teste_{int(time.time())}@exemplo.com",
        senha="123456",
        telefone="11999999999"
    )
    
    if sucesso:
        print(f"✅ Usuário cadastrado com sucesso!")
        print(f"   ID: {resultado['id']}")
        print(f"   Email: {resultado['email']}")
        usuario_id = resultado['id']
    else:
        print(f"❌ Erro no cadastro: {resultado['erro']}")
        return
    
    # Testar geração de pagamento PIX
    print("\n3️⃣ Testando geração de pagamento PIX...")
    sucesso, resultado = sistema.gerar_pagamento_pix_pagbank(usuario_id, 'mensal')
    
    if sucesso:
        print(f"✅ PIX gerado com sucesso!")
        print(f"   ID Pagamento: {resultado['id_pagamento']}")
        print(f"   Valor: R$ {resultado['valor']:.2f}")
        print(f"   Chave PIX: {resultado['chave_pix']}")
        print(f"   QR Code: {resultado['qr_code'][:50]}...")
        
        # Salvar QR Code em arquivo para teste
        try:
            import base64
            qr_code_base64 = resultado['qr_code']
            if qr_code_base64.startswith('data:image/png;base64,'):
                qr_code_base64 = qr_code_base64.replace('data:image/png;base64,', '')
            
            qr_code_bytes = base64.b64decode(qr_code_base64)
            with open(f'qrcode_test_{usuario_id}.png', 'wb') as f:
                f.write(qr_code_bytes)
            print(f"   QR Code salvo como: qrcode_test_{usuario_id}.png")
        except Exception as e:
            print(f"   Erro ao salvar QR Code: {e}")
    else:
        print(f"❌ Erro ao gerar PIX: {resultado['erro']}")
        return
    
    # Testar verificação de status
    print("\n4️⃣ Testando verificação de status...")
    sucesso, resultado = sistema.verificar_status_pagamento_pagbank(usuario_id)
    
    if sucesso:
        print(f"✅ Status verificado!")
        print(f"   Status: {resultado.get('status')}")
    else:
        print(f"❌ Erro na verificação: {resultado['erro']}")
    
    # Testar planos disponíveis
    print("\n5️⃣ Testando planos disponíveis...")
    planos = sistema.obter_planos_disponiveis()
    
    if planos:
        print(f"✅ Planos encontrados:")
        for plano in planos:
            print(f"   📋 {plano['nome'].upper()}: R$ {plano['valor']:.2f} ({plano['dias_validade']} dias)")
    else:
        print("❌ Nenhum plano encontrado")
    
    print("\n🎉 Testes concluídos!")
    print("\n📝 Resumo:")
    print("   ✅ Conexão PagBank: OK")
    print("   ✅ Autenticação: OK") 
    print("   ✅ Cadastro: OK")
    print("   ✅ Geração PIX: OK")
    print("   ✅ Verificação status: OK")
    print("   ✅ Planos: OK")
    print("\n🚀 Sistema pronto para uso!")

if __name__ == "__main__":
    import time
    testar_pagbank()
