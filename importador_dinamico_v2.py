import pandas as pd
import sqlite3
import re
from datetime import datetime

class ImportadorDinamico:
    """Importador que lida automaticamente com colunas extras do Excel"""
    
    def __init__(self, db_file='banco.db'):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.max_colunas = 100
        
        # Mapeamento de colunas principais
        self.mapeamento_colunas = {
            'picture': 'picture',
            'doc': 'doc',
            'rev': 'rev',
            'item': 'codigo',
            'code': 'ncm',
            'quantity': 'quantity',
            'um': 'um',
            'ccy': 'ccy',
            'unit_price_umo': 'valor',
            'total_amount_umo': 'total_amount',
            'descricao_portugues_description_portuguese': 'descricao',
            'marca_brand': 'marca',
            'inner_quantity': 'inner_qty',
            'master_quantity': 'master_qty',
            'total_ctns': 'total_ctns',
            'total_net_weight_kg': 'peso',
            'total_gross_weight_kg': 'gross_weight',
            'net_weight_pc_g': 'net_weight_pc',
            'gross_weight_pc_g': 'gross_weight_pc',
            'net_weight_ctn_kg': 'net_weight_ctn',
            'gross_weight_ctn_kg': 'gross_weight_ctn',
            'name_of_factory': 'factory',
            'address_of_factory': 'address',
            'telephone': 'telephone',
            'ean13': 'ean13',
            'dun_14_inner': 'dun14_inner',
            'dun_14_master': 'dun14_master',
            'length_ctn': 'length',
            'width_ctn': 'width',
            'height_ctn': 'height',
            'total_cbm': 'cbm',
            'hs_code': 'hs_code',
            'prckg': 'prc_kg',
            'li': 'li',
            'obs': 'obs',
            'status_da_compra': 'status'
        }
        
    def obter_colunas_tabela(self):
        self.cursor.execute("PRAGMA table_info(produtos)")
        colunas = self.cursor.fetchall()
        return {col[1]: col[2] for col in colunas}
    
    def normalizar_nome_coluna(self, nome):
        nome_original = str(nome).strip()
        nome = nome_original.lower()
        nome = re.sub(r'[^\w\s]', '_', nome)
        nome = re.sub(r'\s+', '_', nome)
        nome = re.sub(r'_+', '_', nome)
        nome = nome.strip('_')
        
        # Verificar mapeamento
        for padrao_excel, nome_banco in self.mapeamento_colunas.items():
            if nome == padrao_excel or nome.replace('_', '') == padrao_excel.replace('_', ''):
                return nome_banco
        
        if len(nome) > 50:
            nome = nome[:50]
        
        if not nome or nome.replace('_', '').isdigit():
            return None
        
        return nome
    
    def adicionar_coluna(self, nome_coluna, tipo='TEXT'):
        try:
            colunas_existentes = self.obter_colunas_tabela()
            if nome_coluna in colunas_existentes:
                return True
            
            if len(colunas_existentes) >= self.max_colunas:
                return False
            
            sql = f"ALTER TABLE produtos ADD COLUMN {nome_coluna} {tipo}"
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            return False
    
    def ler_excel_dinamico(self, arquivo_excel):
        try:
            df = pd.read_excel(arquivo_excel, header=None)
            if len(df) == 0:
                return None, None
            
            cabecalhos = df.iloc[0].fillna('').astype(str).tolist()
            
            colunas_mapeadas = {}
            colunas_extras = []
            
            for i, cab in enumerate(cabecalhos):
                if cab and cab.strip() and cab.lower() != 'nan':
                    nome_norm = self.normalizar_nome_coluna(cab)
                    if nome_norm:
                        colunas_mapeadas[i] = nome_norm
                    else:
                        colunas_extras.append((i, cab))
                else:
                    colunas_extras.append((i, f"campo_extra_{i}"))
            
            nomes_colunas = []
            for i in range(len(cabecalhos)):
                if i in colunas_mapeadas:
                    nomes_colunas.append(colunas_mapeadas[i])
                else:
                    extra = next((x for x in colunas_extras if x[0] == i), None)
                    if extra:
                        nome_extra = self.normalizar_nome_coluna(extra[1]) or f"campo_extra_{i}"
                        nomes_colunas.append(nome_extra)
                    else:
                        nomes_colunas.append(f"campo_extra_{i}")
            
            # Verificar duplicatas
            seen = {}
            for i, nome in enumerate(nomes_colunas):
                if nome in seen:
                    nomes_colunas[i] = f"{nome}_{seen[nome]}"
                    seen[nome] += 1
                else:
                    seen[nome] = 1
            
            df.columns = nomes_colunas
            df = df.iloc[1:].reset_index(drop=True)
            
            return df, nomes_colunas
        except Exception as e:
            print(f"Erro: {str(e)}")
            return None, None
    
    def preparar_colunas_banco(self, colunas_excel):
        colunas_tabela = self.obter_colunas_tabela()
        for col in colunas_excel:
            if col not in colunas_tabela and col not in ['id']:
                self.adicionar_coluna(col, 'TEXT')
    
    def importar_dados(self, arquivo_excel, cliente='IMPORTACAO', arquivo_nome=None):
        try:
            df, colunas = self.ler_excel_dinamico(arquivo_excel)
            if df is None:
                return False
            
            self.preparar_colunas_banco(colunas)
            colunas_tabela = list(self.obter_colunas_tabela().keys())
            
            self.cursor.execute("DELETE FROM produtos")
            self.conn.commit()
            
            sucesso = 0
            erros = 0
            
            for idx, row in df.iterrows():
                try:
                    doc = str(row.get('doc', '')).strip()
                    codigo = str(row.get('codigo', '') or row.get('item', '')).strip()
                    
                    if not doc or not codigo or doc.lower() in ['nan', ''] or codigo.lower() in ['nan', '']:
                        continue
                    
                    if doc.startswith('=') or codigo.startswith('='):
                        continue
                    
                    valores = {}
                    for col in colunas_tabela:
                        if col in ['id']:
                            continue
                        elif col == 'cliente':
                            valores[col] = cliente
                        elif col == 'arquivo_origem':
                            valores[col] = arquivo_nome or arquivo_excel
                        elif col == 'data_importacao':
                            valores[col] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            valor = row.get(col, '')
                            if pd.isna(valor) or valor is None:
                                valor = ''
                            valores[col] = str(valor).strip()[:1000]
                    
                    colunas_insert = list(valores.keys())
                    placeholders = ['?' for _ in colunas_insert]
                    
                    sql = f"INSERT INTO produtos ({', '.join(colunas_insert)}) VALUES ({', '.join(placeholders)})"
                    self.cursor.execute(sql, list(valores.values()))
                    sucesso += 1
                    
                    if sucesso % 10 == 0:
                        print(f"   ✅ {sucesso}")
                        
                except Exception as e:
                    erros += 1
                    continue
            
            self.conn.commit()
            
            self.cursor.execute("SELECT COUNT(*) FROM produtos")
            total = self.cursor.fetchone()[0]
            
            print(f"\n✅ IMPORTAÇÃO CONCLUÍDA!")
            print(f"   📊 Produtos: {sucesso}")
            print(f"   ❌ Erros: {erros}")
            print(f"   🗃️ Total: {total}")
            print(f"   📋 Colunas: {len(self.obter_colunas_tabela())}")
            
            return True
        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            return False
    
    def fechar(self):
        if self.conn:
            self.conn.close()

def importar_excel_dinamico(arquivo_excel, cliente='IMPORTACAO'):
    importador = ImportadorDinamico()
    try:
        return importador.importar_dados(arquivo_excel, cliente)
    finally:
        importador.fechar()

if __name__ == "__main__":
    print("="*60)
    print(" IMPORTADOR DINÂMICO - SUPORTE ATÉ 100 COLUNAS")
    print("="*60)
    arquivo = "C:/Users/Positivo/Downloads/celio.planilha.xlsx"
    importar_excel_dinamico(arquivo)
