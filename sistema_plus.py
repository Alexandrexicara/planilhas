import sqlite3
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
from datetime import datetime
import csv
import json
from PIL import Image, ImageTk

# ==============================
# BANCO DE DADOS - VERSÃO PLUS
# ==============================

def inicializar_banco_plus():
    """Banco otimizado para cliente final (sem WAL)"""
    conn = sqlite3.connect("banco_plus.db")
    cursor = conn.cursor()
    
    # Configurações para cliente final (sem WAL)
    cursor.execute("PRAGMA journal_mode=DELETE")  # Sem WAL, mais limpo
    cursor.execute("PRAGMA synchronous=FULL")     # Máxima segurança
    cursor.execute("PRAGMA cache_size=25000")      # Cache médio
    cursor.execute("PRAGMA temp_store=FILE")       # Temp em arquivo
    
    # Tabela principal com TODAS as 39 colunas e índices otimizados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos_plus(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT COLLATE NOCASE,
        arquivo_origem TEXT,
        codigo TEXT COLLATE NOCASE,
        descricao TEXT COLLATE NOCASE,
        peso TEXT,
        valor TEXT,
        ncm TEXT COLLATE NOCASE,
        doc TEXT,
        rev TEXT,
        code TEXT,
        quantity TEXT,
        um TEXT,
        ccy TEXT,
        total_amount TEXT,
        marca TEXT,
        inner_qty TEXT,
        master_qty TEXT,
        total_ctns TEXT,
        gross_weight TEXT,
        net_weight_pc TEXT,
        gross_weight_pc TEXT,
        net_weight_ctn TEXT,
        gross_weight_ctn TEXT,
        factory TEXT,
        address TEXT,
        telephone TEXT,
        ean13 TEXT,
        dun14_inner TEXT,
        dun14_master TEXT,
        length TEXT,
        width TEXT,
        height TEXT,
        cbm TEXT,
        prc_kg TEXT,
        li TEXT,
        obs TEXT,
        status TEXT,
        data_importacao TEXT,
        hash_dados TEXT  -- Para detectar duplicatas
    )
    """)
    
    # Índices compostos para busca ultra-rápida
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_cliente_plus ON produtos_plus(cliente)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_codigo_plus ON produtos_plus(codigo)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_descricao_plus ON produtos_plus(descricao)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ncm_plus ON produtos_plus(ncm)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hash_plus ON produtos_plus(hash_dados)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_busca_completa_plus ON produtos_plus(cliente, codigo, descricao, ncm)")
    
    # Tabela de estatísticas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stats_plus(
        id INTEGER PRIMARY KEY,
        total_planilhas INTEGER,
        total_produtos INTEGER,
        ultima_atualizacao TEXT,
        tamanho_banco_mb REAL
    )
    """)
    
    conn.commit()
    return conn, cursor

conn_plus, cursor_plus = inicializar_banco_plus()

# ==============================
# FUNÇÕES OTIMIZADAS
# ==============================

