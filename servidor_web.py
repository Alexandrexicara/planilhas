#!/usr/bin/env python3
"""
Sistema Plus - Servidor Web Ultra Simplificado
Versão garantida para funcionar em qualquer ambiente Python
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os

PORT = 8000

class SistemaHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Sistema Plus - Importação Automática</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .hero {
            text-align: center;
            padding: 60px 20px;
            color: white;
        }
        .hero h1 {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 20px;
            text-shadow: 0 2px 20px rgba(0,0,0,0.3);
        }
        .hero p {
            font-size: 1.2rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        .price-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 40px;
            border-radius: 20px;
            max-width: 500px;
            margin: 0 auto 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }
        .discount-badge {
            background: #10b981;
            color: white;
            padding: 8px 20px;
            border-radius: 50px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 20px;
        }
        .original-price {
            text-decoration: line-through;
            opacity: 0.7;
            font-size: 1.2rem;
        }
        .current-price {
            font-size: 2.5rem;
            font-weight: 800;
            margin: 20px 0;
        }
        .btn {
            display: inline-block;
            padding: 15px 40px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: 1.1rem;
            margin: 10px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }
        .feature-card {
            background: rgba(255,255,255,0.95);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
        }
        .feature-icon {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 1.5rem;
            color: white;
        }
        .nav {
            background: rgba(255,255,255,0.95);
            padding: 15px 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        .nav .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            margin: 0 15px;
        }
        .nav a:hover { color: #764ba2; }
        .main-content { margin-top: 80px; }
        .section-title {
            text-align: center;
            color: white;
            font-size: 2.5rem;
            margin: 40px 0 20px;
        }
        .upload-demo {
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 40px 0;
        }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px;
            background: rgba(102, 102, 241, 0.05);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            background: rgba(102, 102, 241, 0.1);
            border-color: #764ba2;
        }
    </style>
</head>
<body>
    <nav class="nav">
        <div class="container">
            <div style="font-size: 1.5rem; font-weight: 700; color: #667eea;">
                🚀 Sistema Plus
            </div>
            <div>
                <a href="/">Início</a>
                <a href="#upload">Importar</a>
                <a href="#features">Recursos</a>
            </div>
        </div>
    </nav>

    <div class="main-content">
        <div class="hero">
            <h1>🚀 Sistema Plus</h1>
            <p>Importação automática de Excel com extração inteligente de imagens</p>
            
            <div class="price-card">
                <div class="discount-badge">🏷️ 10% OFF</div>
                <h3>Sistema Completo de Importação</h3>
                <div class="original-price">De R$ 5.000,00</div>
                <div class="current-price">R$ 4.500,00</div>
                <p>Pagamento único, acesso vitalício</p>
                <a href="#upload" class="btn">🚀 Começar Agora</a>
                <small style="display: block; margin-top: 10px;">
                    🛡️ Garantia de 7 dias | Suporte dedicado
                </small>
            </div>
        </div>

        <div class="container">
            <div id="upload" class="upload-demo">
                <h2 style="color: #667eea; margin-bottom: 20px;">📤 Importar Planilha Excel</h2>
                <p style="margin-bottom: 30px;">Envie sua planilha Excel com produtos e imagens para importação automática</p>
                
                <div class="upload-area" onclick="alert('Funcionalidade de upload implementada no sistema completo!')">
                    <div style="font-size: 3rem; color: #667eea; margin-bottom: 15px;">☁️</div>
                    <h3>Arraste e solte seu arquivo aqui</h3>
                    <p>ou clique para selecionar</p>
                    <button class="btn">📁 Selecionar Arquivo</button>
                    <p><small>Formatos: .xlsx, .xls (máx. 16MB)</small></p>
                </div>
            </div>

            <h2 id="features" class="section-title">⭐ Recursos Principais</h2>
            
            <div class="features">
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Importação Automática</h3>
                    <p>Importe planilhas Excel automaticamente com detecção inteligente de colunas</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🖼️</div>
                    <h3>Extração de Imagens</h3>
                    <p>Extrai automaticamente imagens coladas no Excel e associa aos produtos</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🌐</div>
                    <h3>Catálogo Web</h3>
                    <p>Gere automaticamente um catálogo web profissional para seus produtos</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">💾</div>
                    <h3>Banco de Dados</h3>
                    <p>Armazenamento seguro e organizado de todos os seus produtos</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <h3>Relatórios</h3>
                    <p>Relatórios detalhados sobre importações e estatísticas de uso</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Alta Performance</h3>
                    <p>Processamento rápido e eficiente mesmo com grandes volumes de dados</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Animação suave ao clicar nos links de navegação
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Efeito de hover nos cards
        document.querySelectorAll('.feature-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
    </script>
</body>
</html>"""
            
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404, "Página não encontrada")

def open_browser():
    """Abre o navegador após iniciar o servidor"""
    time.sleep(1.5)
    webbrowser.open(f'http://localhost:{PORT}')

def main():
    """Função principal"""
    print("🚀 Sistema Plus - Servidor Web")
    print("=" * 50)
    print(f"📍 Servidor: http://localhost:{PORT}")
    print("=" * 50)
    print("📋 Sistema pronto com:")
    print("   ✅ Página inicial moderna")
    print("   ✅ Sistema R$5.000 por R$4.500")
    print("   ✅ Design responsivo")
    print("   ✅ Interface de upload")
    print("   ✅ Todos os recursos visuais")
    print("=" * 50)
    print("🌐 Abrindo navegador automaticamente...")
    print("⚠️  Pressione Ctrl+C para parar")
    print("=" * 50)
    
    # Abrir navegador em thread separada
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Iniciar servidor
    with socketserver.TCPServer(("", PORT), SistemaHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor parado pelo usuário")
        finally:
            httpd.server_close()

if __name__ == "__main__":
    main()
