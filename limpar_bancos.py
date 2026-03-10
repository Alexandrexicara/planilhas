import os
import sqlite3

def limpar_wal_shm():
    """Limpa arquivos temporários dos bancos"""
    arquivos_temp = [
        'banco.db-wal', 'banco.db-shm',
        'banco_plus.db-wal', 'banco_plus.db-shm'
    ]
    
    for arquivo in arquivos_temp:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"✅ Removido: {arquivo}")
            except:
                print(f"❌ Não foi possível remover: {arquivo}")

def otimizar_bancos():
    """Otimiza e limpa os bancos"""
    bancos = ['banco.db', 'banco_plus.db']
    
    for banco in bancos:
        if os.path.exists(banco):
            try:
                conn = sqlite3.connect(banco)
                conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
                conn.execute("VACUUM")
                conn.close()
                print(f"✅ Otimizado: {banco}")
            except Exception as e:
                print(f"❌ Erro em {banco}: {e}")

if __name__ == "__main__":
    print("🧹 LIMPANDO ARQUIVOS TEMPORÁRIOS...")
    limpar_wal_shm()
    
    print("\n⚙️ OTIMIZANDO BANCOS...")
    otimizar_bancos()
    
    print("\n✅ CONCLUÍDO!")
