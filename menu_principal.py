import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os
from datetime import datetime
import hashlib
from usuarios_db import autenticar_usuario, criar_usuario
from gerenciamento_usuarios import GerenciamentoUsuarios
from sistema_online_offline import SistemaOnlineOffline
from banco_offline import BancoOffline

class TelaLogin:
    def __init__(self, callback_sucesso):
        self.callback_sucesso = callback_sucesso
        self.sistema_oo = SistemaOnlineOffline()
        self.banco_offline = BancoOffline()
        
        self.janela = tk.Tk()
        self.janela.title("planilhas.com - Login")
        self.janela.geometry("450x650")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#f0f0f0')
        
        # Centralizar janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (650 // 2)
        self.janela.geometry(f"450x650+{x}+{y}")
        
        self.criar_interface_login()
        self.verificar_status_sistema()
        
    def criar_interface_login(self):
        # Frame principal
        frame_principal = ttk.Frame(self.janela, padding="30")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Título
        titulo = ttk.Label(frame_principal, text="🪶 planilhas.com", 
                          font=("Arial", 24, "bold"))
        titulo.pack(pady=(0, 10))
        
        # Subtitulo com status
        self.status_label = ttk.Label(frame_principal, text="Verificando conexão...", 
                                   font=("Arial", 9))
        self.status_label.pack(pady=(0, 20))
        
        # Frame de login
        frame_login = ttk.LabelFrame(frame_principal, text="🔐 Login", padding="20")
        frame_login.pack(fill='x', pady=(0, 20))
        
        # Email
        ttk.Label(frame_login, text="Email:").pack(anchor='w', pady=(0, 5))
        self.email_entry = ttk.Entry(frame_login, width=35)
        self.email_entry.pack(fill='x', pady=(0, 15))
        self.email_entry.insert(0, "admin@planilhas.com")
        
        # Senha
        ttk.Label(frame_login, text="Senha:").pack(anchor='w', pady=(0, 5))
        self.senha_entry = ttk.Entry(frame_login, width=35, show="*")
        self.senha_entry.pack(fill='x', pady=(0, 15))
        self.senha_entry.insert(0, "admin123")
        
        # Botão Login
        btn_login = ttk.Button(frame_login, text="🚀 Entrar", 
                              command=self.fazer_login)
        btn_login.pack(fill='x', pady=(10, 0))
        
        # Separator
        ttk.Separator(frame_principal, orient='horizontal').pack(fill='x', pady=20)
        
        # Frame de cadastro
        frame_cadastro = ttk.LabelFrame(frame_principal, text="👤 Cadastrar Novo Usuário", padding="20")
        frame_cadastro.pack(fill='x')
        
        # Nome
        ttk.Label(frame_cadastro, text="Nome Completo:").pack(anchor='w', pady=(0, 5))
        self.nome_entry = ttk.Entry(frame_cadastro, width=35)
        self.nome_entry.pack(fill='x', pady=(0, 10))
        
        # Email cadastro
        ttk.Label(frame_cadastro, text="Email:").pack(anchor='w', pady=(0, 5))
        self.email_cad_entry = ttk.Entry(frame_cadastro, width=35)
        self.email_cad_entry.pack(fill='x', pady=(0, 10))
        
        # Senha cadastro
        ttk.Label(frame_cadastro, text="Senha:").pack(anchor='w', pady=(0, 5))
        self.senha_cad_entry = ttk.Entry(frame_cadastro, width=35, show="*")
        self.senha_cad_entry.pack(fill='x', pady=(0, 10))
        
        # Confirmar senha
        ttk.Label(frame_cadastro, text="Confirmar Senha:").pack(anchor='w', pady=(0, 5))
        self.confirma_senha_entry = ttk.Entry(frame_cadastro, width=35, show="*")
        self.confirma_senha_entry.pack(fill='x', pady=(0, 15))
        
        # Botão Cadastrar
        btn_cadastrar = ttk.Button(frame_cadastro, text="✅ Cadastrar Usuário", 
                                  command=self.cadastrar_usuario)
        btn_cadastrar.pack(fill='x')
        
        # Info
        info = ttk.Label(frame_principal, 
                        text="Admin padrão: admin@planilhas.com / admin123",
                        font=("Arial", 8), foreground='gray')
        info.pack(pady=(10, 0))
        
    def verificar_status_sistema(self):
        """Verifica e exibe status online/offline"""
        try:
            status = self.sistema_oo.get_status_sistema()
            
            if status['internet']:
                texto_status = "🌐 Online - Sistema conectado"
                cor = "green"
            else:
                texto_status = "📴 Offline - Sistema local"
                cor = "orange"
            
            # Adicionar info da licença
            if status.get('licenca'):
                licenca = status['licenca']
                texto_status += f"\n📜 Licença válida até: {licenca.get('valido_ate', 'N/A')}"
                
                if status['dados_pendentes'] > 0:
                    texto_status += f"\n⏳ {status['dados_pendentes']} dados para sincronizar"
            
            self.status_label.config(text=texto_status, foreground=cor)
            
        except Exception as e:
            self.status_label.config(text=f"❌ Erro ao verificar status: {str(e)}", 
                                  foreground="red")
    
    def fazer_login(self):
        """Faz login híbrido (online/offline)"""
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        try:
            # Tentar login online primeiro
            status = self.sistema_oo.get_status_sistema()
            
            if status['internet']:
                # Tentar login online
                sucesso, mensagem, usuario = self.sistema_oo.login_online(email, senha)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Login online: {mensagem}")
                    self.janela.destroy()
                    self.callback_sucesso(usuario)
                    return
                else:
                    # Falha online, tentar offline
                    messagebox.showwarning("Aviso", f"Falha no login online: {mensagem}\nTentando modo offline...")
            
            # Login offline
            usuario_offline = self.banco_offline.verificar_usuario_offline(email, senha)
            
            if usuario_offline:
                # Verificar licença
                licenca_ok, licenca_msg = self.sistema_oo.verificar_licenca()
                
                if licenca_ok:
                    messagebox.showinfo("Sucesso", f"Login offline realizado!\n{licenca_msg}")
                    self.janela.destroy()
                    self.callback_sucesso(usuario_offline)
                else:
                    messagebox.showerror("Erro", f"Licença inválida: {licenca_msg}")
            else:
                # Tentar login local (banco original)
                usuario = autenticar_usuario(email, senha)
                
                if usuario:
                    messagebox.showinfo("Sucesso", f"Login local realizado!\nModo: {status['modo']}")
                    self.janela.destroy()
                    self.callback_sucesso(usuario)
                else:
                    messagebox.showerror("Erro", "Email ou senha incorretos em todos os modos!")
                    
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no login: {str(e)}")
    
    def cadastrar_usuario(self):
        """Cadastra usuário com suporte online/offline"""
        nome = self.nome_entry.get().strip()
        email = self.email_cad_entry.get().strip()
        senha = self.senha_cad_entry.get().strip()
        confirma_senha = self.confirma_senha_entry.get().strip()
        
        # Validações
        if not nome or not email or not senha or not confirma_senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        if len(nome) < 3:
            messagebox.showerror("Erro", "O nome deve ter pelo menos 3 caracteres!")
            return
        
        if '@' not in email or '.' not in email:
            messagebox.showerror("Erro", "Digite um email válido!")
            return
        
        if len(senha) < 4:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 4 caracteres!")
            return
        
        if senha != confirma_senha:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        try:
            # Verificar status
            status = self.sistema_oo.get_status_sistema()
            
            if status['internet']:
                # Tentar cadastro online
                sucesso, mensagem = criar_usuario(nome, email, senha)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Usuário criado online: {mensagem}")
                    # Criar também no banco offline
                    self.banco_offline.criar_usuario_offline({
                        'id': f"local_{datetime.now().timestamp()}",
                        'nome': nome,
                        'email': email,
                        'senha_hash': hashlib.sha256(senha.encode()).hexdigest(),
                        'nivel_acesso': 'usuario'
                    })
                else:
                    messagebox.showerror("Erro", mensagem)
                    return
            else:
                # Cadastro offline
                sucesso, mensagem = self.banco_offline.criar_usuario_offline({
                    'id': f"offline_{datetime.now().timestamp()}",
                    'nome': nome,
                    'email': email,
                    'senha_hash': hashlib.sha256(senha.encode()).hexdigest(),
                    'nivel_acesso': 'usuario'
                })
                
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Usuário criado offline: {mensagem}\nSerá sincronizado quando a internet voltar.")
                else:
                    messagebox.showerror("Erro", mensagem)
                    return
            
            # Limpar campos de cadastro
            self.nome_entry.delete(0, tk.END)
            self.email_cad_entry.delete(0, tk.END)
            self.senha_cad_entry.delete(0, tk.END)
            self.confirma_senha_entry.delete(0, tk.END)
            # Preencher email no login
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, email)
            # Limpar senha do login para segurança
            self.senha_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cadastro: {str(e)}")
    
    def executar(self):
        self.janela.mainloop()