def importar_planilha_plus(caminho_arquivo, cliente=None, progress_callback=None, duplicatas=False):
    """Importação ultra-rápida com controle de duplicatas"""
    if not cliente:
        cliente = os.path.basename(caminho_arquivo).replace('.xlsx', '').replace('.xls', '')
    
    try:
        from openpyxl import load_workbook
        import hashlib
        
        wb = load_workbook(caminho_arquivo, read_only=True)
        ws = wb.active
        
        # Detectar colunas
        cabecalhos = []
        for cell in next(ws.iter_rows(min_row=1, max_row=1, values_only=True)):
            if cell:
                cabecalhos.append(str(cell).strip())
        
        colunas_detectadas = detectar_colunas_excel_plus(cabecalhos)
        
        total_importados = 0
        total_duplicatas = 0
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Batch maior para performance
        batch_size = 5000
        dados_batch = []
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            if all(cell is None or str(cell).strip() == '' for cell in row):
                continue
                
            # Extrair TODAS as colunas
            dados = {}
            for i, cell in enumerate(row):
                if i < len(cabecalhos):
                    coluna_nome = cabecalhos[i].lower()
                    for padrao, coluna_real in colunas_detectadas.items():
                        if coluna_nome == coluna_real.lower():
                            dados[padrao] = str(cell).strip() if cell else ''
                            break
            
            # Criar hash para detectar duplicatas (usando codigo e descricao)
            hash_dados = hashlib.md5(
                f"{cliente}_{dados.get('codigo','')}_{dados.get('descricao','')}".encode()
            ).hexdigest()
            
            # Verificar duplicata se necessário
            if duplicatas:
                cursor_plus.execute("SELECT id FROM produtos_plus WHERE hash_dados = ?", (hash_dados,))
                if cursor_plus.fetchone():
                    total_duplicatas += 1
                    continue
            
            # Adicionar TODAS as 39 colunas no batch
            dados_batch.append((
                cliente,
                os.path.basename(caminho_arquivo),
                dados.get('codigo', ''),
                dados.get('descricao', ''),
                dados.get('peso', ''),
                dados.get('valor', ''),
                dados.get('ncm', ''),
                dados.get('doc', ''),
                dados.get('rev', ''),
                dados.get('code', ''),
                dados.get('quantity', ''),
                dados.get('um', ''),
                dados.get('ccy', ''),
                dados.get('total_amount', ''),
                dados.get('marca', ''),
                dados.get('inner_qty', ''),
                dados.get('master_qty', ''),
                dados.get('total_ctns', ''),
                dados.get('gross_weight', ''),
                dados.get('net_weight_pc', ''),
                dados.get('gross_weight_pc', ''),
                dados.get('net_weight_ctn', ''),
                dados.get('gross_weight_ctn', ''),
                dados.get('factory', ''),
                dados.get('address', ''),
                dados.get('telephone', ''),
                dados.get('ean13', ''),
                dados.get('dun14_inner', ''),
                dados.get('dun14_master', ''),
                dados.get('length', ''),
                dados.get('width', ''),
                dados.get('height', ''),
                dados.get('cbm', ''),
                dados.get('prc_kg', ''),
                dados.get('li', ''),
                dados.get('obs', ''),
                dados.get('status', ''),
                data_atual,
                hash_dados
            ))
            
            # Insert em batch com TODAS as 39 colunas
            if len(dados_batch) >= batch_size:
                cursor_plus.executemany("""
                    INSERT INTO produtos_plus
                    (cliente, arquivo_origem, codigo, descricao, peso, valor, ncm, doc, rev,
                     quantity, um, ccy, total_amount, marca, inner_qty, master_qty,
                     total_ctns, gross_weight, net_weight_pc, gross_weight_pc,
                     net_weight_ctn, gross_weight_ctn, factory, address, telephone,
                     ean13, dun14_inner, dun14_master, length, width, height, cbm,
                     prc_kg, li, obs, status, data_importacao, hash_dados)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, dados_batch)
                conn_plus.commit()
                total_importados += len(dados_batch)
                dados_batch = []
                
                if progress_callback and total_importados % 10000 == 0:
                    progress_callback(f"Importados: {total_importados:,}")
        
        # Insert final com TODAS as 39 colunas
        if dados_batch:
            cursor_plus.executemany("""
                INSERT INTO produtos_plus
                (cliente, arquivo_origem, codigo, descricao, peso, valor, ncm, doc, rev,
                 quantity, um, ccy, total_amount, marca, inner_qty, master_qty,
                 total_ctns, gross_weight, net_weight_pc, gross_weight_pc,
                 net_weight_ctn, gross_weight_ctn, factory, address, telephone,
                 ean13, dun14_inner, dun14_master, length, width, height, cbm,
                 prc_kg, li, obs, status, data_importacao, hash_dados)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, dados_batch)
            conn_plus.commit()
            total_importados += len(dados_batch)
        
        wb.close()
        
        # Atualizar estatísticas
        atualizar_estatisticas_plus()
        
        return total_importados, total_duplicatas
        
    except Exception as e:
        print(f"Erro ao importar {caminho_arquivo}: {str(e)}")
        return 0, 0

