#!/usr/bin/env python3
"""
Sistema Plus - Versão Simplificada
Servidor web básico sem dependências externas
"""

import http.server
import socketserver
import os
import json
import urllib.parse
from pathlib import Path

# Configuração
PORT = 8000
SISTEMA_CONFIG = {
    'nome': 'Sistema Plus de Importação',
    'valor_original': 5000.00,
    'valor_promocional': 50.00,
    'desconto': 10,
    'versao': '2.0',
    'recursos': [
        'Importação automática de Excel',
        'Extração automática de imagens', 
        'Catálogo web completo',
        'Gestão de produtos',
        'Relatórios detalhados'
    ]
}

class SistemaHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Manipular requisições GET"""
        if self.path == '/':
            self.serve_index()
        elif self.path == '/upload':
            self.serve_upload()
        elif self.path == '/catalog':
            self.serve_catalog()
        elif self.path == '/api/stats':
            self.serve_stats()
        elif self.path.startswith('/static/'):
            self.serve_static()
        else:
            self.send_error(404, "Página não encontrada")
    
    def serve_index(self):
        """Servir página inicial"""
        html = self.get_index_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_upload(self):
        """Servir página de upload"""
        html = self.get_upload_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_catalog(self):
        """Servir catálogo"""
        html = self.get_catalog_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_stats(self):
        """Servir estatísticas da API"""
        stats = {
            'total_products': 0,
            'total_clients': 0,
            'recent_imports': 0
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(stats).encode('utf-8'))
    
    def serve_static(self):
        """Servir arquivos estáticos"""
        file_path = self.path[1:]  # Remove o '/'
        if os.path.exists(file_path):
            self.send_response(200)
            if file_path.endswith('.css'):
                self.send_header('Content-type', 'text/css')
            elif file_path.endswith('.js'):
                self.send_header('Content-type', 'application/javascript')
            elif file_path.endswith('.png'):
                self.send_header('Content-type', 'image/png')
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                self.send_header('Content-type', 'image/jpeg')
            else:
                self.send_header('Content-type', 'text/plain')
            self.end_headers()
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "Arquivo não encontrado")
    
    def get_index_html(self):
        """HTML da página inicial"""
        return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{SISTEMA_CONFIG['nome']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .hero {{
            text-align: center;
            padding: 80px 20px;
            color: white;
        }}
        .hero h1 {{ font-size: 3.5rem; font-weight: 800; margin-bottom: 20px; text-shadow: 0 2px 20px rgba(0,0,0,0.3); }}
        .hero p {{ font-size: 1.3rem; margin-bottom: 40px; opacity: 0.9; }}
        .price-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 40px;
            border-radius: 20px;
            max-width: 500px;
            margin: 0 auto;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }}
        .discount-badge {{
            background: #10b981;
            color: white;
            padding: 8px 20px;
            border-radius: 50px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 20px;
        }}
        .original-price {{ text-decoration: line-through; opacity: 0.7; font-size: 1.2rem; }}
        .current-price {{ font-size: 3rem; font-weight: 800; margin: 20px 0; }}
        .btn {{
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
        }}
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 60px 0;
        }}
        .feature-card {{
            background: rgba(255,255,255,0.95);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .feature-card:hover {{ transform: translateY(-5px); }}
        .feature-icon {{
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 2rem;
            color: white;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}
        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        .stat-number {{ font-size: 2.5rem; font-weight: 800; color: #667eea; }}
        .nav {{
            background: rgba(255,255,255,0.95);
            padding: 15px 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }}
        .nav .container {{ display: flex; justify-content: space-between; align-items: center; }}
        .nav a {{ color: #667eea; text-decoration: none; font-weight: 600; margin: 0 15px; }}
        .nav a:hover {{ color: #764ba2; }}
        .main-content {{ margin-top: 100px; }}
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
                <a href="/upload">Importar</a>
                <a href="/catalog">Catálogo</a>
            </div>
        </div>
    </nav>

    <div class="main-content">
        <div class="hero">
            <h1>🚀 Sistema Plus</h1>
            <p>Importação automática de Excel com extração inteligente de imagens</p>
            
            <div class="price-card">
                <div class="discount-badge">🏷️ {SISTEMA_CONFIG['desconto']}% OFF</div>
                <h3>Sistema Completo de Importação</h3>
                <div class="original-price">De R$ {SISTEMA_CONFIG['valor_original']:.2f}</div>
                <div class="current-price">R$ {SISTEMA_CONFIG['valor_promocional']:.2f}</div>
                <p>Pagamento único, acesso vitalício</p>
                <a href="/upload" class="btn">🚀 Começar Agora</a>
                <small style="display: block; margin-top: 10px;">
                    🛡️ Garantia de 7 dias | Suporte dedicado
                </small>
            </div>
        </div>

        <div class="container">
            <h2 style="text-align: center; color: white; font-size: 2.5rem; margin-bottom: 20px;">
                ⭐ Recursos Principais
            </h2>
            
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

            <h2 style="text-align: center; color: white; font-size: 2.5rem; margin: 40px 0 20px;">
                📊 Estatísticas do Sistema
            </h2>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="totalProducts">-</div>
                    <h5>Produtos Importados</h5>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="totalClients">-</div>
                    <h5>Clientes Ativos</h5>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="recentImports">-</div>
                    <h5>Importações Recentes</h5>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Carregar estatísticas
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {{
                document.getElementById('totalProducts').textContent = data.total_products;
                document.getElementById('totalClients').textContent = data.total_clients;
                document.getElementById('recentImports').textContent = data.recent_imports;
            }})
            .catch(error => console.error('Erro:', error));
    </script>
</body>
</html>
        """
    
    def get_upload_html(self):
        """HTML da página de upload"""
        return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Importar Excel - Sistema Plus</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 20px;
            padding: 60px 20px;
            text-align: center;
            background: rgba(102, 102, 241, 0.05);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .upload-area:hover {
            background: rgba(102, 102, 241, 0.1);
            border-color: #764ba2;
        }
        h1 { color: #667eea; margin-bottom: 20px; }
        h2 { color: #333; margin-bottom: 20px; }
        .btn {
            display: inline-block;
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
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
            color: white;
        }
        .alert {
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
        }
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .nav {
            background: rgba(255,255,255,0.95);
            padding: 15px 0;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        .nav a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            margin: 0 15px;
        }
        .nav a:hover { color: #764ba2; }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">🏠 Início</a>
            <a href="/upload">📤 Importar</a>
            <a href="/catalog">🛒 Catálogo</a>
        </div>

        <div class="card">
            <h1>📤 Importar Planilha Excel</h1>
            <p>Envie sua planilha Excel com produtos e imagens para importação automática</p>

            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <div style="font-size: 4rem; color: #667eea; margin-bottom: 20px;">☁️</div>
                <h2>Arraste e solte seu arquivo aqui</h2>
                <p>ou</p>
                <button class="btn">📁 Selecionar Arquivo</button>
                <input type="file" id="fileInput" accept=".xlsx,.xls" style="display: none;" onchange="handleFile(this)">
                <p><small>Formatos: .xlsx, .xls (máx. 16MB)</small></p>
            </div>

            <div id="fileInfo" style="display: none;" class="alert alert-info">
                <h4>📄 Arquivo Selecionado</h4>
                <div id="fileName"></div>
            </div>

            <div id="results" style="display: none;" class="alert alert-success">
                <h4>✅ Importação Concluída!</h4>
                <div id="resultsContent"></div>
                <a href="/catalog" class="btn">👁️ Ver Catálogo</a>
                <button class="btn" onclick="resetUpload()">📝 Importar Outro</button>
            </div>
        </div>

        <div class="card">
            <h2>📋 Como Preparar sua Planilha</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h3 style="color: #10b981;">✅ O que fazer:</h3>
                    <ul>
                        <li>Coloque imagens diretamente nas células</li>
                        <li>Use cabeçalhos na primeira linha</li>
                        <li>Mantenha a ordem das imagens</li>
                        <li>Salve como .xlsx</li>
                    </ul>
                </div>
                <div>
                    <h3 style="color: #ef4444;">❌ O que evitar:</h3>
                    <ul>
                        <li>Não use imagens em comentários</li>
                        <li>Não mude a ordem após colar</li>
                        <li>Não use arquivos protegidos</li>
                        <li>Não exceda 16MB</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
        function handleFile(input) {
            const file = input.files[0];
            if (file) {
                document.getElementById('fileName').textContent = file.name;
                document.getElementById('fileInfo').style.display = 'block';
                
                // Simular processamento
                setTimeout(() => {
                    document.getElementById('resultsContent').innerHTML = 
                        '<p>📦 Produtos importados: <strong>0</strong></p>' +
                        '<p>🖼️ Imagens encontradas: <strong>0</strong></p>' +
                        '<p>📊 Total de linhas: <strong>0</strong></p>' +
                        '<p>✅ Sistema pronto para uso!</p>';
                    document.getElementById('results').style.display = 'block';
                }, 2000);
            }
        }

        function resetUpload() {
            document.getElementById('fileInput').value = '';
            document.getElementById('fileInfo').style.display = 'none';
            document.getElementById('results').style.display = 'none';
        }

        // Drag and drop
        document.addEventListener('DOMContentLoaded', function() {
            const uploadArea = document.querySelector('.upload-area');
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.style.background = 'rgba(102, 102, 241, 0.2)';
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.style.background = 'rgba(102, 102, 241, 0.05)';
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.style.background = 'rgba(102, 102, 241, 0.05)';
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    document.getElementById('fileInput').files = files;
                    handleFile(document.getElementById('fileInput'));
                }
            });
        });
    </script>
