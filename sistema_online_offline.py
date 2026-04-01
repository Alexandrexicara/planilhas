import requests
import json
import sqlite3
from datetime import datetime, timedelta
import os
import hashlib

class SistemaOnlineOffline:
    def __init__(self):
        self.config_file = "config_sistema.json"
        self.licenca_file = "licenca.json"
        self.db_local = "banco_offline.db"
        self.carregar_configuracoes()
        
    def carregar_configuracoes(self):
        """Carrega configurações do sistema"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            # Configuração padrão
            self.config = {
                "servidor": "https://seu-servidor.com/api",
                "dias_offline_max": 7,
                "modo_debug": True
            }
            self.salvar_configuracoes()
    
    def salvar_configuracoes(self):
        """Salva configurações do sistema"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def tem_internet(self):
        """Verifica se há conexão com internet"""
        try:
            # Tenta conectar a múltiplos serviços para maior confiabilidade
            servicos = [
                "https://www.google.com",
                "https://www.cloudflare.com",
                "https://httpbin.org/get"
            ]
            
            for servico in servicos:
                try:
                    response = requests.get(servico, timeout=3)
                    if response.status_code == 200:
                        return True
                except:
                    continue
            
            return False
        except:
            return False
    
    def verificar_licenca(self):
        """Verifica se a licença é válida"""
        if not os.path.exists(self.licenca_file):
            return False, "Nenhuma licença encontrada"
        
        try:
            with open(self.licenca_file, 'r', encoding='utf-8') as f:
                licenca = json.load(f)
            
            # Verificar data de validade
            data_validade = datetime.strptime(licenca.get('valido_ate', ''), '%Y-%m-%d')
            data_atual = datetime.now()
            
            if data_atual > data_validade:
                return False, f"Licença expirou em {data_validade.strftime('%d/%m/%Y')}"
            
            # Verificar hash de integridade
            dados_verificacao = f"{licenca['usuario']}{licenca['valido_ate']}{licenca['email']}"
            hash_calculado = hashlib.sha256(dados_verificacao.encode()).hexdigest()
            
            if licenca.get('hash_integridade') != hash_calculado:
                return False, "Licença corrompida ou alterada"
            
            return True, "Licença válida"
            
        except Exception as e:
            return False, f"Erro ao verificar licença: {str(e)}"
    
    def criar_licenca_local(self, usuario_data):
        """Cria licença local baseada nos dados do servidor"""
        try:
            # Calcular data de validade (dias configurados)
            data_validade = datetime.now() + timedelta(days=self.config['dias_offline_max'])
            
            # Criar hash de integridade
            dados_verificacao = f"{usuario_data['id']}{data_validade.strftime('%Y-%m-%d')}{usuario_data['email']}"
            hash_integridade = hashlib.sha256(dados_verificacao.encode()).hexdigest()
            
            licenca = {
                "usuario": usuario_data['id'],
                "email": usuario_data['email'],
                "nome": usuario_data['nome'],
                "valido_ate": data_validade.strftime('%Y-%m-%d'),
                "nivel_acesso": usuario_data.get('nivel_acesso', 'usuario'),
                "data_ultima_sinc": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "hash_integridade": hash_integridade,
                "modo_offline": True
            }
            
            with open(self.licenca_file, 'w', encoding='utf-8') as f:
                json.dump(licenca, f, indent=4, ensure_ascii=False)
            
            return True, "Licença criada com sucesso"
            
        except Exception as e:
            return False, f"Erro ao criar licença: {str(e)}"
    
    def login_online(self, email, senha):
        """Faz login no servidor online"""
        try:
            if not self.tem_internet():
                return False, "Sem conexão com internet", None
            
            # Enviar requisição para o servidor
            dados_login = {
                "email": email,
                "senha": hashlib.sha256(senha.encode()).hexdigest(),
                "dispositivo": self.get_device_id()
            }
            
            response = requests.post(
                f"{self.config['servidor']}/login",
                json=dados_login,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('sucesso'):
                    # Criar licença local
                    sucesso, msg = self.criar_licenca_local(data['usuario'])
                    if sucesso:
                        # Sincronizar dados
                        self.sincronizar_dados_online(data['usuario']['id'])
                        return True, "Login online realizado com sucesso", data['usuario']
                    else:
                        return False, f"Erro ao criar licença: {msg}", None
                else:
                    return False, data.get('mensagem', 'Erro no login'), None
            else:
                return False, "Erro de conexão com servidor", None
                
        except Exception as e:
            return False, f"Erro no login online: {str(e)}", None
    
    def login_offline(self, email, senha):
        """Faz login usando licença local"""
        try:
            # Verificar licença
            licenca_valida, msg = self.verificar_licenca()
            if not licenca_valida:
                return False, msg, None
            
            # Carregar licença
            with open(self.licenca_file, 'r', encoding='utf-8') as f:
                licenca = json.load(f)
            
            # Verificar email
            if licenca['email'] != email:
                return False, "Email não corresponde à licença", None
            
            # Verificar senha offline (usando hash local)
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            
            # Aqui você pode ter um banco local de senhas ou usar o hash da licença
            # Para simplificar, vamos verificar se existe usuário local
            conn = sqlite3.connect(self.db_local)
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT senha FROM usuarios_offline 
            WHERE email = ? AND ativo = 1
            """, (email,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado and resultado[0] == senha_hash:
                # Atualizar última sincronização
                licenca['data_ultima_sinc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                with open(self.licenca_file, 'w', encoding='utf-8') as f:
                    json.dump(licenca, f, indent=4, ensure_ascii=False)
                
                usuario = {
                    'id': licenca['usuario'],
                    'email': licenca['email'],
                    'nome': licenca['nome'],
                    'nivel_acesso': licenca['nivel_acesso']
                }
                
                return True, f"Login offline realizado (válido até {licenca['valido_ate']})", usuario
            else:
                return False, "Senha incorreta", None
                
        except Exception as e:
            return False, f"Erro no login offline: {str(e)}", None
    
    def sincronizar_dados_online(self, usuario_id):
        """Sincroniza dados com servidor online"""
        try:
            if not self.tem_internet():
                return False, "Sem conexão para sincronizar"
            
            # Enviar dados locais para servidor
            dados_locais = self.obter_dados_pendentes()
            
            if dados_locais:
                response = requests.post(
                    f"{self.config['servidor']}/sincronizar",
                    json={
                        "usuario_id": usuario_id,
                        "dados": dados_locais
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    # Marcar dados como sincronizados
                    self.marcar_dados_sincronizados()
                    return True, "Dados sincronizados com sucesso"
                else:
                    return False, "Erro ao sincronizar dados"
            
            return True, "Nenhum dado pendente para sincronizar"
            
        except Exception as e:
            return False, f"Erro na sincronização: {str(e)}"
    
    def obter_dados_pendentes(self):
        """Obtém dados que precisam ser sincronizados"""
        conn = sqlite3.connect(self.db_local)
        cursor = conn.cursor()
        
        # Criar tabela se não existir
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dados_pendentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tabela TEXT NOT NULL,
            operacao TEXT NOT NULL,
            dados TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            sincronizado INTEGER DEFAULT 0
        )
        """)
        
        cursor.execute("""
        SELECT * FROM dados_pendentes 
        WHERE sincronizado = 0
        ORDER BY data_criacao
        """)
        
        pendentes = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': item[0],
                'tabela': item[1],
                'operacao': item[2],
                'dados': json.loads(item[3]),
                'data_criacao': item[4]
            }
            for item in pendentes
        ]
    
    def marcar_dados_sincronizados(self):
        """Marca dados como sincronizados"""
        conn = sqlite3.connect(self.db_local)
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE dados_pendentes 
        SET sincronizado = 1 
        WHERE sincronizado = 0
        """)
        
        conn.commit()
        conn.close()
    
    def adicionar_dado_pendente(self, tabela, operacao, dados):
        """Adiciona operação para sincronização futura"""
        conn = sqlite3.connect(self.db_local)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO dados_pendentes (tabela, operacao, dados, data_criacao)
        VALUES (?, ?, ?, ?)
        """, (
            tabela,
            operacao,
            json.dumps(dados, ensure_ascii=False),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
        conn.close()
    
    def get_device_id(self):
        """Gera/obtém ID único do dispositivo"""
        device_file = "device_id.txt"
        
        if os.path.exists(device_file):
            with open(device_file, 'r') as f:
                return f.read().strip()
        else:
            # Gerar ID único baseado no hardware
            import platform
            import uuid
            
            device_info = f"{platform.node()}{platform.system()}{uuid.getnode()}"
            device_id = hashlib.md5(device_info.encode()).hexdigest()
            
            with open(device_file, 'w') as f:
                f.write(device_id)
            
            return device_id
    
    def get_status_sistema(self):
        """Retorna status atual do sistema"""
        tem_net = self.tem_internet()
        licenca_ok, licenca_msg = self.verificar_licenca()
        
        status = {
            "modo": "online" if tem_net else "offline",
            "internet": tem_net,
            "licenca_valida": licenca_ok,
            "licenca_mensagem": licenca_msg,
            "dados_pendentes": len(self.obter_dados_pendentes())
        }
        
        # Adicionar info da licença se existir
        if os.path.exists(self.licenca_file):
            try:
                with open(self.licenca_file, 'r', encoding='utf-8') as f:
                    licenca = json.load(f)
                    status["licenca"] = {
                        "valido_ate": licenca.get('valido_ate'),
                        "usuario": licenca.get('nome'),
                        "email": licenca.get('email'),
                        "ultima_sinc": licenca.get('data_ultima_sinc')
                    }
            except:
                pass
        
        return status
