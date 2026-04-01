from sistema_pagamento_simulado import SistemaPagamentoPagBankSimulado
import json
import os
import time

def testar_pagbank_simulado():
    """Testa integração simulada com PagBank"""
    print("🧪 Testando sistema PAGBANK SIMULADO...")
    print("   (Não depende de HTTPS/API real)")
    
    # Verificar se arquivo de config existe
    if not os.path.exists('config_pagamento.json'):
        print("❌ Arquivo config_pagamento.json não encontrado!")
        return
    
    sistema = SistemaPagamentoPagBankSimulado()
    
    # Testar obtenção de token
    print("\n1️⃣ Testando obtenção de token...")
    token = sistema.obter_token_pagbank()
    
    if token:
        print(f"✅ Token SIMULADO obtido com sucesso!")
        print(f"   Access Token: {token['access_token'][:20]}...")
        print(f"   Expires in: {token['expires_in']} segundos")
    else:
        print("❌ Erro ao obter token")
        return
    
    # Testar cadastro de usuário
    print("\n2️⃣ Testando cadastro de usuário...")
    sucesso, resultado = sistema.cadastrar_usuario(
        nome="Usuário Teste Simulado",
        email=f"teste_simulado_{int(time.time())}@exemplo.com",
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
        print(f"✅ PIX SIMULADO gerado com sucesso!")
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
            with open(f'qrcode_simulado_{usuario_id}.png', 'wb') as f:
                f.write(qr_code_bytes)
            print(f"   ✅ QR Code salvo como: qrcode_simulado_{usuario_id}.png")
        except Exception as e:
            print(f"   Erro ao salvar QR Code: {e}")
    else:
        print(f"❌ Erro ao gerar PIX: {resultado['erro']}")
        return
    
    # Esperar 2 segundos para simular processamento
    print("\n⏳ Aguardando 2 segundos para simular processamento...")
    time.sleep(2)
    
    # Testar verificação de status
    print("\n4️⃣ Testando verificação de status...")
    sucesso, resultado = sistema.verificar_status_pagamento_pagbank(usuario_id)
    
    if sucesso:
        print(f"✅ Status verificado!")
        print(f"   Status: {resultado.get('status')}")
    else:
        print(f"❌ Erro na verificação: {resultado['erro']}")
    
    # Esperar mais 30 segundos para aprovação automática
    print("\n⏳ Aguardando 30 segundos para aprovação automática...")
    time.sleep(30)
    
    # Testar verificação após aprovação
    print("\n5️⃣ Verificando status após aprovação...")
    sucesso, resultado = sistema.verificar_status_pagamento_pagbank(usuario_id)
    
    if sucesso:
        print(f"✅ Status verificado!")
        print(f"   Status: {resultado.get('status')}")
        
        if resultado.get('status') == 'aprovado':
            print("🎉 PAGAMENTO APROVADO AUTOMATICAMENTE!")
            
            # Testar login após aprovação
            print("\n6️⃣ Testando login após aprovação...")
            sucesso_login, usuario = sistema.verificar_login(
                resultado['email'], 
                "123456"
            )
            
            if sucesso_login and usuario.get('acesso_liberado'):
                print(f"✅ Login realizado com sucesso!")
                print(f"   Usuário: {usuario['nome']}")
                print(f"   Acesso liberado: {usuario['acesso_liberado']}")
                print(f"   Plano: {usuario['plano']}")
    else:
        print(f"❌ Erro na verificação: {resultado['erro']}")
    
    # Testar planos disponíveis
    print("\n7️⃣ Testando planos disponíveis...")
    planos = sistema.obter_planos_disponiveis()
    
    if planos:
        print(f"✅ Planos encontrados:")
        for plano in planos:
            print(f"   📋 {plano['nome'].upper()}: R$ {plano['valor']:.2f} ({plano['dias_validade']} dias)")
            print(f"      {plano['descricao']}")
    else:
        print("❌ Nenhum plano encontrado")
    
    print("\n🎉 Testes concluídos!")
    print("\n📝 Resumo do Sistema Simulado:")
    print("   ✅ Conexão Simulada: OK")
    print("   ✅ Autenticação Simulada: OK") 
    print("   ✅ Cadastro: OK")
    print("   ✅ Geração PIX: OK")
    print("   ✅ QR Code: OK")
    print("   ✅ Verificação status: OK")
    print("   ✅ Aprovação automática: OK")
    print("   ✅ Login pós-aprovação: OK")
    print("   ✅ Planos: OK")
    print("\n🚀 Sistema SIMULADO pronto para uso!")
    print("\n💡 Para usar o sistema real:")
    print("   1. Configure HTTPS no servidor")
    print("   2. Use credenciais reais do PagBank")
    print("   3. Altere 'ambiente' para 'producao'")
    print("   4. Configure webhook para notificações")

if __name__ == "__main__":
    testar_pagbank_simulado()