class MenuPrincipal:
    def __init__(self, usuario_logado):
        self.usuario = usuario_logado
        self.sistema_oo = SistemaOnlineOffline()
        self.banco_offline = BancoOffline()
        
        self.janela = tk.Tk()
        self.janela.title("planilhas.com - Menu Principal")
        self.janela.geometry("450x450")
        self.janela.resizable(False, False)
        
        # Centralizar janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (450 // 2)
        self.janela.geometry(f"450x450+{x}+{y}")
        
        self.criar_interface()
        self.verificar_status_periodico()
        
    def criar_interface(self):
        # Frame principal
        frame_principal = ttk.Frame(self.janela, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Header com info do usuário
        frame_header = ttk.Frame(frame_principal)
        frame_header.pack(fill='x', pady=(0, 20))
        
        # Logo e título
        frame_logo = ttk.Frame(frame_header)
        frame_logo.pack()
        
        titulo = ttk.Label(frame_logo, text="🪶 planilhas.com", 
                          font=("Arial", 20, "bold"))
        titulo.pack()
        
        # Info usuário
        usuario_info = ttk.Label(frame_logo, 
                                text=f"👤 Logado como: {self.usuario['nome']} ({self.usuario['email']})",
                                font=("Arial", 10))
        usuario_info.pack(pady=(5, 0))
        
        # Nível de acesso
        nivel_text = "🔑 Administrador" if self.usuario['nivel_acesso'] == 'admin' else "👤 Usuário"
        nivel_label = ttk.Label(frame_logo, text=nivel_text, font=("Arial", 9, "italic"))
        nivel_label.pack()
        
        # Status do sistema
        self.status_menu_label = ttk.Label(frame_logo, text="Verificando status...", 
                                      font=("Arial", 8), foreground='gray')
        self.status_menu_label.pack(pady=(5, 0))
        
        # Separator
        ttk.Separator(frame_principal, orient='horizontal').pack(fill='x', pady=20)
        
        # Frame dos botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(fill=tk.BOTH, expand=True)
        
        # Botão Sistema Original
        btn_sistema = ttk.Button(frame_botoes, text="📊 Sistema Original", 
                                command=self.abrir_sistema_original,
                                width=30)
        btn_sistema.pack(pady=8)
        
        # Botão Sistema Plus
        btn_sistema_plus = ttk.Button(frame_botoes, text="⭐ Sistema PLUS", 
                                     command=self.abrir_sistema_plus,
                                     width=30)
        btn_sistema_plus.pack(pady=8)
        
        # Botões admin (se for admin)
        if self.usuario['nivel_acesso'] == 'admin':
            btn_usuarios = ttk.Button(frame_botoes, text="👥 Gerenciar Usuários", 
                                    command=self.gerenciar_usuarios,
                                    width=30)
            btn_usuarios.pack(pady=8)
        
        # Botão de sincronização
        btn_sincronizar = ttk.Button(frame_botoes, text="🔄 Sincronizar Dados", 
                                   command=self.sincronizar_dados,
                                   width=30)
        btn_sincronizar.pack(pady=8)
        
        # Separator
        ttk.Separator(frame_botoes, orient='horizontal').pack(fill='x', pady=15)
        
        # Botão Sair
        btn_sair = ttk.Button(frame_botoes, text="🚪 Sair do Sistema", 
                            command=self.sair,
                            width=30)
        btn_sair.pack(pady=8)
        
    def abrir_sistema_original(self):
        """Abre o sistema original em nova janela Tkinter"""
        try:
            from sistema import SistemaPlanilhas
            sistema = SistemaPlanilhas()
            sistema.executar()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o sistema: {str(e)}\nVerifique se o arquivo 'sistema.py' existe.")
    
    def abrir_sistema_plus(self):
        """Abre o sistema PLUS em nova janela Tkinter"""
        try:
            from sistema_plus import SistemaPlanilhasPlus
            sistema_plus = SistemaPlanilhasPlus()
            sistema_plus.executar()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o sistema PLUS: {str(e)}\nVerifique se o arquivo 'sistema_plus.py' existe.")
    
    def gerenciar_usuarios(self):
        """Abre tela de gerenciamento de usuários (admin only)"""
        GerenciamentoUsuarios(self.janela)
    
    def verificar_status_periodico(self):
        """Verifica status do sistema periodicamente"""
        try:
            status = self.sistema_oo.get_status_sistema()
            
            if status['internet']:
                texto = "🌐 Online"
                cor = "green"
            else:
                texto = "📴 Offline"
                cor = "orange"
            
            # Adicionar info de sincronização
            if status.get('dados_pendentes', 0) > 0:
                texto += f" ({status['dados_pendentes']} pendentes)"
            
            self.status_menu_label.config(text=texto, foreground=cor)
            
        except Exception as e:
            self.status_menu_label.config(text=f"❌ Erro: {str(e)[:20]}...", 
                                      foreground="red")
        
        # Verificar novamente a cada 30 segundos
        self.janela.after(30000, self.verificar_status_periodico)
    
    def sincronizar_dados(self):
        """Sincroniza dados pendentes com servidor"""
        try:
            status = self.sistema_oo.get_status_sistema()
            
            if not status['internet']:
                messagebox.showwarning("Aviso", "Sem conexão com internet para sincronizar!")
                return
            
            # Obter estatísticas offline
            stats = self.banco_offline.obter_estatisticas_offline()
            
            if stats.get('produtos_pendentes', 0) == 0 and stats.get('logs_pendentes', 0) == 0:
                messagebox.showinfo("Sincronização", "Nenhum dado pendente para sincronizar!")
                return
            
            # Confirmar sincronização
            total_pendentes = stats.get('produtos_pendentes', 0) + stats.get('logs_pendentes', 0)
            
            if messagebox.askyesno("Sincronizar Dados", 
                                 f"Existem {total_pendentes} dados pendentes.\n\nDeseja sincronizar agora?"):
                
                # Tentar sincronizar
                sucesso, mensagem = self.sistema_oo.sincronizar_dados_online(self.usuario['id'])
                
                if sucesso:
                    messagebox.showinfo("Sucesso", f"Dados sincronizados: {mensagem}")
                else:
                    messagebox.showerror("Erro", f"Falha na sincronização: {mensagem}")
                
                # Atualizar status
                self.verificar_status_periodico()
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na sincronização: {str(e)}")
    
    def verificar_sistema_ativo(self, sistema):
        """Verifica se o usuário fechou o sistema para reabrir o menu"""
        pass
    
    def sair(self):
        """Fecha o menu principal e volta para login"""
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            self.janela.destroy()
            # Reabrir tela de login
            app = SistemaComLogin()
            app.executar()
    
    def executar(self):
        """Inicia o menu principal"""
        self.janela.mainloop()

class SistemaComLogin:
    def __init__(self):
        self.usuario_logado = None
        
    def on_login_sucesso(self, usuario):
        """Callback quando login é bem sucedido"""
        self.usuario_logado = usuario
        # Abrir menu principal
        menu = MenuPrincipal(usuario)
        menu.executar()
    
    def executar(self):
        """Inicia com tela de login"""
        tela_login = TelaLogin(self.on_login_sucesso)
        tela_login.executar()

if __name__ == "__main__":
    app = SistemaComLogin()
    app.executar()
