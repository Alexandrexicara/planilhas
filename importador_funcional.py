import pandas as pd
import sqlite3
from datetime import datetime

def importar_excel_para_banco(arquivo_excel):
    """Importa arquivo Excel para o banco de dados existente"""
    try:
        print(f"Importando: {arquivo_excel}")
        
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        # Ler Excel
        df = pd.read_excel(arquivo_excel)
        print(f"Linhas: {len(df)}")
        
        # Limpar tabela
        cursor.execute("DELETE FROM produtos")
        conn.commit()
        
        sucesso = 0
        erros = 0
        
        for idx, row in df.iterrows():
            try:
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
                    str(row.get('doc', '')).strip(),
                    str(row.get('rev', '')).strip(),
                    str(row.get('codigo', '')).strip(),
                    str(row.get('ncm', '')).strip(),
                    int(float(str(row.get('quantity', 0))) if str(row.get('quantity', 0)) != '' else 0,
                    str(row.get('um', '')).strip(),
                    str(row.get('ccy', '')).strip(),
                    float(str(row.get('valor', 0))) if str(row.get('valor', 0)) != '' else 0.0,
                    str(row.get('total_amount', '')).strip(),
                    str(row.get('descricao', ''))[:500],
                    str(row.get('marca', '')).strip(),
                    str(row.get('inner_qty', '')).strip(),
                    str(row.get('master_qty', '')).strip(),
                    int(float(str(row.get('total_ctns', 0))) if str(row.get('total_ctns', 0)) != '' else 0,
                    float(str(row.get('peso', 0))) if str(row.get('peso', 0)) != '' else 0.0,
                    float(str(row.get('gross_weight', 0))) if str(row.get('gross_weight', 0)) != '' else 0.0,
                    str(row.get('net_weight_pc', '')).strip(),
                    float(str(row.get('gross_weight_pc', 0))) if str(row.get('gross_weight_pc', 0)) != '' else 0.0,
                    float(str(row.get('net_weight_ctn', 0))) if str(row.get('net_weight_ctn', 0)) != '' else 0.0,
                    float(str(row.get('gross_weight_ctn', 0))) if str(row.get('gross_weight_ctn', 0)) != '' else 0.0,
                    str(row.get('factory', '')).strip(),
                    str(row.get('address', '')).strip(),
                    str(row.get('telephone', '')).strip(),
                    str(row.get('ean13', '')).strip(),
                    str(row.get('dun14_inner', '')).strip(),
                    str(row.get('dun14_master', '')).strip(),
                    float(str(row.get('length', 0))) if str(row.get('length', 0)) != '' else 0.0,
                    float(str(row.get('width', 0))) if str(row.get('width', 0)) != '' else 0.0,
                    float(str(row.get('height', 0))) if str(row.get('height', 0)) != '' else 0.0,
                    float(str(row.get('cbm', 0))) if str(row.get('cbm', 0)) != '' else 0.0,
                    str(row.get('prc_kg', '')).strip(),
                    str(row.get('li', '')).strip(),
                    str(row.get('obs', '')).strip(),
                    str(row.get('status', '')).strip(),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ))
                
                sucesso += 1
                if sucesso % 10 == 0:
                    print(f"   Importados: {sucesso}")
                    
            except Exception as e:
                erros += 1
                print(f"   Erro linha {idx + 1}: {str(e)[:30]}")
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        
        print(f"\nConcluido!")
        print(f"   Sucesso: {sucesso}")
        print(f"   Erros: {erros}")
        print(f"   Total no banco: {total}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        return False

# Teste
if __name__ == "__main__":
    print("Testando importador funcional...")
    
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO produtos (
            doc, rev, codigo, ncm, quantity, um, ccy, valor, total_amount,
            descricao, marca, inner_qty, master_qty, total_ctns, peso,
            gross_weight, net_weight_pc, gross_weight_pc, net_weight_ctn,
            gross_weight_ctn, factory, address, telephone, ean13,
            dun14_inner, dun14_master, length, width, height, cbm,
            prc_kg, li, obs, status, data_importacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            '5266', '1', 'TESTE', 'PAP01', 100, 'PC', 'USD', 10.50, '1050.00',
            'PRODUTO TESTE PAPEL DE PAREDE', 'WESTERN HOME', '', '30', 4, 50.0, 52.0,
            '', 0.5, 12.5, 13.0, 'FABRICA TESTE', 'CIDADE TESTE', '',
            '1234567890123', '', '12345678901234', 25.0, 20.0, 30.0, 15.0,
            '=J1/P1', 'SEM LI', 'TESTE OK', 'ATIVO',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        print(f"Teste OK! Total: {total}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro teste: {str(e)}")
    
    print("\nPara importar seu arquivo:")
    print("importar_excel_para_banco('seu_arquivo.xlsx')")