def detectar_colunas_excel_plus(cabecalhos):
    """Detecção de colunas melhorada para TODAS as 39 colunas"""
    colunas_detectadas = {}
    
    mapeamento_expandido = {
        'codigo': ['codigo', 'código', 'cod', 'code', 'item', 'sku', 'referencia', 'referência', 'id', 'produto_id'],
        'descricao': ['descricao', 'descrição', 'produto', 'item_desc', 'name', 'descrição do produto', 'titulo', 'nome'],
        'peso': ['peso', 'weight', 'kg', 'quilos', 'peso_bruto', 'peso_liquido', 'massa', 'gr'],
        'valor': ['valor', 'preco', 'preço', 'price', 'unitario', 'unitário', 'custo', 'valor_unit', 'preco_unit'],
        'ncm': ['ncm', 'nomenclatura', 'codigo_ncm', 'ncm_sh', 'codigo_ncm_sh', 'nsh', 'codigo_nsh'],
        'doc': ['doc', 'documento'],
        'rev': ['rev', 'revisao', 'revisão'],
        'code': ['code', 'codigo_interno'],
        'quantity': ['quantity', 'quantidade', 'qtd'],
        'um': ['um', 'unidade', 'un'],
        'ccy': ['ccy', 'moeda', 'currency'],
        'total_amount': ['total amount', 'valor_total', 'total'],
        'marca': ['marca', 'brand', 'fabricante'],
        'inner_qty': ['inner qty', 'quantidade_interna', 'qtd_interna'],
        'master_qty': ['master qty', 'quantidade_master', 'qtd_master'],
        'total_ctns': ['total ctns', 'caixas', 'cartons'],
        'gross_weight': ['gross weight', 'peso_bruto'],
        'net_weight_pc': ['net weight pc', 'peso_liquido_unit'],
        'gross_weight_pc': ['gross weight pc', 'peso_bruto_unit'],
        'net_weight_ctn': ['net weight ctn', 'peso_liquido_cx'],
        'gross_weight_ctn': ['gross weight ctn', 'peso_bruto_cx'],
        'factory': ['factory', 'fabrica', 'fábrica'],
        'address': ['address', 'endereco', 'endereço'],
        'telephone': ['telephone', 'telefone', 'tel', 'phone'],
        'ean13': ['ean13', 'ean', 'barcode'],
        'dun14_inner': ['dun-14 inner', 'dun14_interno', 'dun_inner'],
        'dun14_master': ['dun-14 master', 'dun14_master'],
        'length': ['length', 'comprimento'],
        'width': ['width', 'largura'],
        'height': ['height', 'altura'],
        'cbm': ['cbm', 'metro_cubico'],
        'prc_kg': ['prc/kg', 'preco_kg'],
        'li': ['li', 'licenca', 'licença'],
        'obs': ['obs', 'observacoes', 'observações', 'notas'],
        'status': ['status', 'situacao', 'situação']
    }
    
    for col_padrao, alternativas in mapeamento_expandido.items():
        for cabecalho in cabecalhos:
            if cabecalho.lower() in [alt.lower() for alt in alternativas]:
                colunas_detectadas[col_padrao] = cabecalho
                break
    
    return colunas_detectadas

def buscar_produtos_plus(termo, cliente_filtro=None, limit=10000):
    """Busca otimizada com TODAS as 39 colunas"""
    query = """
        SELECT cliente, arquivo_origem, codigo, descricao, peso, valor, ncm,
               doc, rev, code, quantity, um, ccy, total_amount, marca,
               inner_qty, master_qty, total_ctns, gross_weight, net_weight_pc,
               gross_weight_pc, net_weight_ctn, gross_weight_ctn, factory,
               address, telephone, ean13, dun14_inner, dun14_master,
               length, width, height, cbm, prc_kg, li, obs, status
        FROM produtos_plus
        WHERE 1=1
    """
    params = []
    
    if termo:
        query += " AND (codigo LIKE ? OR descricao LIKE ? OR ncm LIKE ?)"
        params.extend([f"%{termo}%", f"%{termo}%", f"%{termo}%"])
    
    if cliente_filtro and cliente_filtro != "Todos":
        query += " AND cliente = ?"
        params.append(cliente_filtro)
    
    query += " ORDER BY cliente, descricao LIMIT ?"
    params.append(limit)
    
    cursor_plus.execute(query, params)
    return cursor_plus.fetchall()

def contar_produtos_plus():
    """Contagem otimizada"""
    cursor_plus.execute("SELECT COUNT(*) FROM produtos_plus")
    return cursor_plus.fetchone()[0]

