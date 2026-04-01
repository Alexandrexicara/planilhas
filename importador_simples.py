import pandas as pd
import sqlite3
import re
from datetime import datetime

def importar_dados_simples(arquivo_excel):
    """Importa dados simples sem recriar tabela"""
    try:
        print(f"Importando dados de: {arquivo_excel}")
        
        # Conectar ao banco existente
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        # Ler arquivo Excel
        df = pd.read_excel(arquivo_excel)
        print(f"Encontradas {len(df)} linhas no arquivo")
        
        # Limpar tabela antes de importar
        cursor.execute("DELETE FROM produtos")
        conn.commit()
        
        produtos_importados = 0
        erros = 0
        
        for index, row in df.iterrows():
            try:
                # Preparar dados básicos
                doc = str(row.get('doc', '')).strip()
                rev = str(row.get('rev', '')).strip()
                codigo = str(row.get('codigo', '')).strip()
                ncm = str(row.get('ncm', '')).strip()
                
                # Converter números
                try:
                    quantity = int(float(str(row.get('quantity', 0)).replace(',', '.')))
                except:
                    quantity = 0
                
                try:
                    valor = float(str(row.get('valor', 0)).replace(',', '.'))
                except:
                    valor = 0.0
                
                try:
                    total_ctns = int(float(str(row.get('total_ctns', 0)).replace(',', '.')))
                except:
                    total_ctns = 0
                
                # Textos longos
                descricao = str(row.get('descricao', ''))
                if len(descricao) > 500:
                    descricao = descricao[:500] + "..."
                
                marca = str(row.get('marca', '')).strip()
                factory = str(row.get('factory', '')).strip()
                address = str(row.get('address', '')).strip()
                status = str(row.get('status', '')).strip()
                
                # Inserir com campos básicos
                cursor.execute("""
                INSERT INTO produtos (
                    doc, rev, codigo, ncm, quantity, um, ccy, valor, total_amount,
                    descricao, marca, inner_qty, master_qty, total_ctns, peso,
                    gross_weight, net_weight_pc, gross_weight_pc, net_weight_ctn,
                    gross_weight_ctn, factory, address, telephone, ean13,
                    dun14_inner, dun14_master, length, width, height, cbm,
                    prc_kg, li, obs, status, data_importacao
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    doc, rev, codigo, ncm, quantity,
                    str(row.get('um', '')).strip(),
                    str(row.get('ccy', '')).strip(),
                    valor,
                    str(row.get('total_amount', '')).strip(),
                    descricao,
                    marca,
                    str(row.get('inner_qty', '')).strip(),
                    str(row.get('master_qty', '')).strip(),
                    total_ctns,
                    str(row.get('peso', 0)),
                    str(row.get('gross_weight', 0)),
                    str(row.get('net_weight_pc', '')).strip(),
                    str(row.get('gross_weight_pc', 0)),
                    str(row.get('net_weight_ctn', 0)),
                    str(row.get('gross_weight_ctn', 0)),
                    factory,
                    address,
                    str(row.get('telephone', '')).strip(),
                    str(row.get('ean13', '')).strip(),
                    str(row.get('dun14_inner', '')).strip(),
                    str(row.get('dun14_master', '')).strip(),
                    str(row.get('length', 0)),
                    str(row.get('width', 0)),
                    str(row.get('height', 0)),
                    str(row.get('cbm', 0)),
                    str(row.get('prc_kg', '')).strip(),
                    str(row.get('li', '')).strip(),
                    str(row.get('obs', '')).strip(),
                    status,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ))
                
                produtos_importados += 1
                
                # Mostrar progresso
                if produtos_importados % 10 == 0:
                    print(f"   Importados: {produtos_importados} produtos")
            
            except Exception as e:
                erros += 1
                print(f"   Erro na linha {index + 1}: {str(e)[:100]}")
                continue
        
        conn.commit()
        
        print(f"\nImportacao concluida!")
        print(f"   Produtos importados: {produtos_importados}")
        print(f"   Erros: {erros}")
        
        # Verificar
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        print(f"   Total no banco: {total}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erro na importacao: {str(e)}")
        return False

def testar_importacao():
    """Testa com dados simulados"""
    print("Testando importacao simples...")
    
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
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        # Limpar tabela
        cursor.execute("DELETE FROM produtos")
        conn.commit()
        
        # Inserir dados de teste
        for dados in dados_teste:
            cursor.execute("""
            INSERT INTO produtos (
                doc, rev, codigo, ncm, quantity, um, ccy, valor, total_amount,
                descricao, marca, inner_qty, master_qty, total_ctns, peso,
                gross_weight, net_weight_pc, gross_weight_pc, net_weight_ctn,
                gross_weight_ctn, factory, address, telephone, ean13,
                dun14_inner, dun14_master, length, width, height, cbm,
                prc_kg, li, obs, status, data_importacao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        
        conn.commit()
        
        print("Dados de teste inseridos com sucesso!")
        
        # Verificar
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        print(f"Total de produtos no banco: {total}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro no teste: {str(e)}")

if __name__ == "__main__":
    # Testar primeiro
    testar_importacao()
    
    print("\n" + "="*50)
    print("Para importar seu arquivo Excel, use:")
    print("importar_dados_simples('seu_arquivo.xlsx')")
    print("="*50)
