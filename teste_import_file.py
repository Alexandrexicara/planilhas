#!/usr/bin/env python3
import os
import sys

# Redirecionar output para arquivo
log_file = open('teste_import_log.txt', 'w', encoding='utf-8')
sys.stdout = log_file
sys.stderr = log_file

print("=== INICIANDO TESTE ===")

# Deletar banco
if os.path.exists('banco.db'):
    os.remove('banco.db')
    print("Banco deletado")

# Importar
from sistema import importar_planilha, get_colunas_banco, get_connection

print("\n=== CRIANDO CONEXÃO ===")
conn = get_connection()

print("\n=== IMPORTANDO ===")
resultado = importar_planilha('E:/planilhas-teste/celio.planilha.xlsx')

print(f"\n=== RESULTADO: {resultado} ===")

print("\n=== VERIFICANDO DADOS ===")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM produtos")
count = cursor.fetchone()[0]
print(f"Total no banco: {count}")

if count > 0:
    cursor.execute("SELECT * FROM produtos LIMIT 1")
    row = cursor.fetchone()
    print(f"Primeira linha: {row}")

log_file.close()
print("Log salvo em teste_import_log.txt")
