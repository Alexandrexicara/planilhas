import sqlite3
import hashlib
from datetime import datetime

class BancoOffline:
    def __init__(self, db_file="banco_offline.db"):
        self.db_file = db_file
        self.inicializar_banco()
    
    def inicializar_banco(self):
        """Cria tabelas necessárias para modo offline"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Tabela de usuários offline
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_offline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_servidor TEXT UNIQUE,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nivel_acesso TEXT DEFAULT 'usuario',
            ativo INTEGER DEFAULT 1,
            data_criacao TEXT NOT NULL,
            ultima_sinc TEXT
        )
        """)
        
        # Tabela de produtos offline (sincroniza com sistema principal)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos_offline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_servidor TEXT UNIQUE,
            cliente TEXT NOT NULL,
            arquivo_origem TEXT,
            codigo TEXT,
            descricao TEXT,
            peso TEXT,
            valor TEXT,
            ncm TEXT,
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
            data_importacao TEXT NOT NULL,
            sincronizado INTEGER DEFAULT 0,
            data_criacao_local TEXT NOT NULL
        )
        """)
        
        # Tabela de configurações offline
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS config_offline (
            chave TEXT PRIMARY KEY,
            valor TEXT NOT NULL,
            data_atualizacao TEXT NOT NULL
        )
        """)
        
        # Tabela de logs offline
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs_offline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT,
            acao TEXT NOT NULL,
            tabela TEXT,
            registro_id TEXT,
            dados_antigos TEXT,
            dados_novos TEXT,
            data_criacao TEXT NOT NULL,
            sincronizado INTEGER DEFAULT 0
        )
        """)
        
        conn.commit()
        conn.close()
    
    def criar_usuario_offline(self, usuario_data):
        """Cria usuário para acesso offline"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT OR REPLACE INTO usuarios_offline 
            (id_servidor, nome, email, senha, nivel_acesso, ativo, data_criacao, ultima_sinc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                usuario_data['id'],
                usuario_data['nome'],
                usuario_data['email'],
                usuario_data.get('senha_hash', ''),
                usuario_data.get('nivel_acesso', 'usuario'),
                1,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            conn.commit()
            return True, "Usuário criado offline com sucesso"
            
        except sqlite3.IntegrityError:
            return False, "Email já existe offline"
        except Exception as e:
            return False, f"Erro ao criar usuário offline: {str(e)}"
        finally:
            conn.close()
    
    def verificar_usuario_offline(self, email, senha):
        """Verifica usuário no banco offline"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            
            cursor.execute("""
            SELECT id_servidor, nome, email, nivel_acesso, ativo
            FROM usuarios_offline 
            WHERE email = ? AND senha = ? AND ativo = 1
            """, (email, senha_hash))
            
            resultado = cursor.fetchone()
            
            if resultado:
                return {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'nivel_acesso': resultado[3]
                }
            else:
                return None
                
        except Exception as e:
            print(f"Erro ao verificar usuário offline: {str(e)}")
            return None
        finally:
            conn.close()
    
    def atualizar_senha_offline(self, email, nova_senha):
        """Atualiza senha do usuário offline"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
            
            cursor.execute("""
            UPDATE usuarios_offline 
            SET senha = ?, ultima_sinc = ?
            WHERE email = ?
            """, (senha_hash, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), email))
            
            if cursor.rowcount > 0:
                conn.commit()
                return True, "Senha atualizada offline"
            else:
                return False, "Usuário não encontrado"
                
        except Exception as e:
            return False, f"Erro ao atualizar senha: {str(e)}"
        finally:
            conn.close()
    
    def adicionar_produto_offline(self, produto_data):
        """Adiciona produto para sincronização posterior"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO produtos_offline 
            (id_servidor, cliente, arquivo_origem, codigo, descricao, peso, valor, ncm,
             doc, rev, code, quantity, um, ccy, total_amount, marca, inner_qty, master_qty,
             total_ctns, gross_weight, net_weight_pc, gross_weight_pc, net_weight_ctn,
             gross_weight_ctn, factory, address, telephone, ean13, dun14_inner, dun14_master,
             length, width, height, cbm, prc_kg, li, obs, status, data_importacao,
             data_criacao_local)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                produto_data.get('id_servidor', ''),
                produto_data.get('cliente', ''),
                produto_data.get('arquivo_origem', ''),
                produto_data.get('codigo', ''),
                produto_data.get('descricao', ''),
                produto_data.get('peso', ''),
                produto_data.get('valor', ''),
                produto_data.get('ncm', ''),
                produto_data.get('doc', ''),
                produto_data.get('rev', ''),
                produto_data.get('code', ''),
                produto_data.get('quantity', ''),
                produto_data.get('um', ''),
                produto_data.get('ccy', ''),
                produto_data.get('total_amount', ''),
                produto_data.get('marca', ''),
                produto_data.get('inner_qty', ''),
                produto_data.get('master_qty', ''),
                produto_data.get('total_ctns', ''),
                produto_data.get('gross_weight', ''),
                produto_data.get('net_weight_pc', ''),
                produto_data.get('gross_weight_pc', ''),
                produto_data.get('net_weight_ctn', ''),
                produto_data.get('gross_weight_ctn', ''),
                produto_data.get('factory', ''),
                produto_data.get('address', ''),
                produto_data.get('telephone', ''),
                produto_data.get('ean13', ''),
                produto_data.get('dun14_inner', ''),
                produto_data.get('dun14_master', ''),
                produto_data.get('length', ''),
                produto_data.get('width', ''),
                produto_data.get('height', ''),
                produto_data.get('cbm', ''),
                produto_data.get('prc_kg', ''),
                produto_data.get('li', ''),
                produto_data.get('obs', ''),
                produto_data.get('status', ''),
                produto_data.get('data_importacao', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            conn.commit()
            return True, "Produto adicionado offline"
            
        except Exception as e:
            return False, f"Erro ao adicionar produto offline: {str(e)}"
        finally:
            conn.close()
    
    def obter_produtos_offline(self, limit=100):
        """Obtém produtos do banco offline"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            SELECT * FROM produtos_offline 
            ORDER BY data_criacao_local DESC 
            LIMIT ?
            """, (limit,))
            
            produtos = cursor.fetchall()
            
            # Obter nomes das colunas
            cursor.execute("PRAGMA table_info(produtos_offline)")
            colunas = [col[1] for col in cursor.fetchall()]
            
            return [dict(zip(colunas, produto)) for produto in produtos]
            
        except Exception as e:
            print(f"Erro ao obter produtos offline: {str(e)}")
            return []
        finally:
            conn.close()
    
    def adicionar_log_offline(self, usuario_id, acao, tabela=None, registro_id=None, 
                           dados_antigos=None, dados_novos=None):
        """Adiciona log de ação offline"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO logs_offline 
            (usuario_id, acao, tabela, registro_id, dados_antigos, dados_novos, data_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                usuario_id,
                acao,
                tabela,
                registro_id,
                json.dumps(dados_antigos) if dados_antigos else None,
                json.dumps(dados_novos) if dados_novos else None,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
            
            conn.commit()
            
        except Exception as e:
            print(f"Erro ao adicionar log offline: {str(e)}")
        finally:
            conn.close()
    
    def obter_estatisticas_offline(self):
        """Obtém estatísticas do modo offline"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            stats = {}
            
            # Total de usuários
            cursor.execute("SELECT COUNT(*) FROM usuarios_offline WHERE ativo = 1")
            stats['usuarios_offline'] = cursor.fetchone()[0]
            
            # Total de produtos
            cursor.execute("SELECT COUNT(*) FROM produtos_offline")
            stats['produtos_offline'] = cursor.fetchone()[0]
            
            # Produtos não sincronizados
            cursor.execute("SELECT COUNT(*) FROM produtos_offline WHERE sincronizado = 0")
            stats['produtos_pendentes'] = cursor.fetchone()[0]
            
            # Logs não sincronizados
            cursor.execute("SELECT COUNT(*) FROM logs_offline WHERE sincronizado = 0")
            stats['logs_pendentes'] = cursor.fetchone()[0]
            
            return stats
            
        except Exception as e:
            print(f"Erro ao obter estatísticas: {str(e)}")
            return {}
        finally:
            conn.close()

# Import necessário para JSON
import json