</body>
</html>
        """
    
    def get_catalog_html(self):
        """HTML do catálogo"""
        return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catálogo de Produtos - Sistema Plus</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        h1 { color: #667eea; margin-bottom: 20px; }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            margin: 5px;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            color: white;
        }
        .nav {
            background: rgba(255,255,255,0.95);
            padding: 15px 0;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        .nav a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            margin: 0 15px;
        }
        .nav a:hover { color: #764ba2; }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        .empty-state .icon {
            font-size: 4rem;
            color: #ddd;
            margin-bottom: 20px;
        }
        .search-box {
            width: 100%;
            padding: 15px;
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            font-size: 1rem;
            margin-bottom: 20px;
        }
        .search-box:focus {
            outline: none;
            border-color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/">🏠 Início</a>
            <a href="/upload">📤 Importar</a>
            <a href="/catalog">🛒 Catálogo</a>
        </div>

        <div class="card">
            <h1>🛒 Catálogo de Produtos</h1>
            <p>0 produtos cadastrados</p>
            
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <input type="text" class="search-box" placeholder="🔍 Buscar produtos..." style="flex: 1;">
                <button class="btn">🔄 Atualizar</button>
                <a href="/upload" class="btn">➕ Importar Mais</a>
            </div>

            <div class="empty-state">
                <div class="icon">📦</div>
                <h2>Nenhum produto encontrado</h2>
                <p>Comece importando sua primeira planilha Excel para ver os produtos aqui.</p>
                <a href="/upload" class="btn">📤 Importar Produtos</a>
            </div>
        </div>
    </div>
</body>
</html>
        """

def main():
    """Função principal"""
    print("🚀 Iniciando Sistema Plus - Servidor Web Simplificado")
    print("=" * 60)
    print(f"📍 Endereço: http://localhost:{PORT}")
    print(f"📍 Rede: http://0.0.0.0:{PORT}")
    print("=" * 60)
    print("📋 Funcionalidades:")
    print("   ✅ Página inicial com design moderno")
    print("   ✅ Sistema de R$5.000 por R$4.500")
    print("   ✅ Interface de upload (simulada)")
    print("   ✅ Catálogo de produtos")
    print("   ✅ Navegação completa")
    print("=" * 60)
    print("⚠️  Pressione Ctrl+C para parar o servidor")
    print("=" * 60)
    
    # Criar pastas necessárias
    os.makedirs('static', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    
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
