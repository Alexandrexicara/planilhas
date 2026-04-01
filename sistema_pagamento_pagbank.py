import requests
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
import uuid
import base64

class SistemaPagamentoPagBank:
    def __init__(self):
        self.db_file = "sistema_pagamento.db"
        self.config_file = "config_pagamento.json"
        self.inicializar_banco()
        self.carregar_config()
    
    def carregar_config(self):
        """Carrega configurações do PagBank"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except:
            self.config = {
                "pagbank": {
                    "client_id": "16a9aa69-d7e4-42c7-9688-ed95ac1e47cf",
                    "client_secret": "5b77fe6e4bb0b273825a39cf3919dc700987-52dd-45fa-9d9c-29137dd10a7c",
                    "ambiente": "sandbox"
                }
            }
            self.salvar_config()
    
    def salvar_config(self):
        """Salva configurações"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def inicializar_banco(self):
        """Cria tabelas do sistema de pagamento"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Tabela de usuários com controle de pagamento
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios_pagamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            telefone TEXT,
            acesso_liberado INTEGER DEFAULT 0,
            data_cadastro TEXT NOT NULL,
            data_liberacao TEXT,
            plano TEXT DEFAULT 'mensal',
            valor_pago REAL DEFAULT 0,
            data_expiracao TEXT,
            pagamento_pendente INTEGER DEFAULT 0,
            id_pagamento_pagbank TEXT,
            qr_code_pix TEXT,
            chave_pix TEXT,
            status_pagamento TEXT DEFAULT 'pendente'
        )
        """)
        
        # Tabela de pagamentos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            valor REAL NOT NULL,
            plano TEXT NOT NULL,
            metodo_pagamento TEXT DEFAULT 'pix',
            status TEXT DEFAULT 'pendente',
            id_transacao TEXT,
            data_criacao TEXT NOT NULL,
            data_aprovacao TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios_pagamento (id)
        )
        """)
        
        # Tabela de planos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS planos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL,
            valor REAL NOT NULL,
            dias_validade INTEGER NOT NULL,
            descricao TEXT,
            ativo INTEGER DEFAULT 1
        )
        """)
        
        # Inserir planos padrão
        cursor.execute("""
        INSERT OR IGNORE INTO planos (nome, valor, dias_validade, descricao) VALUES
        ('mensal', 97.00, 30, 'Acesso mensal ao sistema'),
        ('trimestral', 267.00, 90, 'Acesso trimestral com 10% de desconto'),
        ('anual', 897.00, 365, 'Acesso anual com 30% de desconto')
        """)
        
        conn.commit()
        conn.close()
    
    def obter_token_pagbank(self):
        """Obtém token de acesso do PagBank"""
        try:
            # URL base conforme ambiente
            if self.config['pagbank']['ambiente'] == 'sandbox':
                base_url = "https://sandbox.api.pagseguro.com"
            else:
                base_url = "https://api.pagseguro.com"
            
            # Autenticação Basic Auth
            credentials = f"{self.config['pagbank']['client_id']}:{self.config['pagbank']['client_secret']}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            
            # Obter token
            response = requests.post(
                f"{base_url}/public/oauth/token",
                headers=headers,
                json={
                    "grant_type": "client_credentials",
                    "scope": "cob.read cob.write pix.read pix.write"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                return {
                    'access_token': token_data.get('access_token'),
                    'expires_in': token_data.get('expires_in', 3600)
                }
            else:
                print(f"Erro ao obter token: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Erro na autenticação PagBank: {str(e)}")
            return None
    
    def gerar_pagamento_pix_pagbank(self, usuario_id, plano='mensal'):
        """Gera pagamento PIX via PagBank"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            # Obter dados do usuário e plano
            cursor.execute("""
            SELECT u.nome, u.email, p.valor, p.dias_validade 
            FROM usuarios_pagamento u
            JOIN planos p ON u.plano = p.nome
            WHERE u.id = ?
            """, (usuario_id,))
            
            dados = cursor.fetchone()
            if not dados:
                return False, {'erro': 'Usuário não encontrado'}
            
            nome, email, valor, dias_validade = dados
            
            # Obter token
            token_data = self.obter_token_pagbank()
            if not token_data:
                return False, {'erro': 'Erro ao obter token de acesso'}
            
            # URL base conforme ambiente
            if self.config['pagbank']['ambiente'] == 'sandbox':
                base_url = "https://sandbox.api.pagseguro.com"
            else:
                base_url = "https://api.pagseguro.com"
            
            headers = {
                'Authorization': f'Bearer {token_data["access_token"]}',
                'Content-Type': 'application/json'
            }
            
            # Criar cobrança PIX
            cobranca_data = {
                "calendario": {
                    "expiracao": 3600  # 1 hora
                },
                "devedor": {
                    "cpf": "12345678909",  # CPF teste
                    "nome": nome
                },
                "valor": {
                    "original": str(valor).replace('.', '')
                },
                "chave": "santossilvac992@gmail.com",  # Sua chave PIX
                "infoAdicionais": [
                    {
                        "nome": "Pagamento",
                        "valor": f"Plano {plano} - planilhas.com"
                    }
                ]
            }
            
            response = requests.post(
                f"{base_url}/v2/cob",
                headers=headers,
                json=cobranca_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                cobranca = response.json()
                txid = cobranca.get('txid')
                
                # Gerar QR Code
                qr_response = requests.get(
                    f"{base_url}/v2/loc/{cobranca['loc']['id']}/qrcode",
                    headers=headers,
                    timeout=30
                )
                
                if qr_response.status_code == 200:
                    qr_data = qr_response.json()
                    qr_code_base64 = qr_data.get('qrcode')
                    chave_pix = cobranca.get('chave')
                    
                    # Atualizar usuário com dados do pagamento
                    cursor.execute("""
                    UPDATE usuarios_pagamento 
                    SET pagamento_pendente = 1, id_pagamento_pagbank = ?, 
                        qr_code_pix = ?, chave_pix = ?, status_pagamento = 'aguardando_pagamento'
                    WHERE id = ?
                    """, (txid, qr_code_base64, chave_pix, usuario_id))
                    
                    # Registrar pagamento
                    cursor.execute("""
                    INSERT INTO pagamentos 
                    (usuario_id, valor, plano, metodo_pagamento, status, id_transacao, data_criacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        usuario_id, valor, plano, 'pix', 'pendente', txid,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ))
                    
                    conn.commit()
                    
                    return True, {
                        'id_pagamento': txid,
                        'qr_code': qr_code_base64,
                        'chave_pix': chave_pix,
                        'valor': valor,
                        'plano': plano,
                        'dias_validade': dias_validade,
                        'mensagem': f'PIX gerado! Pague R$ {valor:.2f} para liberar acesso.'
                    }
                else:
                    return False, {'erro': f'Erro ao gerar QR Code: {qr_response.text}'}
            else:
                return False, {'erro': f'Erro ao criar cobrança: {response.status_code} - {response.text}'}
                
        except Exception as e:
            return False, {'erro': f'Erro ao gerar pagamento: {str(e)}'}
        finally:
            conn.close()
    
    def verificar_status_pagamento_pagbank(self, usuario_id):
        """Verifica status do pagamento no PagBank"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            SELECT id_pagamento_pagbank, status_pagamento 
            FROM usuarios_pagamento 
            WHERE id = ?
            """, (usuario_id,))
            
            resultado = cursor.fetchone()
            if not resultado:
                return False, {'erro': 'Usuário não encontrado'}
            
            txid, status_atual = resultado
            
            # Obter token
            token_data = self.obter_token_pagbank()
            if not token_data:
                return False, {'erro': 'Erro ao obter token de acesso'}
            
            # URL base conforme ambiente
            if self.config['pagbank']['ambiente'] == 'sandbox':
                base_url = "https://sandbox.api.pagseguro.com"
            else:
                base_url = "https://api.pagseguro.com"
            
            headers = {
                'Authorization': f'Bearer {token_data["access_token"]}',
                'Content-Type': 'application/json'
            }
            
            # Consultar status da cobrança
            response = requests.get(
                f"{base_url}/v2/cob/{txid}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                cobranca = response.json()
                status_pagbank = cobranca.get('status')
                
                # Mapear status
                if status_pagbank == 'ATIVA':
                    status_atual = 'pendente'
                elif status_pagbank == 'CONCLUIDA':
                    status_atual = 'aprovado'
                elif status_pagbank == 'REMOVIDA_PELO_PSP':
                    status_atual = 'removido'
                elif status_pagbank == 'REMOVIDA_PELO_USUARIO_RECEBEDOR':
                    status_atual = 'cancelado'
                
                # Se pagamento aprovado, liberar acesso
                if status_atual == 'aprovado':
                    return self.liberar_acesso(usuario_id, 'pix')
                
                return True, {'status': status_atual}
            else:
                return False, {'erro': f'Erro ao consultar status: {response.status_code}'}
                
        except Exception as e:
            return False, {'erro': f'Erro ao verificar pagamento: {str(e)}'}
        finally:
            conn.close()
    
    def cadastrar_usuario(self, nome, email, senha, telefone=""):
        """Cadastra novo usuário (bloqueado até pagamento)"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            
            cursor.execute("""
            INSERT INTO usuarios_pagamento 
            (nome, email, senha, telefone, acesso_liberado, data_cadastro, plano)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                nome, email, senha_hash, telefone, 
                0,  # acesso_liberado = False
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'mensal'
            ))
            
            usuario_id = cursor.lastrowid
            conn.commit()
            
            return True, {
                'id': usuario_id,
                'nome': nome,
                'email': email,
                'acesso_liberado': False,
                'mensagem': 'Usuário cadastrado! Realize o pagamento para liberar acesso.'
            }
            
        except sqlite3.IntegrityError:
            return False, {'erro': 'Email já cadastrado!'}
        except Exception as e:
            return False, {'erro': f'Erro ao cadastrar: {str(e)}'}
        finally:
            conn.close()
    
    def verificar_login(self, email, senha):
        """Verifica login e status de pagamento"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            
            cursor.execute("""
            SELECT id, nome, email, acesso_liberado, plano, data_expiracao, 
                   pagamento_pendente, status_pagamento
            FROM usuarios_pagamento 
            WHERE email = ? AND senha = ?
            """, (email, senha_hash))
            
            resultado = cursor.fetchone()
            
            if resultado:
                usuario = {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'acesso_liberado': bool(resultado[3]),
                    'plano': resultado[4],
                    'data_expiracao': resultado[5],
                    'pagamento_pendente': bool(resultado[6]),
                    'status_pagamento': resultado[7]
                }
                
                # Verificar se acesso expirou
                if usuario['data_expiracao']:
                    data_expiracao = datetime.strptime(usuario['data_expiracao'], '%Y-%m-%d %H:%M:%S')
                    if datetime.now() > data_expiracao:
                        usuario['acesso_liberado'] = False
                        usuario['status_pagamento'] = 'expirado'
                
                return True, usuario
            else:
                return False, {'erro': 'Email ou senha incorretos'}
                
        except Exception as e:
            return False, {'erro': f'Erro no login: {str(e)}'}
        finally:
            conn.close()
    
    def liberar_acesso(self, usuario_id, metodo_pagamento='pix'):
        """Libera acesso do usuário após pagamento confirmado"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            # Obter dados do usuário
            cursor.execute("""
            SELECT plano FROM usuarios_pagamento WHERE id = ?
            """, (usuario_id,))
            
            resultado = cursor.fetchone()
            if not resultado:
                return False, {'erro': 'Usuário não encontrado'}
            
            plano = resultado[0]
            
            # Obter dias de validade do plano
            cursor.execute("""
            SELECT dias_validade FROM planos WHERE nome = ?
            """, (plano,))
            
            dias_result = cursor.fetchone()
            dias_validade = dias_result[0] if dias_result else 30
            
            # Calcular data de expiração
            data_expiracao = datetime.now() + timedelta(days=dias_validade)
            
            # Atualizar usuário
            cursor.execute("""
            UPDATE usuarios_pagamento 
            SET acesso_liberado = 1, data_liberacao = ?, 
                data_expiracao = ?, pagamento_pendente = 0, 
                status_pagamento = 'aprovado'
            WHERE id = ?
            """, (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                data_expiracao.strftime('%Y-%m-%d %H:%M:%S'),
                usuario_id
            ))
            
            # Atualizar status do pagamento
            cursor.execute("""
            UPDATE pagamentos 
            SET status = 'aprovado', data_aprovacao = ?
            WHERE usuario_id = ? AND status = 'pendente'
            ORDER BY id DESC LIMIT 1
            """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), usuario_id))
            
            conn.commit()
            
            return True, {
                'mensagem': f'Acesso liberado com sucesso! Válido até {data_expiracao.strftime("%d/%m/%Y")}',
                'data_expiracao': data_expiracao.strftime('%Y-%m-%d %H:%M:%S'),
                'dias_validade': dias_validade
            }
            
        except Exception as e:
            return False, {'erro': f'Erro ao liberar acesso: {str(e)}'}
        finally:
            conn.close()
    
    def obter_dados_usuario(self, usuario_id):
        """Obtém dados completos do usuário"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            SELECT id, nome, email, acesso_liberado, plano, data_cadastro, 
                   data_liberacao, data_expiracao, pagamento_pendente, 
                   status_pagamento, qr_code_pix, chave_pix
            FROM usuarios_pagamento 
            WHERE id = ?
            """, (usuario_id,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                return {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'acesso_liberado': bool(resultado[3]),
                    'plano': resultado[4],
                    'data_cadastro': resultado[5],
                    'data_liberacao': resultado[6],
                    'data_expiracao': resultado[7],
                    'pagamento_pendente': bool(resultado[8]),
                    'status_pagamento': resultado[9],
                    'qr_code_pix': resultado[10],
                    'chave_pix': resultado[11]
                }
            else:
                return None
                
        except Exception as e:
            print(f"Erro ao obter dados: {str(e)}")
            return None
        finally:
            conn.close()
    
    def obter_planos_disponiveis(self):
        """Obtém planos disponíveis"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            SELECT nome, valor, dias_validade, descricao 
            FROM planos 
            WHERE ativo = 1 
            ORDER BY valor ASC
            """)
            
            planos = cursor.fetchall()
            
            return [
                {
                    'nome': plano[0],
                    'valor': plano[1],
                    'dias_validade': plano[2],
                    'descricao': plano[3]
                }
                for plano in planos
            ]
            
        except Exception as e:
            print(f"Erro ao obter planos: {str(e)}")
            return []
        finally:
            conn.close()
