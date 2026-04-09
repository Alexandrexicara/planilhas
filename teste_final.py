#!/usr/bin/env python3
import sys
import os

# Limpar banco
if os.path.exists('banco.db'):
    os.remove('banco.db')
    print("Banco removido")

# Limpar cache do Python
modulos = [k for k in sys.modules.keys() if 'sistema' in k]
for m in modulos:
    del sys.modules[m]

print("Importando sistema...")
from sistema import importar_planilha, get_colunas_banco, contar_produtos

print("\n=== TESTE DE IMPORTAÇÃO ===")
try:
    resultado = importar_planilha('E:/planilhas-teste/celio.planilha.xlsx')
    print(f"Resultado: {resultado} produtos importados")
    print(f"Total no banco: {contar_produtos()}")
    colunas = list(get_colunas_banco().keys())
    print(f"Colunas ({len(colunas)}): {colunas}")
    
    if resultado > 0:
        print("\n✅ SUCESSO! Importação funcionou!")
    else:
        print("\n❌ FALHA: Nenhum produto importado")
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
