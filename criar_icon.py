from PIL import Image
import os

# Caminho correto do logo
logo_path = "img/Penacho laranja em fundo neutro.png"
output_path = "icon.ico"

try:
    # Abrir a imagem
    img = Image.open(logo_path)
    
    print(f"✓ Imagem carregada: {img.size}, Modo: {img.mode}")
    
    # Redimensionar para 256x256 (tamanho padrão para ícone)
    img = img.resize((256, 256), Image.Resampling.LANCZOS)
    
    # Se tiver fundo transparente, manter. Se não, converter para RGB
    if img.mode == 'RGBA':
        img_rgb = Image.new('RGB', img.size, (255, 255, 255))
        img_rgb.paste(img, mask=img.split()[3])
        img = img_rgb
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Salvar como ICO com vários tamanhos
    img.save(output_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    print(f"✓ Ícone criado com sucesso: {output_path}")
    
except FileNotFoundError:
    print(f"✗ Arquivo não encontrado: {logo_path}")
except Exception as e:
    print(f"✗ Erro ao converter imagem: {e}")
    import traceback
    traceback.print_exc()
