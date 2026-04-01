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
        self.max_colunas = 100  # Limite máximo de colunas
        
    def obter_colunas_tabela(self):
        """Obtém as colunas atuais da tabela produtos"""
        self.cursor.execute("PRAGMA table_info(produtos)")
        colunas = self.cursor.fetchall()
        return {col[1]: col[2] for col in colunas}  # nome: tipo
    
    def normalizar_nome_coluna(self, nome):
        """Normaliza nome de coluna para ser válido no SQLite"""
        # Remover caracteres especiais
        nome = str(nome).strip()
        nome = re.sub(r'[^\w\s]', '', nome)  # Remove caracteres especiais exceto underscore
        nome = re.sub(r'\s+', '_', nome)      # Substitui espaços por underscore
        nome = nome.lower()                    # Minúsculas
        
        # Limitar tamanho
        if len(nome) > 50:
            nome = nome[:50]
        
        # Se começar com número, adicionar prefixo
        if nome and nome[0].isdigit():
            nome = 'campo_' + nome
            
        return nome if nome else 'campo_vazio'
    
    def adicionar_coluna(self, nome_coluna, tipo='TEXT'):
        """Adiciona uma nova coluna à tabela"""
        try:
            # Verificar se já existe
            colunas_existentes = self.obter_colunas_tabela()
            if nome_coluna in colunas_existentes:
                return True
            
            # Adicionar coluna
            sql = f"ALTER TABLE produtos ADD COLUMN {nome_coluna} {tipo}"
            self.cursor.execute(sql)
            self.conn.commit()
            print(f"   ✅ Coluna adicionada: {nome_coluna}")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao adicionar coluna {nome_coluna}: {str(e)}")
            return False
    
    def ler_excel_dinamico(self, arquivo_excel):
        """Lê Excel detectando cabeçalhos na primeira linha"""
        try:
            # Ler Excel sem cabeçalhos
            df = pd.read_excel(arquivo_excel, header=None)
            
            if len(df) == 0:
                return None, None
            
            # Primeira linha contém os nomes das colunas
            cabecalhos = df.iloc[0].fillna('').astype(str).tolist()
            
            # Normalizar nomes das colunas
            cabecalhos_normalizados = []
            for i, cab in enumerate(cabecalhos):
                if cab and cab.strip() and cab.lower() != 'nan':
                    nome_norm = self.normalizar_nome_coluna(cab)
                else:
                    nome_norm = f"coluna_{i}"
                cabecalhos_normalizados.append(nome_norm)
            
            # Renomear colunas
            df.columns = cabecalhos_normalizados
            
            # Remover primeira linha (cabeçalhos)
            df = df.iloc[1:].reset_index(drop=True)
            
            return df, cabecalhos_normalizados
            
        except Exception as e:
            print(f"Erro ao ler Excel: {str(e)}")
            return None, None
    
    def preparar_colunas_banco(self, colunas_excel):
        """Prepara o banco para receber todas as colunas do Excel"""
        print(f"\n📊 Preparando banco de dados...")
        
        colunas_tabela = self.obter_colunas_tabela()
        print(f"   Colunas na tabela: {len(colunas_tabela)}")
        print(f"   Colunas no Excel: {len(colunas_excel)}")
        
        colunas_adicionadas = 0
        colunas_extras = []
        
        for col in colunas_excel:
            if col not in colunas_tabela:
                # É uma coluna nova
                if len(colunas_tabela) + colunas_adicionadas < self.max_colunas:
                    if self.adicionar_coluna(col, 'TEXT'):
                        colunas_adicionadas += 1
                        colunas_extras.append(col)
                else:
                    print(f"   ⚠️ Limite de {self.max_colunas} colunas atingido. Ignorando: {col}")
        
        print(f"   ✅ {colunas_adicionadas} colunas novas adicionadas")
        return colunas_extras
    
    def importar_dados(self, arquivo_excel, cliente='IMPORTACAO', arquivo_nome=None):
        """Importa dados do Excel para o banco"""
        try:
            print(f"\n🚀 Iniciando importação dinâmica...")
            print(f"📁 Arquivo: {arquivo_excel}")
            
            # Ler Excel
            df, colunas = self.ler_excel_dinamico(arquivo_excel)
            if df is None:
                print("❌ Erro ao ler Excel")
                return False
            
            print(f"📋 {len(colunas)} colunas detectadas: {', '.join(colunas[:10])}{'...' if len(colunas) > 10 else ''}")
            
            # Preparar banco (adicionar colunas extras)
            colunas_extras = self.preparar_colunas_banco(colunas)
            
            # Atualizar lista de colunas após adições
            colunas_tabela = list(self.obter_colunas_tabela().keys())
            
            # Limpar tabela anterior (opcional - comentar se quiser manter dados)
            self.cursor.execute("DELETE FROM produtos")
            self.conn.commit()
            
            # Importar dados
            sucesso = 0
            erros = 0
            
            for idx, row in df.iterrows():
                try:
                    # Verificar se é linha válida (tem código ou doc)
                    doc = str(row.get('doc', '')).strip()
                    codigo = str(row.get('item', '')).strip() or str(row.get('codigo', '')).strip()
                    
                    if not doc or not codigo or doc.lower() == 'nan' or codigo.lower() == 'nan':
                        continue
                    
                    # Preparar valores
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
                            # Buscar valor no Excel
                            valor = row.get(col, '')
                            if pd.isna(valor):
                                valor = ''
                            valores[col] = str(valor).strip()[:1000]  # Limitar tamanho
                    
                    # Construir SQL dinâmico
                    colunas_insert = list(valores.keys())
                    placeholders = ['?' for _ in colunas_insert]
                    
                    sql = f"INSERT INTO produtos ({', '.join(colunas_insert)}) VALUES ({', '.join(placeholders)})"
                    
                    self.cursor.execute(sql, list(valores.values()))
                    sucesso += 1
                    
                    if sucesso % 10 == 0:
                        print(f"   📦 Importados: {sucesso}")
                        
                except Exception as e:
                    erros += 1
                    if erros <= 3:
                        print(f"   ❌ Erro linha {idx + 2}: {str(e)[:60]}")
                    continue
            
            self.conn.commit()
            
            # Verificar total
            self.cursor.execute("SELECT COUNT(*) FROM produtos")
            total = self.cursor.fetchone()[0]
            
            print(f"\n✅ IMPORTAÇÃO CONCLUÍDA!")
            print(f"   📊 Produtos importados: {sucesso}")
            print(f"   ❌ Erros: {erros}")
            print(f"   🗃️ Total no banco: {total}")
            print(f"   📋 Colunas na tabela: {len(self.obter_colunas_tabela())}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ ERRO GERAL: {str(e)}")
            return False
    
    def fechar(self):
        """Fecha conexão com banco"""
        if self.conn:
            self.conn.close()

def importar_excel_dinamico(arquivo_excel, cliente='IMPORTACAO'):
    """Função principal de importação"""
    importador = ImportadorDinamico()
    try:
        resultado = importador.importar_dados(arquivo_excel, cliente)
        return resultado
    finally:
        importador.fechar()

# Teste
if __name__ == "__main__":
    print("=== IMPORTADOR DINÂMICO COM SUPORTE A COLUNAS EXTRAS ===")
    print("Este importador detecta automaticamente todas as colunas do Excel")
    print("e cria as colunas necessárias no banco de dados.\n")
    
    # Teste com o arquivo
    arquivo = "C:/Users/Positivo/Downloads/celio.planilha.xlsx"
    importar_excel_dinamico(arquivo)
