from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import sys
import sqlite3
import zipfile
import shutil
import subprocess
import time
import importlib
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
import json
from datetime import datetime

# Importacao segura dos modulos desktop (podem falhar em ambiente server/headless)
MODULOS_IMPORTACAO = {}
ERROS_IMPORTACAO = {}


def importar_modulo(nome_modulo):
    try:
        modulo = importlib.import_module(nome_modulo)
        MODULOS_IMPORTACAO[nome_modulo] = True
        return modulo
    except Exception as e:
        MODULOS_IMPORTACAO[nome_modulo] = False
        ERROS_IMPORTACAO[nome_modulo] = str(e)
        print(f"[AVISO] Nao foi possivel importar {nome_modulo}: {e}")
        return None


sistema = importar_modulo('sistema')
sistema_plus = importar_modulo('sistema_plus')

app = Flask(__name__)
app.secret_key = 'sistema_plus_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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


def ambiente_desktop_disponivel():
    """Indica se o servidor consegue abrir janelas desktop (GUI)."""
    if os.name == 'nt':
        return True
    return bool(os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'))


def nome_ambiente_execucao():
    """Nome amigavel do ambiente atual para mensagens."""
    if os.environ.get('RENDER'):
        return 'Render'
    if os.name == 'nt':
        return 'Windows'
    return 'Servidor Linux sem interface grafica'


def abrir_janela_sistema(script_name, nome_exibicao):
    """Abre um sistema desktop em uma nova janela sem bloquear o Flask."""
    script_path = os.path.join(BASE_DIR, script_name)

    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Arquivo nao encontrado: {script_name}")

    if not ambiente_desktop_disponivel():
        ambiente = nome_ambiente_execucao()
        raise RuntimeError(
            f"Nao e possivel abrir janela desktop no ambiente {ambiente}. Use a interface web."
        )

    popen_kwargs = {
        'cwd': BASE_DIR,
    }

    if os.name == 'nt':
        pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        executable = pythonw_path if os.path.exists(pythonw_path) else sys.executable
        creationflags = getattr(subprocess, 'CREATE_NEW_CONSOLE', 0)
        if creationflags:
            popen_kwargs['creationflags'] = creationflags
    else:
        executable = sys.executable
        popen_kwargs['start_new_session'] = True

    processo = subprocess.Popen([executable, script_path], **popen_kwargs)
    time.sleep(0.6)
    if processo.poll() is not None:
        raise RuntimeError(
            f"{nome_exibicao} encerrou logo apos iniciar (codigo {processo.returncode})."
        )

    return {
        'nome': nome_exibicao,
        'arquivo': script_name,
        'pid': processo.pid,
        'status': 'sucesso',
        'mensagem': f'{nome_exibicao} aberto em nova janela.'
    }

@app.route('/')
def index():
    """Página inicial atraente"""
    return render_template('index.html', config=SISTEMA_CONFIG)

@app.route('/executar-sistema-legado')
def executar_sistema_legado():
    """Executa funcoes dos modulos dentro do mesmo processo Flask."""
    try:
        dados_sistema = {
            'status': 'sucesso',
            'mensagem': 'Sistema iniciado com sucesso!',
            'timestamp': datetime.now().isoformat(),
            'modulos_carregados': []
        }

        # Modulo sistema
        try:
            if sistema is not None:
                dados_sistema['modulos_carregados'].append('[OK] sistema.py carregado')
            else:
                erro = ERROS_IMPORTACAO.get('sistema', 'modulo nao carregado')
                dados_sistema['modulos_carregados'].append(f'[ERRO] sistema.py: {erro[:80]}')
        except Exception as e:
            dados_sistema['modulos_carregados'].append(f'[ERRO] sistema.py: {str(e)[:50]}')

        # Modulo sistema_plus
        try:
            if sistema_plus is not None and hasattr(sistema_plus, 'contar_produtos_plus'):
                dados_sistema['total_produtos'] = sistema_plus.contar_produtos_plus()
            if sistema_plus is not None and hasattr(sistema_plus, 'contar_planilhas_plus'):
                dados_sistema['total_planilhas'] = sistema_plus.contar_planilhas_plus()

            if sistema_plus is not None:
                dados_sistema['modulos_carregados'].append('[OK] sistema_plus.py carregado')
            else:
                erro = ERROS_IMPORTACAO.get('sistema_plus', 'modulo nao carregado')
                dados_sistema['modulos_carregados'].append(f'[ERRO] sistema_plus.py: {erro[:80]}')
        except Exception as e:
            dados_sistema['modulos_carregados'].append(f'[ERRO] sistema_plus.py: {str(e)[:50]}')

        return render_template(
            'sistema.html',
            config=SISTEMA_CONFIG,
            resultado=dados_sistema
        )
    except Exception as e:
        return render_template('iniciando.html', erro=str(e))


@app.route('/executar-sistema')
def executar_sistema():
    """Abre as janelas do sistema original e/ou PLUS a partir do Flask."""
    try:
        alvo = request.args.get('target', 'both').lower()
        scripts_por_alvo = {
            'original': [('sistema.py', 'Sistema Original')],
            'plus': [('sistema_plus.py', 'Sistema Plus')],
            'both': [
                ('sistema.py', 'Sistema Original'),
                ('sistema_plus.py', 'Sistema Plus')
            ]
        }

        scripts_para_abrir = scripts_por_alvo.get(alvo, scripts_por_alvo['both'])
        ambiente_gui = ambiente_desktop_disponivel()
        ambiente_nome = nome_ambiente_execucao()
        dados_sistema = {
            'status': 'sucesso',
            'mensagem': 'As janelas do sistema foram abertas com sucesso.',
            'timestamp': datetime.now().isoformat(),
            'modulos_carregados': [],
            'janelas_abertas': [],
            'alvo': alvo,
            'ambiente_gui': ambiente_gui,
            'ambiente_nome': ambiente_nome
        }

        for script_name, nome_exibicao in scripts_para_abrir:
            try:
                janela = abrir_janela_sistema(script_name, nome_exibicao)
                dados_sistema['janelas_abertas'].append(janela)
                dados_sistema['modulos_carregados'].append(f'[OK] {script_name} aberto em nova janela')
            except Exception as e:
                dados_sistema['status'] = 'parcial'
                dados_sistema['janelas_abertas'].append({
                    'nome': nome_exibicao,
                    'arquivo': script_name,
                    'status': 'erro',
                    'mensagem': str(e)
                })
                dados_sistema['modulos_carregados'].append(f'[ERRO] {script_name}: {str(e)[:80]}')

        try:
            if sistema_plus is not None and hasattr(sistema_plus, 'contar_produtos_plus'):
                dados_sistema['total_produtos'] = sistema_plus.contar_produtos_plus()
            if sistema_plus is not None and hasattr(sistema_plus, 'contar_planilhas_plus'):
                dados_sistema['total_planilhas'] = sistema_plus.contar_planilhas_plus()

            if sistema_plus is not None:
                dados_sistema['modulos_carregados'].append('[OK] Estatisticas do sistema_plus.py carregadas')
            else:
                erro = ERROS_IMPORTACAO.get('sistema_plus', 'modulo nao carregado')
                dados_sistema['modulos_carregados'].append(
                    f'[ERRO] Estatisticas indisponiveis (sistema_plus.py): {erro[:80]}'
                )
        except Exception as e:
            dados_sistema['modulos_carregados'].append(f'[ERRO] Estatisticas do sistema_plus.py: {str(e)[:80]}')

        if not ambiente_gui:
            dados_sistema['status'] = 'erro'
            dados_sistema['mensagem'] = (
                f"Ambiente {ambiente_nome} nao suporta janelas desktop. "
                "Use apenas as rotas web."
            )

        if dados_sistema['janelas_abertas'] and all(
            item.get('status') == 'erro' for item in dados_sistema['janelas_abertas']
        ):
            dados_sistema['status'] = 'erro'
            if ambiente_gui:
                dados_sistema['mensagem'] = 'Nao foi possivel abrir as janelas solicitadas.'
        elif ambiente_gui and any(item.get('status') == 'erro' for item in dados_sistema['janelas_abertas']):
            dados_sistema['mensagem'] = 'Algumas janelas abriram e outras falharam.'

        return render_template('sistema.html',
                             config=SISTEMA_CONFIG,
                             resultado=dados_sistema)
    except Exception as e:
        return render_template('iniciando.html', erro=str(e))



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