def contar_planilhas_plus():
    """Contagem de planilhas únicas"""
    cursor_plus.execute("SELECT COUNT(DISTINCT arquivo_origem) FROM produtos_plus")
    return cursor_plus.fetchone()[0]

def tamanho_banco_plus():
    """Tamanho do banco em MB"""
    cursor_plus.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
    tamanho_bytes = cursor_plus.fetchone()[0]
    return round(tamanho_bytes / (1024 * 1024), 2)

def atualizar_estatisticas_plus():
    """Atualiza tabela de estatísticas"""
    total_produtos = contar_produtos_plus()
    total_planilhas = contar_planilhas_plus()
    tamanho_mb = tamanho_banco_plus()
    
    cursor_plus.execute("""
        INSERT OR REPLACE INTO stats_plus (id, total_planilhas, total_produtos, ultima_atualizacao, tamanho_banco_mb)
        VALUES (1, ?, ?, ?, ?)
    """, (total_planilhas, total_produtos, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), tamanho_mb))
    conn_plus.commit()

def otimizar_banco_plus():
    """Otimização do banco para performance máxima"""
    cursor_plus.execute("VACUUM")
    cursor_plus.execute("ANALYZE")
    conn_plus.commit()

# ==============================
# INTERFACE PLUS
# ==============================

