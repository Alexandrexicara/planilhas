#!/usr/bin/env python3
import os, sys, io

# Capturar output
output = io.StringIO()
sys.stdout = output
sys.stderr = output

try:
    if os.path.exists('banco.db'):
        os.remove('banco.db')
    
    # Forçar recarregar
    for m in list(sys.modules.keys()):
        if 'sistema' in m:
            del sys.modules[m]
    
    from sistema import importar_planilha, contar_produtos, get_colunas_banco
    
    print("=== TESTE ===")
    r = importar_planilha('E:/planilhas-teste/celio.planilha.xlsx')
    print(f"Importados: {r}")
    print(f"Total: {contar_produtos()}")
    print(f"Colunas: {list(get_colunas_banco().keys())}")
    
except Exception as e:
    import traceback
    print(f"ERRO: {e}")
    traceback.print_exc()

# Salvar output
with open('resultado_teste.txt', 'w', encoding='utf-8') as f:
    f.write(output.getvalue())

print("\nResultado salvo em resultado_teste.txt")
