import pandas as pd
import sqlite3
from datetime import datetime

def importar_excel_corrigido(arquivo_excel):
    """Importa Excel com colunas Unnamed e dados na primeira linha"""
    try:
        print("=== IMPORTADOR CORRIGIDO PARA EXCEL COM COLUNAS UNNAMED ===")
        print(f"Arquivo: {arquivo_excel}")
        
        # Ler Excel
        df = pd.read_excel(arquivo_excel)
        print(f"Linhas: {len(df)}, Colunas: {len(df.columns)}")
        
        # A primeira linha contém os cabeçalhos reais
        if len(df) > 0:
            cabecalhos_reais = df.iloc[0].fillna('').astype(str)
            dados_reais = df.iloc[1:].copy()  # Pular linha de cabeçalhos
            
            # Renomear colunas com os cabeçalhos reais
            for i, coluna in enumerate(df.columns):
                if i < len(cabecalhos_reais):
                    novo_nome = cabecalhos_reais.iloc[i]
                    if novo_nome and novo_nome != 'nan':
                        dados_reais = dados_reais.rename(columns={coluna: novo_nome})
            
            print(f"\nCabeçalhos encontrados:")
            for i, cabecalho in enumerate(cabecalhos_reais):
                if cabecalho and cabecalho != 'nan':
                    print(f"  {i}: {cabecalho}")
            
            # Mapeamento corrigido
            mapeamento = {
                'codigo': 'ITEM',
                'descricao': 'DESCRIÇÃO PORTUGUES (DESCRIPTION PORTUGUESE)',
                'peso': 'TOTAL NET WEIGHT( kg )',
                'valor': 'UNIT PRICE UMO',
                'ncm': 'CODE',
                'doc': 'DOC',
                'rev': 'REV',
                'quantity': 'QUANTITY',
                'um': 'UM',
                'ccy': 'CCY',
                'total_amount': 'TOTAL AMOUNT UMO',
                'marca': 'MARCA (BRAND)',
                'inner_qty': 'INNER QUANTITY',
                'master_qty': 'MASTER QUANTITY',
                'total_ctns': 'TOTAL CTNS',
                'gross_weight': 'TOTAL GROSS WEIGHT( kg )',
                'net_weight_pc': 'NET WEIGHT / PC( g )',
                'gross_weight_pc': 'GROSS WEIGHT / PC( g )',
                'net_weight_ctn': 'NET WEIGHT / CTN( kg )',
                'gross_weight_ctn': 'GROSS WEIGHT / CTN( kg )',
                'factory': 'NAME OF FACTORY',
                'address': 'ADDRESS OF FACTORY',
                'telephone': 'TELEPHONE',
                'ean13': 'EAN13',
                'dun14_inner': 'DUN-14 INNER',
                'dun14_master': 'DUN-14 MASTER',
                'length': 'LENGTH CTN',
                'width': 'WIDTH CTN',
                'height': 'HEIGHT CTN',
                'cbm': 'TOTAL CBM',
                'prc_kg': 'PRC/KG',
                'li': 'LI',
                'obs': 'OBS',
                'status': 'STATUS DA COMPRA'
            }
            
            # Conectar ao banco
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            
            # Limpar tabela
            cursor.execute("DELETE FROM produtos")
            conn.commit()
            
            sucesso = 0
            erros = 0
            
            # Importar dados reais
            for idx, (index, row) in enumerate(dados_reais.iterrows()):
                try:
                    # Pular linhas vazias ou de totais
                    doc = str(row.get('DOC', '')).strip()
                    codigo = str(row.get('ITEM', '')).strip()
                    
                    if not doc or not codigo or doc.lower() == 'nan' or codigo.lower() == 'nan':
                        continue
                    
                    # Preparar dados
                    dados = []
                    campos_ordem = [
                        'cliente', 'arquivo_origem', 'doc', 'rev', 'codigo', 'ncm', 'quantity', 'um', 'ccy', 'valor', 'total_amount',
                        'descricao', 'marca', 'inner_qty', 'master_qty', 'total_ctns', 'peso',
                        'gross_weight', 'net_weight_pc', 'gross_weight_pc', 'net_weight_ctn',
                        'gross_weight_ctn', 'factory', 'address', 'telephone', 'ean13',
                        'dun14_inner', 'dun14_master', 'length', 'width', 'height', 'cbm',
                        'prc_kg', 'li', 'obs', 'status', 'data_importacao'
                    ]
                    
                    for campo in campos_ordem:
                        if campo == 'data_importacao':
                            dados.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                        elif campo == 'cliente':
                            dados.append('IMPORTACAO_EXCEL')  # Cliente padrão
                        elif campo == 'arquivo_origem':
                            dados.append(arquivo_excel)  # Nome do arquivo
                        else:
                            coluna_excel = mapeamento.get(campo, '')
                            valor = row.get(coluna, '')
                            
                            if campo in ['quantity', 'total_ctns']:
                                try:
                                    valor = int(float(str(valor))) if str(valor) != '' and str(valor) != 'nan' else 0
                                except:
                                    valor = 0
                            elif campo in ['valor', 'peso', 'gross_weight', 'gross_weight_pc', 'net_weight_ctn', 'gross_weight_ctn', 'length', 'width', 'height', 'cbm']:
                                try:
                                    valor = float(str(valor)) if str(valor) != '' and str(valor) != 'nan' else 0.0
                                except:
                                    valor = 0.0
                            else:
                                valor = str(valor).strip()[:500] if valor and str(valor) != 'nan' else ''
                            
                            dados.append(valor)
                    
                    # Inserir no banco
                    cursor.execute(f"""
                    INSERT INTO produtos ({', '.join(campos_ordem)})
                    VALUES ({', '.join(['?'] * len(campos_ordem))})
                    """, dados)
                    
                    sucesso += 1
                    if sucesso % 5 == 0:
                        print(f"   Importados: {sucesso}")
                        
                except Exception as e:
                    erros += 1
                    if erros <= 3:
                        print(f"   Erro linha {index}: {str(e)[:50]}")
                    continue
            
            conn.commit()
            
            cursor.execute("SELECT COUNT(*) FROM produtos")
            total = cursor.fetchone()[0]
            
            print(f"\n=== IMPORTAÇÃO CONCLUÍDA ===")
            print(f"✅ Sucesso: {sucesso}")
            print(f"❌ Erros: {erros}")
            print(f"📊 Total no banco: {total}")
            
            conn.close()
            return True
            
    except Exception as e:
        print(f"ERRO GERAL: {str(e)}")
        return False

if __name__ == "__main__":
    importar_excel_corrigido("C:/Users/Positivo/Downloads/celio.planilha.xlsx")
