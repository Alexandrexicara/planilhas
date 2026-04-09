#!/usr/bin/env python3
# Teste simples de importação

import os
import sys

# Deletar banco
if os.path.exists('banco.db'):
    os.remove('banco.db')
    print("✅ Banco deletado")

# Importar e testar
from sistema import importar_planilha, get_colunas_banco, get_connection

print("\n=== CRIANDO BANCO ===")
conn = get_connection()

print("\n=== IMPORTANDO ===")
resultado = importar_planilha('E:/planilhas-teste/celio.planilha.xlsx')
print(f"\n=== RESULTADO: {resultado} produtos ===")

print("\n=== COLUNAS ===")
colunas = get_colunas_banco()
print(f"Total: {len(colunas)}")
for c in list(colunas.keys())[:15]:
    print(f"  - {c}")

print("\n=== VERIFICAR DADOS ===")
cursor = conn.cursor()
cursor.execute("SELECT * FROM produtos LIMIT 1")
dados = cursor.fetchone()
if dados:
    print(f"Dados encontrados: {dados}")
else:
    print("NENHUM DADO ENCONTRADO!")
