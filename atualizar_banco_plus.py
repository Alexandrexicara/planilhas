"""
Atualiza o banco_plus.db para ter TODAS as 39 colunas
"""
import sqlite3
import os

def atualizar_banco_plus():
    """Recria o banco PLUS com todas as 39 colunas"""
    print("=" * 60)
    print("🔄 ATUALIZANDO BANCO PLUS PARA 39 COLUNAS")
    print("=" * 60)
    
    # Remover banco antigo se existir
    if os.path.exists('banco_plus.db'):
        print("🗑️  Removendo banco_plus.db antigo...")
        os.remove('banco_plus.db')
        
        # Remover arquivos temporários também
        for arquivo in ['banco_plus.db-wal', 'banco_plus.db-shm']:
            if os.path.exists(arquivo):
                os.remove(arquivo)
                print(f"   ✅ Removido: {arquivo}")
    
    print("\n✨ Criando novo banco_plus.db com 39 colunas...")
    
    # Criar novo banco
    conn = sqlite3.connect('banco_plus.db')
    cursor = conn.cursor()
    
    # Configurações
    cursor.execute("PRAGMA journal_mode=DELETE")
    cursor.execute("PRAGMA synchronous=FULL")
    cursor.execute("PRAGMA cache_size=25000")
    cursor.execute("PRAGMA temp_store=FILE")
    
    # Tabela principal com TODAS as 39 colunas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos_plus(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT COLLATE NOCASE,
        arquivo_origem TEXT,
        codigo TEXT COLLATE NOCASE,
        descricao TEXT COLLATE NOCASE,
        peso TEXT,
        valor TEXT,
        ncm TEXT COLLATE NOCASE,
        doc TEXT,
        rev TEXT,
        code TEXT,
        quantity TEXT,
        um TEXT,
        ccy TEXT,
        total_amount TEXT,
        marca TEXT,
        inner_qty TEXT,
        master_qty TEXT,
        total_ctns TEXT,
        gross_weight TEXT,
        net_weight_pc TEXT,
        gross_weight_pc TEXT,
        net_weight_ctn TEXT,
        gross_weight_ctn TEXT,
        factory TEXT,
        address TEXT,
        telephone TEXT,
        ean13 TEXT,
        dun14_inner TEXT,
        dun14_master TEXT,
        length TEXT,
        width TEXT,
        height TEXT,
        cbm TEXT,
        prc_kg TEXT,
        li TEXT,
        obs TEXT,
        status TEXT,
        data_importacao TEXT,
        hash_dados TEXT
    )
    """)
    
    print("✅ Tabela 'produtos_plus' criada com 39 colunas")
    
    # Índices
    indices = [
        "CREATE INDEX IF NOT EXISTS idx_cliente_plus ON produtos_plus(cliente)",
        "CREATE INDEX IF NOT EXISTS idx_codigo_plus ON produtos_plus(codigo)",
        "CREATE INDEX IF NOT EXISTS idx_descricao_plus ON produtos_plus(descricao)",
        "CREATE INDEX IF NOT EXISTS idx_ncm_plus ON produtos_plus(ncm)",
        "CREATE INDEX IF NOT EXISTS idx_hash_plus ON produtos_plus(hash_dados)",
        "CREATE INDEX IF NOT EXISTS idx_busca_completa_plus ON produtos_plus(cliente, codigo, descricao, ncm)"
    ]
    
    for indice_sql in indices:
        cursor.execute(indice_sql)
    
    print(f"✅ {len(indices)} índices criados")
    
    # Tabela de estatísticas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stats_plus(
        id INTEGER PRIMARY KEY,
        total_planilhas INTEGER,
        total_produtos INTEGER,
        ultima_atualizacao TEXT,
        tamanho_banco_mb REAL
    )
    """)
    
    print("✅ Tabela 'stats_plus' criada")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ BANCO PLUS ATUALIZADO COM SUCESSO!")
    print("📊 Agora possui TODAS as 39 colunas")
    print("=" * 60)

if __name__ == "__main__":
    atualizar_banco_plus()
