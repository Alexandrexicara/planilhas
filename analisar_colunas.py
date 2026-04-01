import pandas as pd

def analisar_colunas_excel(arquivo_excel):
    """Analisa os nomes exatos das colunas do Excel"""
    print("=== ANÁLISE EXATA DAS COLUNAS DO EXCEL ===")
    
    try:
        df = pd.read_excel(arquivo_excel)
        
        print(f"\nColunas encontradas ({len(df.columns)}):")
        print("=" * 80)
        
        for i, coluna in enumerate(df.columns):
            print(f"{i:2d}. '{coluna}'")
        
        print(f"\nPrimeiras linhas do Excel:")
        print("=" * 80)
        
        for idx in range(min(3, len(df))):
            print(f"\nLinha {idx + 1}:")
            for coluna in df.columns:
                valor = df.iloc[idx][coluna]
                print(f"  {coluna}: {repr(valor)}")
        
        print(f"\nVerificação de colunas importantes:")
        print("=" * 80)
        
        colunas_importantes = [
            'DOC', 'REV', 'ITEM', 'CODE', 'QUANTITY', 'UM', 'CCY',
            'UNIT PRICE UMO', 'TOTAL AMOUNT UMO', 'DESCRIÇÃO PORTUGUES (DESCRIPTION PORTUGUESE)',
            'MARCA (BRAND)', 'INNER QUANTITY', 'MASTER QUANTITY', 'TOTAL CTNS',
            'TOTAL NET WEIGHT( kg )', 'TOTAL GROSS WEIGHT( kg )',
            'NET WEIGHT / PC( g )', 'GROSS WEIGHT / PC( g )',
            'NET WEIGHT / CTN( kg )', 'GROSS WEIGHT / CTN( kg )',
            'NAME OF FACTORY', 'ADDRESS OF FACTORY', 'TELEPHONE',
            'EAN13', 'DUN-14 INNER', 'DUN-14 MASTER',
            'LENGTH CTN', 'WIDTH CTN', 'HEIGHT CTN', 'TOTAL CBM',
            'PRC/KG', 'LI', 'OBS', 'STATUS DA COMPRA'
        ]
        
        for coluna in colunas_importantes:
            if coluna in df.columns:
                print(f"✅ {coluna}")
            else:
                # Tentar encontrar similar
                encontradas = [c for c in df.columns if coluna.lower() in c.lower() or c.lower() in coluna.lower()]
                if encontradas:
                    print(f"⚠️  {coluna} -> POSSÍVEL: {encontradas}")
                else:
                    print(f"❌ {coluna}")
        
    except Exception as e:
        print(f"Erro ao ler arquivo: {str(e)}")

if __name__ == "__main__":
    analisar_colunas_excel("C:/Users/Positivo/Downloads/celio.planilha.xlsx")
