import sqlite3
import pandas as pd
from datetime import datetime

def debug_importacao(arquivo_excel):
    """Debug completo para encontrar o erro de importação"""
    print("=== DEBUG COMPLETO DA IMPORTAÇÃO ===")
    
    # 1. Verificar estrutura da tabela
    print("\n1. ESTRUTURA DA TABELA PRODUTOS:")
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(produtos)")
    colunas_tabela = cursor.fetchall()
    
    print(f"Total de colunas na tabela: {len(colunas_tabela)}")
    for i, col in enumerate(colunas_tabela):
        print(f"  {i:2d}. {col[1]} ({col[2]})")
    
    # 2. Ler Excel e analisar
    print(f"\n2. ANÁLISE DO ARQUIVO: {arquivo_excel}")
    try:
        df = pd.read_excel(arquivo_excel)
        print(f"Linhas no Excel: {len(df)}")
        print(f"Colunas no Excel: {len(df.columns)}")
        
        # Mapeamento de colunas
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
        
        print(f"\n3. MAPEAMENTO DE COLUNAS:")
        for campo, coluna_excel in mapeamento.items():
            if coluna_excel in df.columns:
                print(f"  ✅ {campo} -> {coluna_excel}")
            else:
                print(f"  ❌ {campo} -> {coluna_excel} (NÃO ENCONTRADA)")
        
        # 3. Testar inserção com a primeira linha válida
        print(f"\n4. TESTE DE INSERÇÃO:")
        
        # Encontrar primeira linha válida (não totais)
        for idx, row in df.iterrows():
            if str(row.get('DOC', '')).strip() and str(row.get('ITEM', '')).strip():
                print(f"Testando com linha {idx + 1}:")
                
                # Preparar dados exatamente como o sistema faz
                dados_teste = []
                campos_ordem = [
                    'doc', 'rev', 'codigo', 'ncm', 'quantity', 'um', 'ccy', 'valor', 'total_amount',
                    'descricao', 'marca', 'inner_qty', 'master_qty', 'total_ctns', 'peso',
                    'gross_weight', 'net_weight_pc', 'gross_weight_pc', 'net_weight_ctn',
                    'gross_weight_ctn', 'factory', 'address', 'telephone', 'ean13',
                    'dun14_inner', 'dun14_master', 'length', 'width', 'height', 'cbm',
                    'prc_kg', 'li', 'obs', 'status', 'data_importacao'
                ]
                
                for campo in campos_ordem:
                    if campo == 'data_importacao':
                        dados_teste.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        coluna_excel = mapeamento.get(campo, '')
                        if coluna_excel in df.columns:
                            valor = row.get(coluna_excel, '')
                            if campo in ['quantity', 'total_ctns']:
                                try:
                                    valor = int(float(str(valor))) if str(valor) != '' else 0
                                except:
                                    valor = 0
                            elif campo in ['valor', 'peso', 'gross_weight', 'gross_weight_pc', 'net_weight_ctn', 'gross_weight_ctn', 'length', 'width', 'height', 'cbm']:
                                try:
                                    valor = float(str(valor)) if str(valor) != '' else 0.0
                                except:
                                    valor = 0.0
                            else:
                                valor = str(valor).strip()[:500] if valor else ''
                            
                            dados_teste.append(valor)
                        else:
                            dados_teste.append('')
                
                print(f"  Valores preparados: {len(dados_teste)}")
                print(f"  Campos esperados: {len(campos_ordem)}")
                
                # Verificar se tem algum valor extra
                if len(dados_teste) != len(campos_ordem):
                    print(f"  ❌ ERRO: {len(dados_teste)} valores para {len(campos_ordem)} campos")
                    for i, (campo, valor) in enumerate(zip(campos_ordem, dados_teste)):
                        print(f"    {i:2d}. {campo}: {repr(valor)}")
                else:
                    print(f"  ✅ Quantidade de valores correta")
                
                # Tentar inserir
                try:
                    cursor.execute(f"""
                    INSERT INTO produtos ({', '.join(campos_ordem)})
                    VALUES ({', '.join(['?'] * len(campos_ordem))})
                    """, dados_teste)
                    conn.commit()
                    print(f"  ✅ Inserção bem-sucedida!")
                    
                    # Limpar teste
                    cursor.execute("DELETE FROM produtos")
                    conn.commit()
                    
                except Exception as e:
                    print(f"  ❌ Erro na inserção: {str(e)}")
                    print(f"  SQL: INSERT INTO produtos ({', '.join(campos_ordem)}) VALUES ({', '.join(['?'] * len(campos_ordem))})")
                
                break
        
        conn.close()
        
    except Exception as e:
        print(f"Erro ao analisar arquivo: {str(e)}")

if __name__ == "__main__":
    # Testar com o arquivo que está dando erro
    debug_importacao("C:/Users/Positivo/Downloads/celio.planilha.xlsx")
