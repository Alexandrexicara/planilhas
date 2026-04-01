import pandas as pd
import sqlite3

# Ler Excel
df = pd.read_excel("C:/Users/Positivo/Downloads/celio.planilha.xlsx", header=None)

print(f"Total de linhas: {len(df)}")
print(f"Total de colunas: {len(df.columns)}")

# Primeira linha é cabeçalho
cabecalhos = df.iloc[0].fillna('').astype(str).tolist()
print(f"\nCabecalhos: {cabecalhos}")

# Segunda linha é primeiro dado
if len(df) > 1:
    print(f"\nPrimeira linha de dados (linha 1):")
    for i, val in enumerate(df.iloc[1].tolist()):
        if i < 10:  # Mostrar só primeiras
            print(f"  {i}: {cabecalhos[i]} = {repr(val)}")

# Verificar valores de doc e item
if len(df) > 1:
    doc_val = str(df.iloc[1].get(1, '')).strip()  # Coluna 1 = DOC
    item_val = str(df.iloc[1].get(3, '')).strip()  # Coluna 3 = ITEM
    print(f"\nDOC: '{doc_val}'")
    print(f"ITEM: '{item_val}'")
    print(f"DOC válido: {bool(doc_val and doc_val.lower() != 'nan')}")
    print(f"ITEM válido: {bool(item_val and item_val.lower() != 'nan')}")
