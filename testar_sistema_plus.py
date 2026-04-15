"""
Script de teste para verificar se o sistema PLUS está salvando planilhas corretamente
COM TODAS AS 39 COLUNAS
"""
import sqlite3
import os

def testar_banco_plus():
    """Testa se o banco de dados PLUS está configurado corretamente"""
    print("=" * 60)
    print("🧪 TESTANDO SISTEMA PLUS - 39 COLUNAS")
    print("=" * 60)
    
    # Conectar ao banco
    if not os.path.exists('banco_plus.db'):
        print("❌ Banco PLUS não encontrado!")
        return False
    
    conn = sqlite3.connect('banco_plus.db')
    cursor = conn.cursor()
    
    # Verificar se tabela produtos_plus existe
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos_plus'")
        if cursor.fetchone():
            print("✅ Tabela 'produtos_plus' encontrada")
        else:
            print("❌ Tabela 'produtos_plus' não encontrada!")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar tabela: {e}")
        return False
    
    # Verificar colunas da tabela
    try:
        cursor.execute("PRAGMA table_info(produtos_plus)")
        colunas = cursor.fetchall()
        print(f"\n📊 Colunas da tabela produtos_plus: {len(colunas)}")
        
        colunas_esperadas = [
            'id', 'cliente', 'arquivo_origem', 'picture', 'codigo', 'descricao', 'peso', 'valor', 
            'ncm', 'doc', 'rev', 'code', 'quantity', 'um', 'ccy', 'total_amount',
            'marca', 'inner_qty', 'master_qty', 'total_ctns', 'gross_weight',
            'net_weight_pc', 'gross_weight_pc', 'net_weight_ctn', 'gross_weight_ctn',
            'factory', 'address', 'telephone', 'ean13', 'dun14_inner', 'dun14_master',
            'length', 'width', 'height', 'cbm', 'prc_kg', 'li', 'obs', 'status',
            'data_importacao', 'hash_dados'
        ]
        
        colunas_encontradas = [col[1] for col in colunas]
        
        print(f"\n📋 Verificando {len(colunas_esperadas)} colunas esperadas:")
        todas_ok = True
        for coluna in colunas_esperadas:
            if coluna in colunas_encontradas:
                print(f"  ✅ {coluna}")
            else:
                print(f"  ❌ {coluna} (FALTANDO)")
                todas_ok = False
        
        if todas_ok:
            print(f"\n✅ TODAS AS {len(colunas_esperadas)} COLUNAS ESTÃO PRESENTES!")
        else:
            print(f"\n❌ Algumas colunas estão faltando!")
        
    except Exception as e:
        print(f"❌ Erro ao verificar colunas: {e}")
        return False
    
    # Contar registros
    try:
        cursor.execute("SELECT COUNT(*) FROM produtos_plus")
        total = cursor.fetchone()[0]
        print(f"\n📦 Total de produtos cadastrados: {total:,}")
    except Exception as e:
        print(f"❌ Erro ao contar produtos: {e}")
    
    # Verificar últimos registros
    try:
        cursor.execute("""
            SELECT cliente, arquivo_origem, codigo, descricao, data_importacao 
            FROM produtos_plus 
            ORDER BY id DESC 
            LIMIT 5
        """)
        registros = cursor.fetchall()
        
        if registros:
            print(f"\n📋 Últimos 5 registros:")
            for reg in registros:
                print(f"  • Cliente: {reg[0]} | Arquivo: {reg[1]} | Código: {reg[2]} | Data: {reg[3]}")
        else:
            print("\n⚠️  Nenhum registro encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao buscar registros: {e}")
    
    # Verificar índices
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='produtos_plus'")
        indices = cursor.fetchall()
        print(f"\n📊 Índices encontrados: {len(indices)}")
        for indice in indices:
            print(f"  ✅ {indice[0]}")
    except Exception as e:
        print(f"❌ Erro ao verificar índices: {e}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    if todas_ok:
        print("✅ TESTE PLUS CONCLUÍDO COM SUCESSO!")
        print("🎉 Sistema PLUS com TODAS as 39 colunas!")
    else:
        print("⚠️  TESTE PLUS CONCLUÍDO - Verifique colunas faltantes")
    print("=" * 60)
    return todas_ok

if __name__ == "__main__":
    testar_banco_plus()
