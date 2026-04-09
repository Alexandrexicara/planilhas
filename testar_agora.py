#!/usr/bin/env python3
import sys
import os

# Limpar cache
if os.path.exists('banco.db'):
    os.remove('banco.db')

# Forçar reimport
if 'sistema' in sys.modules:
    del sys.modules['sistema']

from sistema import importar_planilha, get_colunas_banco, contar_produtos

print("=== TESTANDO IMPORTAÇÃO ===")
try:
    resultado = importar_planilha('E:/planilhas-teste/celio.planilha.xlsx')
    print(f"Importados: {resultado}")
    print(f"Total no banco: {contar_produtos()}")
    colunas = list(get_colunas_banco().keys())
    print(f"Colunas criadas ({len(colunas)}): {colunas[:10]}")
except Exception as e:
    print(f"ERRO: {e}")
    import traceback
    traceback.print_exc()

print("=== FIM ===")
input("Pressione Enter para sair...")
