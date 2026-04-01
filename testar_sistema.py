"""
Script de teste para verificar se o sistema está salvando planilhas corretamente
"""
import sqlite3
import os
from datetime import datetime

def testar_banco_dados():
    """Testa se o banco de dados está configurado corretamente"""
    print("=" * 60)
    print("🧪 TESTANDO SISTEMA DE PLANILHAS")
    print("=" * 60)
    
    # Conectar ao banco
    if not os.path.exists('banco.db'):
        print("❌ Banco de dados não encontrado!")
        return False
    
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    
    # Verificar se tabela produtos existe
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produtos'")
        if cursor.fetchone():
            print("✅ Tabela 'produtos' encontrada")
        else:
            print("❌ Tabela 'produtos' não encontrada!")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar tabela: {e}")
        return False
    
    # Verificar colunas da tabela
    try:
        cursor.execute("PRAGMA table_info(produtos)")
        colunas = cursor.fetchall()
        print(f"\n📊 Colunas da tabela produtos: {len(colunas)}")
        
        colunas_esperadas = [
            'id', 'cliente', 'arquivo_origem', 'codigo', 'descricao', 'peso', 'valor', 
            'ncm', 'doc', 'rev', 'code', 'quantity', 'um', 'ccy', 'total_amount',
            'marca', 'inner_qty', 'master_qty', 'total_ctns', 'gross_weight',
            'net_weight_pc', 'gross_weight_pc', 'net_weight_ctn', 'gross_weight_ctn',
            'factory', 'address', 'telephone', 'ean13', 'dun14_inner', 'dun14_master',
            'length', 'width', 'height', 'cbm', 'prc_kg', 'li', 'obs', 'status',
            'data_importacao'
        ]
        
        colunas_encontradas = [col[1] for col in colunas]
        
        for coluna in colunas_esperadas:
            if coluna in colunas_encontradas:
                print(f"  ✅ {coluna}")
            else:
                print(f"  ❌ {coluna} (FALTANDO)")
        
    except Exception as e:
        print(f"❌ Erro ao verificar colunas: {e}")
        return False
    
    # Contar registros
    try:
        cursor.execute("SELECT COUNT(*) FROM produtos")
        total = cursor.fetchone()[0]
        print(f"\n📦 Total de produtos cadastrados: {total:,}")
    except Exception as e:
        print(f"❌ Erro ao contar produtos: {e}")
    
    # Verificar últimos registros
    try:
        cursor.execute("""
            SELECT cliente, arquivo_origem, codigo, descricao, data_importacao 
            FROM produtos 
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
    
    # Verificar tabela de importações
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='importacoes'")
        if cursor.fetchone():
            print("\n✅ Tabela 'importacoes' encontrada")
            
            cursor.execute("SELECT COUNT(*) FROM importacoes")
            total_imp = cursor.fetchone()[0]
            print(f"📁 Total de importações: {total_imp}")
        else:
            print("\n❌ Tabela 'importacoes' não encontrada!")
    except Exception as e:
        print(f"❌ Erro ao verificar importações: {e}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ TESTE CONCLUÍDO!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    testar_banco_dados()
