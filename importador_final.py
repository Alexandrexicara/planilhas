import pandas as pd
import sqlite3
import os
from datetime import datetime
from gerenciar_planilhas import mover_planilha_para_pasta, listar_planilhas

def importar_planilha_completa(arquivo_excel):
    """Importa planilha para banco e salva na pasta planilhas"""
    try:
        print(f"=== Importando Planilha ===")
        print(f"Arquivo: {arquivo_excel}")
        
        # 1. Mover arquivo para pasta planilhas
        arquivo_destino = mover_planilha_para_pasta(arquivo_excel)
        
        # 2. Conectar ao banco
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        # 3. Ler Excel
        df = pd.read_excel(arquivo_destino)
        print(f"Linhas encontradas: {len(df)}")
        
        # 4. Limpar tabela
        cursor.execute("DELETE FROM produtos")
        conn.commit()
        
        # 5. Importar dados
        sucesso = 0
        erros = 0
        
        for idx, row in df.iterrows():
            try:
                # Preparar dados
                dados = [
                    str(row.get('doc', '')).strip(),
                    str(row.get('rev', '')).strip(),
                    str(row.get('codigo', '')).strip(),
                    str(row.get('ncm', '')).strip(),
                    int(float(str(row.get('quantity', 0))) if str(row.get('quantity', 0)) != '' else 0),
                    str(row.get('um', '')).strip(),
                    str(row.get('ccy', '')).strip(),
                    float(str(row.get('valor', 0))) if str(row.get('valor', 0)) != '' else 0.0,
                    str(row.get('total_amount', '')).strip(),
                    str(row.get('descricao', ''))[:500],
                    str(row.get('marca', '')).strip(),
                    str(row.get('inner_qty', '')).strip(),
                    str(row.get('master_qty', '')).strip(),
                    int(float(str(row.get('total_ctns', 0))) if str(row.get('total_ctns', 0)) != '' else 0),
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
                ]
                
                # Inserir no banco
                cursor.execute("""
                INSERT INTO produtos (
                    doc, rev, codigo, ncm, quantity, um, ccy, valor, total_amount,
                    descricao, marca, inner_qty, master_qty, total_ctns, peso,
                    gross_weight, net_weight_pc, gross_weight_pc, net_weight_ctn,
                    gross_weight_ctn, factory, address, telephone, ean13,
                    dun14_inner, dun14_master, length, width, height, cbm,
                    prc_kg, li, obs, status, data_importacao
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, dados)
                
                sucesso += 1
                
                # Progresso
                if sucesso % 10 == 0:
                    print(f"   Importados: {sucesso}")
                    
            except Exception as e:
                erros += 1
                if erros <= 5:  # Mostrar só os primeiros erros
                    print(f"   Erro linha {idx + 1}: {str(e)[:50]}")
        
        # 6. Salvar e mostrar resultado
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        
        print(f"\n=== IMPORTAÇÃO CONCLUÍDA ===")
        print(f"✅ Arquivo salvo em: {arquivo_destino}")
        print(f"✅ Produtos importados: {sucesso}")
        print(f"❌ Erros: {erros}")
        print(f"📊 Total no banco: {total}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERRO GERAL: {str(e)}")
        return False

def mostrar_planilhas_disponiveis():
    """Mostra planilhas disponíveis para importação"""
    print("\n=== PLANILHAS DISPONÍVEIS ===")
    arquivos = listar_planilhas()
    
    if arquivos:
        print("\nPara importar uma planilha:")
        print("importar_planilha_completa('planilhas/nome_do_arquivo.xlsx')")
    else:
        print("Nenhuma planilha encontrada na pasta 'planilhas'")
        print("Cole suas planilhas na pasta 'planilhas' ou use:")
        print("mover_planilha_para_pasta('caminho/da/sua/planilha.xlsx')")

# Teste
if __name__ == "__main__":
    print("=== SISTEMA DE IMPORTAÇÃO COMPLETO ===")
    
    # Mostrar planilhas disponíveis
    mostrar_planilhas_disponiveis()
    
    print("\n=== COMO USAR ===")
    print("1. Para mover planilha para pasta correta:")
    print("   mover_planilha_para_pasta('seu_arquivo.xlsx')")
    print("\n2. Para importar planilha:")
    print("   importar_planilha_completa('planilhas/seu_arquivo.xlsx')")
    print("\n3. Para listar planilhas:")
    print("   mostrar_planilhas_disponiveis()")