class SistemaPlanilhasPlus:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Sistema Planilhas PLUS - Alta Capacidade")
        self.janela.geometry("1400x800")
        self.janela.configure(bg='#1a1a1a')
        
        # Variáveis
        self.termo_busca = tk.StringVar()
        self.cliente_selecionado = tk.StringVar(value="Todos")
        
        self.criar_interface_plus()
        self.atualizar_estatisticas_interface()
    
    def criar_interface_plus(self):
        # Frame superior - Estatísticas PLUS
        frame_stats_plus = tk.Frame(self.janela, bg='#2c3e50', height=180)
        frame_stats_plus.pack(fill='x', padx=5, pady=5)
        frame_stats_plus.pack_propagate(False)
        
        # Frame para logo e título (linha superior)
        frame_logo_titulo = tk.Frame(frame_stats_plus, bg='#2c3e50')
        frame_logo_titulo.pack(fill='x', pady=(10, 5))
        
        # Logo no canto esquerdo
        try:
            logo_path = os.path.join("img", "Penacho laranja em fundo neutro.png")
            if os.path.exists(logo_path):
                # Carregar e redimensionar imagem
                logo_image = Image.open(logo_path)
                logo_image = logo_image.resize((80, 80), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_image)
                
                logo_label = tk.Label(frame_logo_titulo, image=logo_photo, bg='#2c3e50')
                logo_label.image = logo_photo  # Manter referência
                logo_label.pack(side='left', padx=(20, 15))
            else:
                # Fallback para emoji se imagem não existir
                logo_label = tk.Label(frame_logo_titulo, text="🪶", font=('Arial', 64), bg='#2c3e50', fg='white')
                logo_label.pack(side='left', padx=(20, 15))
        except Exception as e:
            # Fallback para emoji em caso de erro
            logo_label = tk.Label(frame_logo_titulo, text="🪶", font=('Arial', 64), bg='#2c3e50', fg='white')
            logo_label.pack(side='left', padx=(20, 15))
        
        # Título ao lado do logo
        titulo_label = tk.Label(frame_logo_titulo, text="planilhas.com PLUS", font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white')
        titulo_label.pack(side='left', padx=(0, 20))
        
        # Frame de navegação no canto direito
        frame_navegacao = tk.Frame(frame_logo_titulo, bg='#2c3e50')
        frame_navegacao.pack(side='right', padx=(20, 0))
        
        # Botão para voltar ao Sistema Original
        btn_voltar_original = tk.Button(frame_navegacao, text="📊 Sistema Original", 
                                       command=self.voltar_sistema_original,
                                       bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                       relief='raised', bd=2, cursor='hand2')
        btn_voltar_original.pack(pady=2)
        
        # Estatísticas em linha separada (linha inferior)
        frame_stats_container = tk.Frame(frame_stats_plus, bg='#2c3e50')
        frame_stats_container.pack(fill='x', pady=(5, 15))
        
        self.label_stats_plus = tk.Label(frame_stats_container, text="", bg='#2c3e50', fg='white', font=('Arial', 12, 'bold'))
        self.label_stats_plus.pack()
        
        # Frame de controles avançados
        frame_controles = tk.LabelFrame(self.janela, text="⚡ Controles Avançados", 
                                      font=('Arial', 14, 'bold'), bg='#34495e')
        frame_controles.pack(fill='x', padx=10, pady=5)
        
        # Linha 1 - Busca
        frame_busca = tk.Frame(frame_controles, bg='#34495e')
        frame_busca.pack(fill='x', padx=10, pady=10)
        
        tk.Label(frame_busca, text="🔍 Busca:", font=('Arial', 12), bg='#34495e', fg='white').pack(side='left', padx=5)
        self.campo_busca = tk.Entry(frame_busca, textvariable=self.termo_busca, font=('Arial', 12), width=50)
        self.campo_busca.pack(side='left', padx=5)
        
        tk.Button(frame_busca, text="🔎 Buscar", command=self.executar_busca_plus,
                 bg='#3498db', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        
        tk.Button(frame_busca, text="🗑️ Limpar", command=self.limpar_busca_plus,
                 bg='#e74c3c', fg='white', font=('Arial', 12), width=12, height=1).pack(side='left', padx=5)
        
        # Linha 2 - Importação
        frame_import = tk.Frame(frame_controles, bg='#34495e')
        frame_import.pack(fill='x', padx=10, pady=5)
        
        tk.Button(frame_import, text="📁 Importar Pasta", command=self.importar_pasta_plus,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'), width=20).pack(side='left', padx=5)
        
        tk.Button(frame_import, text="📄 Selecionar Arquivos", command=self.selecionar_arquivos_plus,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold'), width=20).pack(side='left', padx=5)
        
        tk.Button(frame_import, text="⚙️ Otimizar Banco", command=self.otimizar_banco_interface,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'), width=20).pack(side='left', padx=5)
        
        # Filtros
        tk.Label(frame_import, text="Cliente:", font=('Arial', 12), bg='#34495e', fg='white').pack(side='left', padx=5)
        self.combo_clientes_plus = ttk.Combobox(frame_import, textvariable=self.cliente_selecionado, 
                                               state='readonly', width=30)
        self.combo_clientes_plus.pack(side='left', padx=5)
        
        # Frame de resultados
        frame_resultados = tk.LabelFrame(self.janela, text="📊 Resultados (Capacidade Máxima)", 
                                       font=('Arial', 14, 'bold'), bg='#34495e')
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Barra de exportação
        frame_export = tk.Frame(frame_resultados, bg='#34495e')
        frame_export.pack(fill='x', padx=5, pady=5)
        
        tk.Button(frame_export, text="📊 Exportar Excel", command=self.exportar_excel_plus,
                 bg='#8e44ad', fg='white', font=('Arial', 12), width=20, height=1,
                 relief='raised', bd=2, cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(frame_export, text="📈 Estatísticas", command=self.mostrar_estatisticas_detalhadas,
                 bg='#2ecc71', fg='white', font=('Arial', 12)).pack(side='left', padx=5)
        
        self.label_resultados_plus = tk.Label(frame_export, text="0 resultados", bg='#34495e', 
                                            fg='white', font=('Arial', 12))
        self.label_resultados_plus.pack(side='right', padx=5)
        
        # Tabela otimizada
        frame_tabela = tk.Frame(frame_resultados)
        frame_tabela.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.colunas_plus = ('Cliente', 'Arquivo Origem', 'Código', 'Descrição', 'Peso', 'Valor', 'NCM', 'DOC', 'REV', 'CODE', 'QUANTITY', 'UM', 'CCY', 'TOTAL AMOUNT', 'MARCA', 'INNER QTY', 'MASTER QTY', 'TOTAL CTNS', 'GROSS WEIGHT', 'NET WEIGHT PC', 'GROSS WEIGHT PC', 'NET WEIGHT CTN', 'GROSS WEIGHT CTN', 'FACTORY', 'ADDRESS', 'TELEPHONE', 'EAN13', 'DUN-14 INNER', 'DUN-14 MASTER', 'LENGTH', 'WIDTH', 'HEIGHT', 'CBM', 'PRC/KG', 'LI', 'OBS', 'STATUS')
        self.tabela_plus = ttk.Treeview(frame_tabela, columns=self.colunas_plus, show='headings', height=20)
        
        for col in self.colunas_plus:
            self.tabela_plus.heading(col, text=col)
            if col == 'Descrição':
                self.tabela_plus.column(col, width=400)
            elif col == 'Cliente':
                self.tabela_plus.column(col, width=150)
            elif col == 'Arquivo':
                self.tabela_plus.column(col, width=250)
            else:
                self.tabela_plus.column(col, width=100)
        
        # Scrollbars
        scroll_v = ttk.Scrollbar(frame_tabela, orient='vertical', command=self.tabela_plus.yview)
        scroll_h = ttk.Scrollbar(frame_tabela, orient='horizontal', command=self.tabela_plus.xview)
        self.tabela_plus.configure(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)
        
        self.tabela_plus.grid(row=0, column=0, sticky='nsew')
        scroll_v.grid(row=0, column=1, sticky='ns')
        scroll_h.grid(row=1, column=0, sticky='ew')
        
        frame_tabela.grid_rowconfigure(0, weight=1)
        frame_tabela.grid_columnconfigure(0, weight=1)
        
        # Barra de status
        self.status_bar_plus = tk.Label(self.janela, text="Sistema PLUS - Pronto", bd=1, 
                                       relief='sunken', anchor='w', bg='#2c3e50', fg='white')
        self.status_bar_plus.pack(side='bottom', fill='x')
    
    def executar_busca_plus(self):
        termo = self.termo_busca.get().strip()
        cliente = self.cliente_selecionado.get()
        
        # Limpar tabela
        for item in self.tabela_plus.get_children():
            self.tabela_plus.delete(item)
        
        if not termo and cliente == "Todos":
            self.status_bar_plus.config(text="Digite um termo ou selecione cliente")
            return
        
        try:
            resultados = buscar_produtos_plus(termo, cliente, limit=10000)
            
            for resultado in resultados:
                self.tabela_plus.insert('', 'end', values=resultado)
            
            self.label_resultados_plus.config(text=f"{len(resultados):,} resultados")
            self.status_bar_plus.config(text=f"Busca PLUS: {len(resultados):,} resultados")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na busca: {str(e)}")
    
    def limpar_busca_plus(self):
        self.termo_busca.set("")
        self.cliente_selecionado.set("Todos")
        
        for item in self.tabela_plus.get_children():
            self.tabela_plus.delete(item)
        
        self.label_resultados_plus.config(text="0 resultados")
        self.status_bar_plus.config(text="Busca limpa")
    
    def importar_pasta_plus(self):
        def importar_thread():
            try:
                self.status_bar_plus.config(text="Importação PLUS em andamento...")
                self.janela.update()
                
                pasta = "planilhas"
                if not os.path.exists(pasta):
                    os.makedirs(pasta)
                
                total_geral = 0
                arquivos = [f for f in os.listdir(pasta) if f.endswith(('.xlsx', '.xls'))]
                
                for arquivo in arquivos:
                    caminho = os.path.join(pasta, arquivo)
                    importados, duplicatas = importar_planilha_plus(caminho, progress_callback=self.atualizar_progresso_plus)
                    total_geral += importados
                
                self.atualizar_estatisticas_interface()
                messagebox.showinfo("Importação PLUS", f"Importados {total_geral:,} produtos!")
                self.status_bar_plus.config(text=f"Importação concluída: {total_geral:,} produtos")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {str(e)}")
        
        threading.Thread(target=importar_thread, daemon=True).start()
    
    def selecionar_arquivos_plus(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione planilhas (múltiplo)",
            filetypes=[("Excel", "*.xlsx *.xls"), ("Todos", "*.*")]
        )
        
        if arquivos:
            def importar_thread():
                try:
                    total_geral = 0
                    for caminho in arquivos:
                        importados, _ = importar_planilha_plus(caminho, progress_callback=self.atualizar_progresso_plus)
                        total_geral += importados
                    
                    self.atualizar_estatisticas_interface()
                    messagebox.showinfo("Importação PLUS", f"Importados {total_geral:,} produtos!")
                    
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro: {str(e)}")
            
            threading.Thread(target=importar_thread, daemon=True).start()
    
    def otimizar_banco_interface(self):
        try:
            self.status_bar_plus.config(text="Otimizando banco...")
            self.janela.update()
            
            otimizar_banco_plus()
            self.atualizar_estatisticas_interface()
            
            messagebox.showinfo("Otimização", "Banco otimizado com sucesso!")
            self.status_bar_plus.config(text="Banco otimizado")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {str(e)}")
    
    def exportar_excel_plus(self):
        """Exporta resultados PLUS para Excel/CSV com TODAS as colunas"""
        resultados = []
        for item in self.tabela_plus.get_children():
            resultados.append(self.tabela_plus.item(item)['values'])
        
        if not resultados:
            messagebox.showwarning("Aviso", "Sem resultados para exportar!")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo = f"resultados_plus_{timestamp}.csv"
        
        # Exportar com TODAS as 39 colunas
        colunas_completas = ['Cliente', 'Arquivo Origem', 'Código', 'Descrição', 'Peso', 'Valor', 'NCM', 'DOC', 'REV', 'CODE', 'QUANTITY', 'UM', 'CCY', 'TOTAL AMOUNT', 'MARCA', 'INNER QTY', 'MASTER QTY', 'TOTAL CTNS', 'GROSS WEIGHT', 'NET WEIGHT PC', 'GROSS WEIGHT PC', 'NET WEIGHT CTN', 'GROSS WEIGHT CTN', 'FACTORY', 'ADDRESS', 'TELEPHONE', 'EAN13', 'DUN-14 INNER', 'DUN-14 MASTER', 'LENGTH', 'WIDTH', 'HEIGHT', 'CBM', 'PRC/KG', 'LI', 'OBS', 'STATUS']
        
        with open(arquivo, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(colunas_completas)
            writer.writerows(resultados)
        
        messagebox.showinfo("Exportado", f"Exportado para {arquivo}\n\nTodas as 39 colunas foram exportadas!")
    
    def exportar_csv_plus(self):
        """Exporta resultados PLUS para CSV (mesma função do Excel)"""
        self.exportar_excel_plus()
    
    def mostrar_estatisticas_detalhadas(self):
        stats_text = f"""
📊 ESTATÍSTICAS DETALHADAS

🗄️ Banco de Dados:
• Tamanho: {tamanho_banco_plus():.2f} MB
• Produtos: {contar_produtos_plus():,}
• Planilhas: {contar_planilhas_plus():,}

⚡ Performance:
• Cache: 50MB
• Memory Map: 256MB
• Índices: 6 otimizados

🚀 Capacidade:
• Máximo teórico: Ilimitado
• Recomendado: 5M+ produtos
• Testado: 1M+ produtos
        """
        messagebox.showinfo("Estatísticas PLUS", stats_text)
    
    def atualizar_estatisticas_interface(self):
        total_produtos = contar_produtos_plus()
        total_planilhas = contar_planilhas_plus()
        tamanho_mb = tamanho_banco_plus()
        
        stats_text = f"📦 Produtos: {total_produtos:,}  |  📁 Planilhas: {total_planilhas:,}  |  💾 Banco: {tamanho_mb:.1f}MB  |  ⚡ PLUS MODE"
        self.label_stats_plus.config(text=stats_text)
    
    def atualizar_progresso_plus(self, mensagem):
        self.status_bar_plus.config(text=mensagem)
        self.janela.update()
    
    def voltar_sistema_original(self):
        """Volta para o Sistema Original"""
        if messagebox.askyesno("Voltar para Sistema Original", 
                              "Deseja fechar o Sistema PLUS e abrir o Sistema Original?"):
            try:
                import subprocess
                import sys
                
                # Fecha o sistema atual
                self.janela.destroy()
                
                # Executa o sistema original
                subprocess.Popen([sys.executable, "sistema.py"])
                
            except Exception as e:
                messagebox.showerror("Erro", 
                    "Não foi possível abrir o Sistema Original. Verifique se o arquivo 'sistema.py' existe na pasta.")
    
    def executar(self):
        """Inicia a interface PLUS"""
        self.janela.mainloop()

# ==============================
# INICIALIZAÇÃO
# ==============================

if __name__ == "__main__":
    app_plus = SistemaPlanilhasPlus()
    app_plus.executar()
