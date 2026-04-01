import pandas as pd
import sqlite3
import json
import re
from datetime import datetime

class ImportadorProdutos:
    def __init__(self):
        self.db_file = "banco.db"
        self.conectar_banco()
    
    def conectar_banco(self):
        """Conecta ao banco de dados"""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        
        # Verificar se tabela produtos existe
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc TEXT,
            rev TEXT,
            codigo TEXT,
            ncm TEXT,
            quantity INTEGER,
            um TEXT,
            ccy TEXT,
            valor REAL,
            total_amount TEXT,
            descricao TEXT,
            marca TEXT,
            inner_qty TEXT,
            master_qty TEXT,
            total_ctns INTEGER,
            peso REAL,
            gross_weight REAL,
            net_weight_pc TEXT,
            gross_weight_pc REAL,
            net_weight_ctn REAL,
            gross_weight_ctn REAL,
            factory TEXT,
            address TEXT,
            telephone TEXT,
            ean13 TEXT,
            dun14_inner TEXT,
            dun14_master TEXT,
            length REAL,
            width REAL,
            height REAL,
            cbm REAL,
            prc_kg TEXT,
            li TEXT,
            obs TEXT,
            status TEXT,
            data_importacao TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()
    
    def limpar_dados(self, texto):
        """Limpa e formata texto"""
        if pd.isna(texto) or texto is None:
            return ""
        
        texto = str(texto).strip()
        
        # Remover caracteres especiais problemáticos
        texto = re.sub(r'[^\x20-\x7E]', '', texto)
        
        # Substituir quebras de linha
        texto = texto.replace('\n', ' ').replace('\r', ' ')
        
        # Limitar tamanho de campos de texto
        if len(texto) > 500:
            texto = texto[:500] + "..."
        
        return texto
    
    def converter_numero(self, valor):
        """Converte string para número"""
        if pd.isna(valor) or valor is None or valor == '':
            return None
        
        try:
            # Remover caracteres não numéricos exceto ponto e vírgula
            valor_str = str(valor).replace(',', '.').replace('$', '').replace('USD', '').strip()
            
            # Se começar com =, é fórmula do Excel
            if valor_str.startswith('='):
                return None
                
            return float(valor_str)
        except:
            return None
    
    def converter_inteiro(self, valor):
        """Converte string para inteiro"""
        num = self.converter_numero(valor)
        return int(num) if num is not None else None
    
    def importar_dados(self, arquivo_excel):
        """Importa dados do arquivo Excel"""
        try:
            print(f"Importando dados de: {arquivo_excel}")
            
            # Ler arquivo Excel
            df = pd.read_excel(arquivo_excel)
            
            print(f"Encontradas {len(df)} linhas no arquivo")
            
            # Limpar tabela antes de importar
            self.cursor.execute("DELETE FROM produtos")
            self.conn.commit()
            
            produtos_importados = 0
            erros = 0
            
            for index, row in df.iterrows():
                try:
                    # Limpar e preparar dados
                    dados = {
                        'doc': self.limpar_dados(row.get('doc', '')),
                        'rev': self.limpar_dados(row.get('rev', '')),
                        'codigo': self.limpar_dados(row.get('codigo', '')),
                        'ncm': self.limpar_dados(row.get('ncm', '')),
                        'quantity': self.converter_inteiro(row.get('quantity')),
                        'um': self.limpar_dados(row.get('um', '')),
                        'ccy': self.limpar_dados(row.get('ccy', '')),
                        'valor': self.converter_numero(row.get('valor')),
                        'total_amount': self.limpar_dados(row.get('total_amount', '')),
                        'descricao': self.limpar_dados(row.get('descricao', '')),
                        'marca': self.limpar_dados(row.get('marca', '')),
                        'inner_qty': self.limpar_dados(row.get('inner_qty', '')),
                        'master_qty': self.limpar_dados(row.get('master_qty', '')),
                        'total_ctns': self.converter_inteiro(row.get('total_ctns')),
                        'peso': self.converter_numero(row.get('peso')),
                        'gross_weight': self.converter_numero(row.get('gross_weight')),
                        'net_weight_pc': self.limpar_dados(row.get('net_weight_pc', '')),
                        'gross_weight_pc': self.converter_numero(row.get('gross_weight_pc')),
                        'net_weight_ctn': self.converter_numero(row.get('net_weight_ctn')),
                        'gross_weight_ctn': self.converter_numero(row.get('gross_weight_ctn')),
                        'factory': self.limpar_dados(row.get('factory', '')),
                        'address': self.limpar_dados(row.get('address', '')),
                        'telephone': self.limpar_dados(row.get('telephone', '')),
                        'ean13': self.limpar_dados(row.get('ean13', '')),
                        'dun14_inner': self.limpar_dados(row.get('dun14_inner', '')),
                        'dun14_master': self.limpar_dados(row.get('dun14_master', '')),
                        'length': self.converter_numero(row.get('length')),
                        'width': self.converter_numero(row.get('width')),
                        'height': self.converter_numero(row.get('height')),
                        'cbm': self.converter_numero(row.get('cbm')),
                        'prc_kg': self.limpar_dados(row.get('prc_kg', '')),
                        'li': self.limpar_dados(row.get('li', '')),
                        'obs': self.limpar_dados(row.get('obs', '')),
                        'status': self.limpar_dados(row.get('status', ''))
                    }
                    
                    # Inserir no banco
                    self.cursor.execute("""
                    INSERT INTO produtos (
                        id, doc, rev, codigo, ncm, quantity, um, ccy, valor, total_amount,
                        descricao, marca, inner_qty, master_qty, total_ctns, peso,
                        gross_weight, net_weight_pc, gross_weight_pc, net_weight_ctn,
                        gross_weight_ctn, factory, address, telephone, ean13,
                        dun14_inner, dun14_master, length, width, height, cbm,
                        prc_kg, li, obs, status, data_importacao
                    ) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        dados['doc'], dados['rev'], dados['codigo'], dados['ncm'],
                        dados['quantity'], dados['um'], dados['ccy'], dados['valor'],
                        dados['total_amount'], dados['descricao'], dados['marca'],
                        dados['inner_qty'], dados['master_qty'], dados['total_ctns'],
                        dados['peso'], dados['gross_weight'], dados['net_weight_pc'],
                        dados['gross_weight_pc'], dados['net_weight_ctn'],
                        dados['gross_weight_ctn'], dados['factory'], dados['address'],
                        dados['telephone'], dados['ean13'], dados['dun14_inner'],
                        dados['dun14_master'], dados['length'], dados['width'],
                        dados['height'], dados['cbm'], dados['prc_kg'],
                        dados['li'], dados['obs'], dados['status'],
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ))
                    
                    produtos_importados += 1
                    
                    # Mostrar progresso
                    if produtos_importados % 5 == 0:
                        print(f"   Importados: {produtos_importados} produtos")
                
                except Exception as e:
                    erros += 1
                    print(f"   Erro na linha {index + 1}: {str(e)[:100]}")
                    continue
            
            self.conn.commit()
            
            print(f"\nImportacao concluida!")
            print(f"   Produtos importados: {produtos_importados}")
            print(f"   Erros: {erros}")
            
            # Estatísticas
            self.cursor.execute("SELECT COUNT(*) FROM produtos")
            total = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM produtos WHERE valor > 0")
            com_valor = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM produtos WHERE marca != ''")
            com_marca = self.cursor.fetchone()[0]
            
            print(f"\nEstatisticas:")
            print(f"   Total de produtos: {total}")
            print(f"   Com valor definido: {com_valor}")
            print(f"   Com marca: {com_marca}")
            
            return True
            
        except Exception as e:
            print(f"Erro na importacao: {str(e)}")
            return False
    
    def fechar_conexao(self):
        """Fecha conexão com banco"""
        if hasattr(self, 'conn'):
            self.conn.close()

def testar_importacao():
    """Testa a importação com dados simulados"""
    print("Testando importacao de produtos...")
    
    importador = ImportadorProdutos()
    
    # Criar dados de teste baseados nos logs
    dados_teste = [
        {
            'doc': '5266',
            'rev': '1',
            'codigo': '1',
            'ncm': 'PAP01',
            'quantity': 3600,
            'um': 'PC',
            'ccy': 'USD',
            'valor': 0.56,
            'total_amount': '2016.00',
            'descricao': 'PAPEL DE PAREDE ADESIVO ESTAMPA ESTRELADO 5 METROS',
            'marca': 'WESTERN HOME',
            'inner_qty': '',
            'master_qty': '30',
            'total_ctns': 120,
            'peso': 1060.2,
            'gross_weight': 1092,
            'net_weight_pc': '',
            'gross_weight_pc': 0.392,
            'net_weight_ctn': 8.835,
            'gross_weight_ctn': 9.1,
            'factory': 'YOUNGCOM HONGKONG LIMITED',
            'address': 'YIWU,CHINA',
            'telephone': '',
            'ean13': '7897186068084',
            'dun14_inner': '',
            'dun14_master': '57897186068089',
            'length': 25,
            'width': 20.5,
            'height': 47,
            'cbm': 2.8905,
            'prc_kg': '=J3/P3',
            'li': 'SEM LI',
            'obs': 'NCM OK',
            'status': 'REPOSIÇÃO'
        }
    ]
    
    try:
        # Limpar tabela
        importador.cursor.execute("DELETE FROM produtos")
        importador.conn.commit()
        
        # Inserir dados de teste
        for dados in dados_teste:
            importador.cursor.execute("""
            INSERT INTO produtos (
                id, doc, rev, codigo, ncm, quantity, um, ccy, valor, total_amount,
                descricao, marca, inner_qty, master_qty, total_ctns, peso,
                gross_weight, net_weight_pc, gross_weight_pc, net_weight_ctn,
                gross_weight_ctn, factory, address, telephone, ean13,
                dun14_inner, dun14_master, length, width, height, cbm,
                prc_kg, li, obs, status, data_importacao
            ) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dados['doc'], dados['rev'], dados['codigo'], dados['ncm'],
                dados['quantity'], dados['um'], dados['ccy'], dados['valor'],
                dados['total_amount'], dados['descricao'], dados['marca'],
                dados['inner_qty'], dados['master_qty'], dados['total_ctns'],
                dados['peso'], dados['gross_weight'], dados['net_weight_pc'],
                dados['gross_weight_pc'], dados['net_weight_ctn'],
                dados['gross_weight_ctn'], dados['factory'], dados['address'],
                dados['telephone'], dados['ean13'], dados['dun14_inner'],
                dados['dun14_master'], dados['length'], dados['width'],
                dados['height'], dados['cbm'], dados['prc_kg'],
                dados['li'], dados['obs'], dados['status'],
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
        
        importador.conn.commit()
        
        print("✅ Dados de teste inseridos com sucesso!")
        
        # Verificar inserção
        importador.cursor.execute("SELECT COUNT(*) FROM produtos")
        total = importador.cursor.fetchone()[0]
        print(f"📊 Total de produtos no banco: {total}")
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
    
    finally:
        importador.fechar_conexao()

if __name__ == "__main__":
    testar_importacao()
