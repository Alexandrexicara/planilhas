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
        """Carrega configuracoes do sistema"""
        config_padrao = {
            "servidor": "https://seu-servidor.com/api",
            "dias_offline_max": 7,
            "modo_debug": True,
            "timeout_conexao": 10,
            "tentativas_reconexao": 3,
            "intervalo_sincronizacao": 30,
            "versao_sistema": "1.0.0",
            "max_maquinas_permitidas": 10,
            "atualizacao_automatica": False,
            "atualizacao_requer_compra": True
        }

        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)

            # Garante novas chaves sem quebrar instalacoes antigas
            for chave, valor in config_padrao.items():
                if chave not in self.config:
                    self.config[chave] = valor
            self.salvar_configuracoes()
        else:
            # Configuracao padrao
            self.config = config_padrao
            self.salvar_configuracoes()

    def salvar_configuracoes(self):
        """Salva configuraÃ§Ãµes do sistema"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def gerar_hash_licenca(self, licenca):
        """Gera hash de integridade com campos relevantes da licenca."""
        payload = {
            "usuario": licenca.get("usuario"),
            "email": licenca.get("email"),
            "valido_ate": licenca.get("valido_ate"),
            "nivel_acesso": licenca.get("nivel_acesso", "usuario"),
            "versao_licenca": licenca.get("versao_licenca", self.config.get("versao_sistema", "1.0.0")),
            "max_maquinas": int(licenca.get("max_maquinas", self.config.get("max_maquinas_permitidas", 10))),
            "dispositivos_autorizados": sorted(licenca.get("dispositivos_autorizados", [])),
            "atualizacao_requer_compra": bool(licenca.get("atualizacao_requer_compra", True))
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()

    def _parse_versao(self, versao):
        partes = []
        for parte in str(versao).split("."):
            try:
                partes.append(int(parte))
            except ValueError:
                partes.append(0)
        while len(partes) < 3:
            partes.append(0)
        return tuple(partes[:3])

    def versao_maior(self, versao_a, versao_b):
        """Retorna True se versao_a > versao_b."""
        return self._parse_versao(versao_a) > self._parse_versao(versao_b)

    def _montar_licenca(self, usuario_data):
        """Monta estrutura padrao da licenca local."""
        data_validade = datetime.now() + timedelta(days=self.config['dias_offline_max'])
        dispositivo_atual = self.get_device_id()

        dispositivos_autorizados = usuario_data.get("dispositivos_autorizados") or []
        if not isinstance(dispositivos_autorizados, list):
            dispositivos_autorizados = []

        max_maquinas = int(
            usuario_data.get("max_maquinas", self.config.get("max_maquinas_permitidas", 10))
        )
        if max_maquinas < 1:
            max_maquinas = 1

        if dispositivo_atual not in dispositivos_autorizados:
            if len(dispositivos_autorizados) >= max_maquinas:
                return None, (
                    f"Limite de maquinas atingido ({max_maquinas}). "
                    "Remova uma maquina ativa antes de liberar esta."
                )
            dispositivos_autorizados.append(dispositivo_atual)

        licenca = {
            "usuario": usuario_data['id'],
            "email": usuario_data['email'],
            "nome": usuario_data['nome'],
            "valido_ate": data_validade.strftime('%Y-%m-%d'),
            "nivel_acesso": usuario_data.get('nivel_acesso', 'usuario'),
            "data_ultima_sinc": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "modo_offline": True,
            "versao_licenca": usuario_data.get("versao_licenca", self.config.get("versao_sistema", "1.0.0")),
            "max_maquinas": max_maquinas,
            "dispositivos_autorizados": dispositivos_autorizados,
            "atualizacao_automatica": False,
            "atualizacao_requer_compra": bool(
                usuario_data.get("atualizacao_requer_compra", self.config.get("atualizacao_requer_compra", True))
            )
        }

        licenca["hash_integridade"] = self.gerar_hash_licenca(licenca)
        return licenca, "Licenca criada com sucesso"
    
    def tem_internet(self):
        """Verifica se hÃ¡ conexÃ£o com internet"""
        try:
            # Tenta conectar a mÃºltiplos serviÃ§os para maior confiabilidade
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
        """Verifica se a licenÃ§a Ã© vÃ¡lida"""
        if not os.path.exists(self.licenca_file):
            return False, "Nenhuma licenÃ§a encontrada"
        
        try:
            with open(self.licenca_file, 'r', encoding='utf-8') as f:
                licenca = json.load(f)

            # Backward compatibility para licencas antigas
            if "max_maquinas" not in licenca:
                licenca["max_maquinas"] = int(self.config.get("max_maquinas_permitidas", 10))
            if "dispositivos_autorizados" not in licenca or not isinstance(licenca["dispositivos_autorizados"], list):
                licenca["dispositivos_autorizados"] = []
            # Migracao suave: licencas antigas sem lista ganham o dispositivo atual
            if len(licenca["dispositivos_autorizados"]) == 0:
                licenca["dispositivos_autorizados"].append(self.get_device_id())
            if "versao_licenca" not in licenca:
                licenca["versao_licenca"] = self.config.get("versao_sistema", "1.0.0")
            if "atualizacao_requer_compra" not in licenca:
                licenca["atualizacao_requer_compra"] = bool(self.config.get("atualizacao_requer_compra", True))

            # Verificar data de validade
            data_validade = datetime.strptime(licenca.get('valido_ate', ''), '%Y-%m-%d')
            if datetime.now() > data_validade:
                return False, f"LicenÃ§a expirou em {data_validade.strftime('%d/%m/%Y')}"

            # Verificar hash de integridade (novo formato + legado)
            hash_atual = licenca.get("hash_integridade", "")
            hash_novo = self.gerar_hash_licenca(licenca)
            hash_legado = hashlib.sha256(
                f"{licenca.get('usuario', '')}{licenca.get('valido_ate', '')}{licenca.get('email', '')}".encode()
            ).hexdigest()

            if hash_atual not in {hash_novo, hash_legado}:
                return False, "LicenÃ§a corrompida ou alterada"

            # Enforce limite de maquinas
            dispositivo_atual = self.get_device_id()
            autorizados = licenca.get("dispositivos_autorizados", [])
            max_maquinas = int(licenca.get("max_maquinas", self.config.get("max_maquinas_permitidas", 10)))
            if dispositivo_atual not in autorizados:
                return False, (
                    f"Esta maquina nao esta autorizada para a licenca. "
                    f"Limite contratado: {max_maquinas} maquinas."
                )

            # Atualizacao por compra: se app > licenca e regra ativa, bloqueia
            versao_sistema = self.config.get("versao_sistema", "1.0.0")
            versao_licenca = licenca.get("versao_licenca", versao_sistema)
            if licenca.get("atualizacao_requer_compra", True) and self.versao_maior(versao_sistema, versao_licenca):
                return False, (
                    f"Licenca valida ate versao {versao_licenca}. "
                    f"Versao instalada {versao_sistema} requer compra de atualizacao."
                )

            # Se hash legado foi usado, migra para novo hash
            if hash_atual != hash_novo:
                licenca["hash_integridade"] = hash_novo
                with open(self.licenca_file, 'w', encoding='utf-8') as f:
                    json.dump(licenca, f, indent=4, ensure_ascii=False)

            return True, "LicenÃ§a vÃ¡lida"
            
        except Exception as e:
            return False, f"Erro ao verificar licenÃ§a: {str(e)}"
    
    def criar_licenca_local(self, usuario_data):
        """Cria licenÃ§a local baseada nos dados do servidor"""
        try:
            licenca, mensagem = self._montar_licenca(usuario_data)
            if not licenca:
                return False, mensagem

            with open(self.licenca_file, 'w', encoding='utf-8') as f:
                json.dump(licenca, f, indent=4, ensure_ascii=False)
            
            return True, mensagem
            
        except Exception as e:
            return False, f"Erro ao criar licenÃ§a: {str(e)}"
    
    def login_online(self, email, senha):
        """Faz login no servidor online"""
        try:
            if not self.tem_internet():
                return False, "Sem conexÃ£o com internet", None
            
            # Enviar requisiÃ§Ã£o para o servidor
            dados_login = {
                "email": email,
                "senha": hashlib.sha256(senha.encode()).hexdigest(),
                "dispositivo": self.get_device_id(),
                "versao_sistema": self.config.get("versao_sistema", "1.0.0")
            }
            
            response = requests.post(
                f"{self.config['servidor']}/login",
                json=dados_login,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('sucesso'):
                    # Criar licenÃ§a local
                    sucesso, msg = self.criar_licenca_local(data['usuario'])
                    if sucesso:
                        # Sincronizar dados
                        self.sincronizar_dados_online(data['usuario']['id'])
                        return True, "Login online realizado com sucesso", data['usuario']
                    else:
                        return False, f"Erro ao criar licenÃ§a: {msg}", None
                else:
                    return False, data.get('mensagem', 'Erro no login'), None
            elif response.status_code in (401, 403, 409):
                try:
                    data = response.json()
                    return False, data.get('mensagem', 'Acesso negado pelo servidor'), None
                except Exception:
                    return False, "Acesso negado pelo servidor", None
            else:
                return False, "Erro de conexÃ£o com servidor", None
                
        except Exception as e:
            return False, f"Erro no login online: {str(e)}", None
    
    def login_offline(self, email, senha):
        """Faz login usando licenÃ§a local"""
        try:
            # Verificar licenÃ§a
            licenca_valida, msg = self.verificar_licenca()
            if not licenca_valida:
                return False, msg, None
            
            # Carregar licenÃ§a
            with open(self.licenca_file, 'r', encoding='utf-8') as f:
                licenca = json.load(f)
            
            # Verificar email
            if licenca['email'] != email:
                return False, "Email nÃ£o corresponde Ã  licenÃ§a", None
            
            # Verificar senha offline (usando hash local)
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            
            # Aqui vocÃª pode ter um banco local de senhas ou usar o hash da licenÃ§a
            # Para simplificar, vamos verificar se existe usuÃ¡rio local
            conn = sqlite3.connect(self.db_local)
            cursor = conn.cursor()
            
            cursor.execute("""
            SELECT senha FROM usuarios_offline 
            WHERE email = ? AND ativo = 1
            """, (email,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado and resultado[0] == senha_hash:
                # Atualizar Ãºltima sincronizaÃ§Ã£o
                licenca['data_ultima_sinc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                with open(self.licenca_file, 'w', encoding='utf-8') as f:
                    json.dump(licenca, f, indent=4, ensure_ascii=False)
                
                usuario = {
                    'id': licenca['usuario'],
                    'email': licenca['email'],
                    'nome': licenca['nome'],
                    'nivel_acesso': licenca['nivel_acesso']
                }
                
                return True, f"Login offline realizado (vÃ¡lido atÃ© {licenca['valido_ate']})", usuario
            else:
                return False, "Senha incorreta", None
                
        except Exception as e:
            return False, f"Erro no login offline: {str(e)}", None
    
    def sincronizar_dados_online(self, usuario_id):
        """Sincroniza dados com servidor online"""
        try:
            if not self.tem_internet():
                return False, "Sem conexÃ£o para sincronizar"
            
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
            return False, f"Erro na sincronizaÃ§Ã£o: {str(e)}"
    
    def obter_dados_pendentes(self):
        """ObtÃ©m dados que precisam ser sincronizados"""
        conn = sqlite3.connect(self.db_local)
        cursor = conn.cursor()
        
        # Criar tabela se nÃ£o existir
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
        """Adiciona operaÃ§Ã£o para sincronizaÃ§Ã£o futura"""
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
        """Gera/obtÃ©m ID Ãºnico do dispositivo"""
        device_file = "device_id.txt"
        
        if os.path.exists(device_file):
            with open(device_file, 'r') as f:
                return f.read().strip()
        else:
            # Gerar ID Ãºnico baseado no hardware
            import platform
            import uuid
            
            device_info = f"{platform.node()}{platform.system()}{uuid.getnode()}"
            device_id = hashlib.md5(device_info.encode()).hexdigest()
            
            with open(device_file, 'w') as f:
                f.write(device_id)
            
            return device_id

    def pode_atualizar_para(self, nova_versao):
        """
        Verifica se a licenca atual permite atualizar para `nova_versao`.
        Regra: se `atualizacao_requer_compra` for True, so permite ate versao_licenca.
        """
        if not os.path.exists(self.licenca_file):
            return False, "Licenca nao encontrada"

        with open(self.licenca_file, 'r', encoding='utf-8') as f:
            licenca = json.load(f)

        versao_licenca = licenca.get("versao_licenca", self.config.get("versao_sistema", "1.0.0"))
        requer_compra = bool(licenca.get("atualizacao_requer_compra", True))

        if not requer_compra:
            return True, "Atualizacao liberada"

        if self.versao_maior(nova_versao, versao_licenca):
            return False, (
                f"Atualizacao para {nova_versao} bloqueada. "
                f"Licenca atual cobre ate {versao_licenca}."
            )
        return True, "Atualizacao permitida pela licenca"
    
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
        
        # Adicionar info da licenÃ§a se existir
        if os.path.exists(self.licenca_file):
            try:
                with open(self.licenca_file, 'r', encoding='utf-8') as f:
                    licenca = json.load(f)
                    status["licenca"] = {
                        "valido_ate": licenca.get('valido_ate'),
                        "usuario": licenca.get('nome'),
                        "email": licenca.get('email'),
                        "ultima_sinc": licenca.get('data_ultima_sinc'),
                        "versao_licenca": licenca.get('versao_licenca'),
                        "max_maquinas": licenca.get('max_maquinas', self.config.get("max_maquinas_permitidas", 10)),
                        "maquinas_em_uso": len(licenca.get('dispositivos_autorizados', [])),
                        "dispositivo_atual_autorizado": self.get_device_id() in licenca.get('dispositivos_autorizados', [])
                    }
            except:
                pass
        
        return status

