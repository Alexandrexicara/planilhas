import pandas as pd
import sqlite3
import os
import shutil
from datetime import datetime

def garantir_pasta_planilhas():
    """Garante que a pasta planilhas existe"""
    pasta = "planilhas"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"Pasta '{pasta}' criada com sucesso!")
    return pasta

def mover_arquivo_para_planilhas(arquivo_origem):
    """Move arquivo Excel para a pasta planilhas"""
    try:
        # Garantir que a pasta existe
        garantir_pasta_planilhas()
        
        # Obter nome do arquivo
        nome_arquivo = os.path.basename(arquivo_origem)
        caminho_destino = os.path.join("planilhas", nome_arquivo)
        
        # Se o arquivo já existe na pasta planilhas, mover com timestamp
        if os.path.exists(caminho_destino):
            nome, ext = os.path.splitext(nome_arquivo)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            novo_nome = f"{nome}_{timestamp}{ext}"
            caminho_destino = os.path.join("planilhas", novo_nome)
        
        # Mover arquivo
        shutil.copy2(arquivo_origem, caminho_destino)
        print(f"Arquivo movido para: {caminho_destino}")
        return caminho_destino
        
    except Exception as e:
        print(f"Erro ao mover arquivo: {str(e)}")
        return arquivo_origem

def importar_excel_para_banco(arquivo_excel):
    """Importa arquivo Excel para o banco de dados existente"""
    try:
        print(f"Importando: {arquivo_excel}")
        
        # Mover arquivo para pasta planilhas
        arquivo_caminho = mover_arquivo_para_planilhas(arquivo_excel)
        
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        # Ler Excel
        df = pd.read_excel(arquivo_caminho)
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
        print(f"   Arquivo salvo em: {arquivo_caminho}")
        print(f"   Sucesso: {sucesso}")
        print(f"   Erros: {erros}")
        print(f"   Total no banco: {total}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        return False

def listar_arquivos_planilhas():
    """Lista todos os arquivos na pasta planilhas"""
    garantir_pasta_planilhas()
    
    try:
        arquivos = []
        for arquivo in os.listdir("planilhas"):
            if arquivo.endswith(('.xlsx', '.xls', '.csv')):
                caminho_completo = os.path.join("planilhas", arquivo)
                tamanho = os.path.getsize(caminho_completo)
                data_mod = datetime.fromtimestamp(os.path.getmtime(caminho_completo))
                arquivos.append({
                    'nome': arquivo,
                    'caminho': caminho_completo,
                    'tamanho': tamanho,
                    'data': data_mod
                })
        
        print(f"\n📁 Arquivos na pasta 'planilhas':")
        print("=" * 60)
        
        if not arquivos:
            print("   Nenhum arquivo encontrado.")
        else:
            for i, arq in enumerate(sorted(arquivos, key=lambda x: x['data'], reverse=True), 1):
                print(f"{i:2d}. {arq['nome']}")
                print(f"    📊 Tamanho: {arq['tamanho']:,} bytes")
                print(f"    📅 Data: {arq['data'].strftime('%d/%m/%Y %H:%M')}")
                print(f"    📂 Caminho: {arq['caminho']}")
                print()
        
        return arquivos
        
    except Exception as e:
        print(f"Erro ao listar arquivos: {str(e)}")
        return []

# Teste
if __name__ == "__main__":
    print("=== Testando Importador com Pasta Planilhas ===")
    
    # Criar pasta se não existir
    garantir_pasta_planilhas()
    
    # Listar arquivos existentes
    listar_arquivos_planilhas()
    
    print("\nPara importar seu arquivo:")
    print("importar_excel_para_banco('caminho_do_seu_arquivo.xlsx')")
    print("\nPara listar arquivos disponíveis:")
    print("listar_arquivos_planilhas()")
