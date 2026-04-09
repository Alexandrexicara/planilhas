import os
import zipfile
import io
from openpyxl import load_workbook
from PIL import Image as PILImage

def extrair_imagens_completas(caminho_arquivo, cliente):
    """Extrai TODAS as imagens possíveis do Excel"""
    print(f"=== EXTRAÇÃO COMPLETA DE IMAGENS ===")
    print(f"Arquivo: {caminho_arquivo}")
    print(f"Cliente: {cliente}")
    
    # Criar pasta para o cliente
    pasta_cliente = os.path.join("imagens", cliente)
    if not os.path.exists(pasta_cliente):
        os.makedirs(pasta_cliente)
    
    imagens_encontradas = []
    
    # Método 1: Extração do ZIP (mais completo)
    try:
        print("\n1. Buscando no ZIP do Excel...")
        with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
            todos_arquivos = zip_ref.namelist()
            print(f"Total arquivos no ZIP: {len(todos_arquivos)}")
            
            # Procurar em TODAS as pastas possíveis
            pastas_busca = ['xl/media/', 'xl/drawings/', 'xl/charts/', 'xl/worksheets/']
            todos_arquivos_imagem = []
            
            for pasta in pastas_busca:
                arquivos_pasta = [f for f in todos_arquivos if f.startswith(pasta)]
                print(f"Arquivos em {pasta}: {len(arquivos_pasta)}")
                
                # Procurar imagens em várias extensões
                extensoes = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.emf', '.wmf']
                for ext in extensoes:
                    imagens_ext = [f for f in arquivos_pasta if f.lower().endswith(ext)]
                    todos_arquivos_imagem.extend(imagens_ext)
                    if imagens_ext:
                        print(f"  {ext}: {len(imagens_ext)} arquivos")
                        for img in imagens_ext[:3]:
                            print(f"    - {img}")
            
            print(f"TOTAL de imagens encontradas: {len(todos_arquivos_imagem)}")
            
            # Extrair todas as imagens encontradas
            for i, arquivo_img in enumerate(todos_arquivos_imagem):
                try:
                    # Extrair dados
                    image_data = zip_ref.read(arquivo_img)
                    
                    # Abrir com PIL
                    img = PILImage.open(io.BytesIO(image_data))
                    
                    # Converter para RGB se necessário
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Salvar como JPG
                    nome_arquivo = f"imagem_{i+1:03d}.jpg"
                    caminho_salvo = os.path.join(pasta_cliente, nome_arquivo)
                    
                    img.save(caminho_salvo, 'JPEG', quality=85)
                    imagens_encontradas.append(nome_arquivo)
                    print(f"✅ Imagem salva: {caminho_salvo}")
                    
                except Exception as e:
                    print(f"❌ Erro ao extrair {arquivo_img}: {e}")
                    
    except Exception as e:
        print(f"❌ Erro geral no ZIP: {e}")
    
    # Método 2: openpyxl
    try:
        print("\n2. Buscando com openpyxl...")
        wb = load_workbook(caminho_arquivo)
        ws = wb.active
        
        if hasattr(ws, '_images'):
            print(f"Imagens em ws._images: {len(ws._images)}")
            
            for i, img in enumerate(ws._images):
                try:
                    nome_arquivo = f"imagem_openpyxl_{i+1:03d}.jpg"
                    caminho_salvo = os.path.join(pasta_cliente, nome_arquivo)
                    
                    img.save(caminho_salvo)
                    imagens_encontradas.append(nome_arquivo)
                    print(f"✅ Imagem openpyxl salva: {caminho_salvo}")
                    
                except Exception as e:
                    print(f"❌ Erro ao salvar imagem openpyxl: {e}")
        else:
            print("Nenhuma imagem em ws._images")
            
        wb.close()
        
    except Exception as e:
        print(f"❌ Erro no openpyxl: {e}")
    
    # Método 3: Buscar por arquivos .bin ou .rel
    try:
        print("\n3. Buscando arquivos binários...")
        with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
            arquivos_bin = [f for f in zip_ref.namelist() if f.endswith(('.bin', '.rel', '.xml'))]
            print(f"Arquivos .bin/.rel/.xml: {len(arquivos_bin)}")
            
            # Procurar por referências a imagens nos XMLs
            for arquivo in arquivos_bin:
                if arquivo.endswith('.xml') and 'drawing' in arquivo.lower():
                    try:
                        xml_content = zip_ref.read(arquivo).decode('utf-8')
                        if 'image' in xml_content.lower():
                            print(f"🔍 Possível referência de imagem em: {arquivo}")
                    except:
                        pass
                        
    except Exception as e:
        print(f"❌ Erro na busca binária: {e}")
    
    print(f"\n=== RESUMO FINAL ===")
    print(f"✅ Total de imagens extraídas: {len(imagens_encontradas)}")
    print(f"📁 Pasta: {pasta_cliente}")
    
    if imagens_encontradas:
        print("📋 Imagens salvas:")
        for img in imagens_encontradas:
            print(f"  - {img}")
    else:
        print("❌ Nenhuma imagem encontrada em nenhum método!")
    
    return imagens_encontradas

if __name__ == "__main__":
    # Testar com os arquivos
    arquivos_teste = [
        "E:/planilhas-teste/celio.planilha.xlsx",
        "E:/planilhas-teste/05-03-2026 - 25-608_ESTUDO_250503 - COM LI ANP.xlsx"
    ]
    
    for arquivo in arquivos_teste:
        if os.path.exists(arquivo):
            print(f"\n{'='*60}")
            cliente = os.path.basename(arquivo).replace('.xlsx', '').replace('.xls', '')
            extrair_imagens_completas(arquivo, cliente)
