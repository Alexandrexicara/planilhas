from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import sys
import subprocess
import sqlite3
import zipfile
import shutil
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sistema_plus_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Garantir que as pastas existam
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('static/images', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Configuração do sistema
SISTEMA_CONFIG = {
    'nome': 'Sistema Plus de Importação',
    'valor_original': 5000.00,
    'valor_promocional': 4500.00,
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

def get_db_connection():
    """Conexão com o banco de dados"""
    conn = sqlite3.connect('banco_plus.db')
    conn.row_factory = sqlite3.Row
    return conn

def extract_images_from_excel(excel_path, output_dir):
    """Extrai imagens do arquivo Excel automaticamente"""
    images = []
    
    try:
        with zipfile.ZipFile(excel_path, 'r') as z:
            for file in z.namelist():
                if file.startswith("xl/media/"):
                    name = os.path.basename(file)
                    path = os.path.join(output_dir, name)
                    
                    with open(path, "wb") as f:
                        f.write(z.read(file))
                    
                    images.append(path)
    except Exception as e:
        print(f"Erro ao extrair imagens: {e}")
    
    return images

def read_excel_with_images(excel_path):
    """Lê Excel e associa imagens automaticamente"""
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. Extrair imagens
    images = extract_images_from_excel(excel_path, temp_dir)
    
    # 2. Ler dados do Excel
    workbook = load_workbook(excel_path)
    sheet = workbook.active
    
    rows = []
    headers = []
    
    # Pegar cabeçalhos
    for cell in sheet[1]:
        if cell.value:
            headers.append(str(cell.value).strip())
    
    # Ler linhas de dados
    for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), 2):
        row_data = {}
        for i, value in enumerate(row):
            if i < len(headers):
                row_data[headers[i]] = str(value) if value is not None else ""
        
        # 3. Associar imagem por ordem
        img_index = row_idx - 2  # Ajuste para índice zero
        if img_index < len(images):
            row_data['picture'] = images[img_index]
        else:
            row_data['picture'] = None
        
        rows.append(row_data)
    
    return rows, images

def save_image_to_static(image_path):
    """Move imagem para pasta static e retorna URL"""
    if not image_path or not os.path.exists(image_path):
        return None
    
    filename = os.path.basename(image_path)
    new_path = f"static/uploads/{filename}"
    
    shutil.copy(image_path, new_path)
    return f"/static/uploads/{filename}"

def import_products_to_db(products_data):
    """Importa produtos para o banco de dados"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    imported_count = 0
    
    for product in products_data:
        try:
            # Salvar imagem se existir
            picture_url = None
            if product.get('picture'):
                picture_url = save_image_to_static(product['picture'])
            
            # Inserir no banco
            cursor.execute("""
                INSERT INTO produtos_plus (
                    cliente, arquivo_origem, codigo, descricao, peso, 
                    picture, data_importacao
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product.get('cliente', 'Web'),
                'upload_web',
                product.get('codigo', ''),
                product.get('descricao', ''),
                product.get('peso', ''),
                picture_url,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            imported_count += 1
            
        except Exception as e:
            print(f"Erro ao importar produto: {e}")
            continue
    
    conn.commit()
    conn.close()
    
    # Limpar pasta temporária
    if os.path.exists("temp_images"):
        shutil.rmtree("temp_images")
    
    return imported_count

@app.route('/')
def index():
    """Página inicial atraente"""
    return render_template('index.html', config=SISTEMA_CONFIG)

@app.route('/executar-sistema')
def executar_sistema():
    """Executa o sistema.py após login bem-sucedido"""
    try:
        subprocess.Popen([sys.executable, 'sistema.py'])
        # Retorna página visual ao invés de JSON puro
        return render_template('iniciando.html')
    except Exception as e:
        return render_template('iniciando.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Página de login do sistema"""
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        senha = request.form.get('senha', '')
        
        # Autenticação simples (padrão: admin@planilhas.com / admin123)
        if email == 'admin@planilhas.com' and senha == 'admin123':
            return jsonify({
                'success': True,
                'message': 'Login realizado com sucesso!',
                'redirect': url_for('executar_sistema')
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Email ou senha incorretos'
            }), 401
    
    return render_template('login.html', config=SISTEMA_CONFIG)

@app.route('/registro', methods=['POST'])
def registro():
    """Registrar novo usuário"""
    nome = request.form.get('nome', '')
    email = request.form.get('email', '').lower()
    senha = request.form.get('senha', '')
    confirma_senha = request.form.get('confirma_senha', '')
    
    if not all([nome, email, senha, confirma_senha]):
        return jsonify({
            'success': False,
            'message': 'Todos os campos são obrigatórios'
        }), 400
    
    if senha != confirma_senha:
        return jsonify({
            'success': False,
            'message': 'As senhas não correspondem'
        }), 400
    
    if len(senha) < 6:
        return jsonify({
            'success': False,
            'message': 'A senha deve ter no mínimo 6 caracteres'
        }), 400
    
    # Aqui você poderia salvar no banco de dados
    # Por enquanto, apenas retorna sucesso
    return jsonify({
        'success': True,
        'message': 'Usuário registrado com sucesso! Faça login agora.',
        'redirect': url_for('login_page')
    })

@app.route('/upload')
def upload_page():
    """Página de upload"""
    return render_template('upload.html', config=SISTEMA_CONFIG)

@app.route('/api/upload', methods=['POST'])
def upload_excel():
    """API para upload e processamento de Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nome de arquivo inválido'}), 400
        
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify({'error': 'Arquivo deve ser Excel (.xlsx ou .xls)'}), 400
        
        # Salvar arquivo temporário
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        
        # Processar Excel
        products_data, images = read_excel_with_images(temp_path)
        
        # Importar para banco
        imported_count = import_products_to_db(products_data)
        
        # Limpar arquivo temporário
        os.remove(temp_path)
        
        return jsonify({
            'success': True,
            'message': f'Importação concluída com sucesso!',
            'imported_count': imported_count,
            'images_found': len(images),
            'products_count': len(products_data)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/catalog')
def catalog():
    """Catálogo de produtos"""
    conn = get_db_connection()
    products = conn.execute("""
        SELECT * FROM produtos_plus 
        ORDER BY data_importacao DESC 
        LIMIT 100
    """).fetchall()
    conn.close()
    
    return render_template('catalog.html', products=products, config=SISTEMA_CONFIG)

@app.route('/api/stats')
def get_stats():
    """API de estatísticas"""
    conn = get_db_connection()
    
    stats = {
        'total_products': conn.execute("SELECT COUNT(*) FROM produtos_plus").fetchone()[0],
        'total_clients': conn.execute("SELECT COUNT(DISTINCT cliente) FROM produtos_plus").fetchone()[0],
        'recent_imports': conn.execute("""
            SELECT COUNT(*) FROM produtos_plus 
            WHERE data_importacao >= date('now', '-7 days')
        """).fetchone()[0]
    }
    
    conn.close()
    return jsonify(stats)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
