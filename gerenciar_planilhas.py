import os
import shutil
from datetime import datetime

def criar_pasta_planilhas():
    """Cria a pasta planilhas se não existir"""
    pasta = "planilhas"
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        print(f"Pasta '{pasta}' criada!")
    else:
        print(f"Pasta '{pasta}' já existe.")
    return pasta

def mover_planilha_para_pasta(arquivo_origem):
    """Move planilha para pasta planilhas"""
    try:
        criar_pasta_planilhas()
        
        nome = os.path.basename(arquivo_origem)
        destino = os.path.join("planilhas", nome)
        
        # Se já existir, adiciona timestamp
        if os.path.exists(destino):
            nome_base, ext = os.path.splitext(nome)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome = f"{nome_base}_{timestamp}{ext}"
            destino = os.path.join("planilhas", nome)
        
        shutil.copy2(arquivo_origem, destino)
        print(f"Planilha salva em: {destino}")
        return destino
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        return arquivo_origem

def listar_planilhas():
    """Lista arquivos na pasta planilhas"""
    criar_pasta_planilhas()
    
    try:
        arquivos = [f for f in os.listdir("planilhas") 
                   if f.endswith(('.xlsx', '.xls', '.csv'))]
        
        print(f"\nPlanilhas na pasta:")
        print("-" * 40)
        
        if not arquivos:
            print("Nenhuma planilha encontrada.")
        else:
            for i, arq in enumerate(sorted(arquivos), 1):
                caminho = os.path.join("planilhas", arq)
                tamanho = os.path.getsize(caminho)
                print(f"{i}. {arq} ({tamanho:,} bytes)")
        
        return arquivos
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        return []

# Teste
if __name__ == "__main__":
    print("=== Gerenciador de Pasta Planilhas ===")
    
    criar_pasta_planilhas()
    listar_planilhas()
    
    print("\nPara mover sua planilha:")
    print("mover_planilha_para_pasta('seu_arquivo.xlsx')")
    print("\nPara listar planilhas:")
    print("listar_planilhas()")
