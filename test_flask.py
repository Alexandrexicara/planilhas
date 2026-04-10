#!/usr/bin/env python3
"""
Teste simples do Flask
"""

try:
    from flask import Flask
    print("✅ Flask importado com sucesso")
    
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "<h1>✅ Flask está funcionando!</h1><p>Sistema Plus pronto para uso</p>"
    
    print("✅ Aplicação de teste criada")
    print("🚀 Iniciando servidor na porta 5001...")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
    
except ImportError as e:
    print(f"❌ Erro ao importar Flask: {e}")
    print("📦 Execute: pip install flask")
except Exception as e:
    print(f"❌ Erro geral: {e}")
