import pandas as pd
import sqlite3
from datetime import datetime

def importar_produtos_excel(arquivo_excel):
    """Importa produtos do Excel para o banco existente"""
    try:
        print(f"Importando de: {arquivo_excel}")
        
        # Conectar ao banco
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        # Ler Excel
        df = pd.read_excel(arquivo_excel)
        print(f"Linhas encontradas: {len(df)}")
        
        # Limpar tabela
        cursor.execute("DELETE FROM produtos")
        conn.commit()
        
        # Importar linha por linha
        for idx, row in df.iterrows():
            try:
                # Dados básicos
                dados = {
                    'doc': str(row.get('doc', '')).strip(),
                    'rev': str(row.get('rev', '')).strip(),
                    'codigo': str(row.get('codigo', '')).strip(),
                    'ncm': str(row.get('ncm', '')).strip(),
                    'quantity': int(float(str(row.get('quantity', 0))) if str(row.get('quantity', 0)) != '' else 0,
                    'um': str(row.get('um', '')).strip(),
                    'ccy': str(row.get('ccy', '')).strip(),
                    'valor': float(str(row.get('valor', 0))) if str(row.get('valor', 0)) != '' else 0.0,
                    'total_amount': str(row.get('total_amount', '')).strip(),
                    'descricao': str(row.get('descricao', ''))[:500],
                    'marca': str(row.get('marca', '')).strip(),
                    'inner_qty': str(row.get('inner_qty', '')).strip(),
                    'master_qty': str(row.get('master_qty', '')).strip(),
                    'total_ctns': int(float(str(row.get('total_ctns', 0))) if str(row.get('total_ctns', 0)) != '' else 0,
                    'peso': float(str(row.get('peso', 0))) if str(row.get('peso', 0)) != '' else 0.0,
                    'gross_weight': float(str(row.get('gross_weight', 0))) if str(row.get('gross_weight', 0)) != '' else 0.0,
                    'net_weight_pc': str(row.get('net_weight_pc', '')).strip(),
                    'gross_weight_pc': float(str(row.get('gross_weight_pc', 0))) if str(row.get('gross_weight_pc', 0)) != '' else 0.0,
                    'net_weight_ctn': float(str(row.get('net_weight_ctn', 0))) if str(row.get('net_weight_ctn', 0)) != '' else 0.0,
                    'gross_weight_ctn': float(str(row.get('gross_weight_ctn', 0))) if str(row.get('gross_weight_ctn', 0)) != '' else 0.0,
                    'factory': str(row.get('factory', '')).strip(),
                    'address': str(row.get('address', '')).strip(),
                    'telephone': str(row.get('telephone', '')).strip(),
                    'ean13': str(row.get('ean13', '')).strip(),
                    'dun14_inner': str(row.get('dun14_inner', '')).strip(),
                    'dun14_master': str(row.get('dun14_master', '')).strip(),
                    'length': float(str(row.get('length', 0))) if str(row.get('length', 0)) != '' else 0.0,
                    'width': float(str(row.get('width', 0))) if str(row.get('width', 0)) != '' else 0.0,
                    'height': float(str(row.get('height', 0))) if str(row.get('height', 0)) != '' else 0.0,
                    'cbm': float(str(row.get('cbm', 0))) if str(row.get('cbm', 0)) != '' else 0.0,
                    'prc_kg': str(row.get('prc_kg', '')).strip(),
                    'li': str(row.get('li', '')).strip(),
                    'obs': str(row.get('obs', '')).strip(),
                    'status': str(row.get('status', '')).strip()
                }
                
                # Inserir usando SQL dinâmico para evitar problemas de colunas
                colunas = list(dados.keys())
                valores = list(dados.values())
                valores.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  # data_importacao
                
                # Montar SQL
                sql = f"""
                INSERT INTO produtos ({', '.join(colunas)}, data_importacao)
                VALUES ({', '.join(['?'] * (len(colunas) + 1))})
                """
                
                cursor.execute(sql, valores)
                
                if (idx + 1) % 10 == 0:
                    print(f"   Importados: {idx + 1} produtos")
                    
            except Exception as e:
                print(f"   Erro linha {idx + 1}: {str(e)[:50]}")
                continue
        
        conn.commit()
        
        # Verificar resultado
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        print(f"\nConcluído! Total importado: {total}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erro geral: {str(e)}")
        return False

# Teste com dados simulados
if __name__ == "__main__":
    print("Testando importador ultra simples...")
    
    # Teste básico
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        # Inserir um produto de teste
        cursor.execute("""
        INSERT INTO produtos (
            doc, rev, codigo, ncm, quantity, um, ccy, valor, total_amount,
            descricao, marca, inner_qty, master_qty, total_ctns, peso,
            gross_weight, net_weight_pc, gross_weight_pc, net_weight_ctn,
            gross_weight_ctn, factory, address, telephone, ean13,
            dun14_inner, dun14_master, length, width, height, cbm,
            prc_kg, li, obs, status, data_importacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            '5266', '1', '1', 'PAP01', 3600, 'PC', 'USD', 0.56, '2016.00',
            'PAPEL DE PAREDE ADESIVO ESTAMPA ESTRELADO 5 METROS',
            'WESTERN HOME', '', '30', 120, 1060.2, 1092, '', 0.392,
            8.835, 9.1, 'YOUNGCOM HONGKONG LIMITED', 'YIWU,CHINA', '', '7897186068084',
            '', '57897186068089', 25, 20.5, 47, 2.8905, '=J3/P3', 'SEM LI',
            'NCM OK', 'REPOSIÇÃO', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        print(f"Teste OK! Produtos no banco: {total}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro no teste: {str(e)}")
    
    print("\nPara usar com seu arquivo Excel:")
    print("importar_produtos_excel('seu_arquivo.xlsx')")
