import pandas as pd
import sqlite3
import re
from datetime import datetime
import os

class ImportadorDefinitivo:
    """Importador com suporte a 100+ colunas"""
    
    def __init__(self, db_file='banco.db'):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.max_colunas = 100
        
        self.mapeamento = {
            'picture': 'picture', 'doc': 'doc', 'rev': 'rev', 'item': 'codigo', 'code': 'ncm',
            'quantity': 'quantity', 'um': 'um', 'ccy': 'ccy', 'unit_price_umo': 'valor',
            'total_amount_umo': 'total_amount', 'descricao_portugues_description_portuguese': 'descricao',
            'marca_brand': 'marca', 'inner_quantity': 'inner_qty', 'master_quantity': 'master_qty',
            'total_ctns': 'total_ctns', 'total_net_weight_kg': 'peso', 'total_gross_weight_kg': 'gross_weight',
            'net_weight_pc_g': 'net_weight_pc', 'gross_weight_pc_g': 'gross_weight_pc',
            'net_weight_ctn_kg': 'net_weight_ctn', 'gross_weight_ctn_kg': 'gross_weight_ctn',
            'name_of_factory': 'factory', 'address_of_factory': 'address', 'telephone': 'telephone',
            'ean13': 'ean13', 'dun_14_inner': 'dun14_inner', 'dun_14_master': 'dun14_master',
            'length_ctn': 'length', 'width_ctn': 'width', 'height_ctn': 'height',
            'total_cbm': 'cbm', 'hs_code': 'hs_code', 'prckg': 'prc_kg', 'li': 'li',
            'obs': 'obs', 'status_da_compra': 'status'
        }
    
    def get_colunas_banco(self):
        self.cursor.execute("PRAGMA table_info(produtos)")
        return {col[1]: {'tipo': col[2], 'notnull': col[3], 'default': col[4]} 
                for col in self.cursor.fetchall()}
    
    def normalizar(self, nome):
        if not nome or pd.isna(nome): return None
        nome = str(nome).strip().lower()
        nome = re.sub(r'[^\w\s]', '_', nome)
        nome = re.sub(r'\s+', '_', nome)
        nome = re.sub(r'_+', '_', nome).strip('_')
        
        for padrao, banco in self.mapeamento.items():
            if nome == padrao or nome.replace('_', '') == padrao.replace('_', ''):
                return banco
        
        return nome if nome and not nome.replace('_', '').isdigit() else None
    
    def add_coluna(self, nome, tipo='TEXT'):
        try:
            cols = self.get_colunas_banco()
            if nome in cols: return True
            if len(cols) >= self.max_colunas: return False
            
            self.cursor.execute(f"ALTER TABLE produtos ADD COLUMN {nome} {tipo} DEFAULT ''")
            self.conn.commit()
            return True
        except: return False
    
    def ler_excel(self, arquivo):
        print(f"\n📖 Lendo: {os.path.basename(arquivo)}")
        try:
            df = pd.read_excel(arquivo, header=None)
            if len(df) == 0: return None, None
            
            linha_cab = None
            for idx in range(min(5, len(df))):
                texto = ' '.join(df.iloc[idx].fillna('').astype(str).str.lower().tolist())
                if sum(1 for k in ['doc', 'item', 'code', 'quantity'] if k in texto) >= 3:
                    linha_cab = idx
                    break
            
            if linha_cab is None: linha_cab = 1
            
            cabs = df.iloc[linha_cab].fillna('').astype(str).tolist()
            mapeados = {i: self.normalizar(cab) for i, cab in enumerate(cabs) if self.normalizar(cab)}
            
            nomes = [mapeados.get(i, f"extra_{i}") for i in range(len(cabs))]
            
            # Remover duplicatas
            seen = {}
            for i, n in enumerate(nomes):
                if n in seen:
                    nomes[i] = f"{n}_{seen[n]}"
                    seen[n] += 1
                else:
                    seen[n] = 1
            
            df.columns = nomes
            df = df.iloc[linha_cab + 1:].reset_index(drop=True)
            
            print(f"   ✅ {len(nomes)} colunas, {len(df)} linhas")
            return df, nomes
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None, None
    
    def importar(self, arquivo, cliente='IMPORTADO'):
        print("\n" + "="*60)
        print("🚀 IMPORTAÇÃO DEFINITIVA")
        print("="*60)
        
        df, cols_excel = self.ler_excel(arquivo)
        if df is None: return False
        
        cols_banco = self.get_colunas_banco()
        print(f"📊 Banco: {len(cols_banco)} cols | Excel: {len(cols_excel)} cols")
        
        # Adicionar colunas extras
        for c in cols_excel:
            if c not in cols_banco and not c.startswith('extra_'):
                self.add_coluna(c)
        
        cols_banco = self.get_colunas_banco()
        
        self.cursor.execute("DELETE FROM produtos")
        self.conn.commit()
        
        sucesso = 0
        for idx, row in df.iterrows():
            try:
                doc = str(row.get('doc', '')).strip()
                cod = str(row.get('codigo', '')).strip()
                
                if not doc or not cod or doc.lower() in ['nan', 'doc', ''] or cod.lower() in ['nan', 'item', '']:
                    continue
                if doc.startswith('=') or cod.startswith('='):
                    continue
                
                valores = {}
                for nome, info in cols_banco.items():
                    if nome == 'id': continue
                    
                    if nome == 'cliente': valores[nome] = cliente
                    elif nome == 'arquivo_origem': valores[nome] = arquivo
                    elif nome == 'data_importacao': valores[nome] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    elif nome in cols_excel:
                        v = row.get(nome, '')
                        valores[nome] = str(v).strip()[:1000] if not pd.isna(v) else ''
                    else:
                        valores[nome] = ''
                
                sql = f"INSERT INTO produtos ({', '.join(valores.keys())}) VALUES ({', '.join(['?' for _ in valores])})"
                self.cursor.execute(sql, list(valores.values()))
                sucesso += 1
                
                if sucesso % 10 == 0:
                    print(f"   ✅ {sucesso}...")
                    
            except Exception as e:
                if idx < 3: print(f"   ❌ Erro linha {idx}: {str(e)[:60]}")
                continue
        
        self.conn.commit()
        self.cursor.execute("SELECT COUNT(*) FROM produtos")
        total = self.cursor.fetchone()[0]
        
        print(f"\n✅ CONCLUÍDO: {sucesso} produtos | {len(self.get_colunas_banco())} colunas")
        self.conn.close()
        return True

def importar_excel_definitivo(arquivo, cliente='IMPORTADO'):
    return ImportadorDefinitivo().importar(arquivo, cliente)

if __name__ == "__main__":
    importar_excel_definitivo("C:/Users/Positivo/Downloads/celio.planilha.xlsx")
