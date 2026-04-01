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
from sistema_pagamento_simulado import SistemaPagamentoPagBankSimulado
from tela_pagamento import TelaCadastroPagamento

class TelaLoginPrincipalSimulado:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("planilhas.com - Sistema Completo (Simulado)")
        self.janela.geometry("500x450")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#f0f0f0')
        
        # Centralizar janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (450 // 2)
        self.janela.geometry(f"500x450+{x}+{y}")
        
        self.sistema_oo = SistemaOnlineOffline()
        self.banco_offline = BancoOffline()
        self.sistema_pg = SistemaPagamentoPagBankSimulado()
        
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        frame_principal = ttk.Frame(self.janela, padding="30")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Título
        titulo = ttk.Label(frame_principal, text="🪶 planilhas.com", 
                          font=("Arial", 24, "bold"))
        titulo.pack(pady=(0, 10))
        
        subtitulo = ttk.Label(frame_principal, text="Sistema de Gestão de Planilhas (Simulado)", 
                            font=("Arial", 12))
        subtitulo.pack(pady=(0, 20))
        
        # Frame de opções
        frame_opcoes = ttk.Frame(frame_principal)
        frame_opcoes.pack(fill='x', pady=20)
        
        # Botão de Cadastro e Pagamento
        btn_cadastro = ttk.Button(frame_opcoes, text="🆕 Novo Cadastro + Pagamento PIX (Simulado)", 
                               command=self.abrir_cadastro_pagamento,
                               width=35)
        btn_cadastro.pack(pady=10)
        
        # Botão de Login para Usuários Cadastrados
        btn_login = ttk.Button(frame_opcoes, text="🔐 Login (Usuário Cadastrado)", 
                            command=self.abrir_login_tradicional,
                            width=35)
        btn_login.pack(pady=10)
        
        # Botão de Teste PagBank
        btn_testar = ttk.Button(frame_opcoes, text="🧪 Testar PagBank Simulado", 
                             command=self.testar_pagbank,
                             width=35)
        btn_testar.pack(pady=10)
        
        # Separator
        ttk.Separator(frame_principal, orient='horizontal').pack(fill='x', pady=20)
        
        # Frame de acesso direto
        frame_acesso = ttk.LabelFrame(frame_principal, text="Acesso Rápido", padding="15")
        frame_acesso.pack(fill='x')
        
        # Email
        ttk.Label(frame_acesso, text="Email:").pack(anchor='w', pady=(0, 5))
        self.email_entry = ttk.Entry(frame_acesso, width=40)
        self.email_entry.pack(fill='x', pady=(0, 10))
        
        # Senha
        ttk.Label(frame_acesso, text="Senha:").pack(anchor='w', pady=(0, 5))
        self.senha_entry = ttk.Entry(frame_acesso, width=40, show="*")
        self.senha_entry.pack(fill='x', pady=(0, 15))
        
        # Botão Entrar
        btn_entrar = ttk.Button(frame_acesso, text="🚀 Entrar Direto", 
                              command=self.fazer_login_direto)
        btn_entrar.pack(fill='x')
        
        # Info
        info = ttk.Label(frame_principal, 
                        text="Novos usuários: Cadastre-se e pague via PIX simulado\nUsuários existentes: Use login tradicional",
                        font=("Arial", 9), foreground='gray', justify='center')
        info.pack(pady=(20, 0))
        
        # Status PagBank
        self.status_label = ttk.Label(frame_principal, 
                                   text="🟢 PagBank Simulado - Pronto", 
                                   font=("Arial", 8), foreground='green')
        self.status_label.pack(pady=(10, 0))
    
    def abrir_cadastro_pagamento(self):
        """Abre tela de cadastro e pagamento"""
        self.janela.withdraw()
        
        def callback_sucesso(usuario):
            self.janela.deiconify()
            self.abrir_menu_principal(usuario)
        
        tela_pg = TelaCadastroPagamento(callback_sucesso)
        tela_pg.executar()
    
    def abrir_login_tradicional(self):
        """Abre tela de login tradicional"""
        self.janela.withdraw()
        
        def callback_sucesso(usuario):
            self.janela.deiconify()
            self.abrir_menu_principal(usuario)
        
        from menu_principal import TelaLogin
        tela_login = TelaLogin(callback_sucesso)
        tela_login.executar()
    
    def testar_pagbank(self):
        """Executa testes do PagBank"""
        try:
            from testar_pagbank_simulado import testar_pagbank_simulado
            testar_pagbank_simulado()
            messagebox.showinfo("Teste", "Testes PagBank Simulado executados! Verifique o console.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar testes: {str(e)}")
    
    def fazer_login_direto(self):
        """Faz login direto (híbrido)"""
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        
        if not email or not senha:
            messagebox.showerror("Erro", "Preencha email e senha!")
            return
        
        try:
            # Tentar login no sistema de pagamento simulado primeiro
            sucesso, resultado = self.sistema_pg.verificar_login(email, senha)
            
            if sucesso:
                if resultado.get('acesso_liberado'):
                    messagebox.showinfo("Sucesso", f"Bem-vindo(a), {resultado['nome']}!")
                    self.abrir_menu_principal(resultado)
                    return
                else:
                    messagebox.showwarning("Pagamento Pendente", 
                                       "Seu acesso está bloqueado. Realize o pagamento simulado para liberar.")
                    self.abrir_cadastro_pagamento()
                    return
            
            # Tentar login tradicional
            usuario = autenticar_usuario(email, senha)
            if usuario:
                messagebox.showinfo("Sucesso", f"Bem-vindo(a), {usuario['nome']}!")
                self.abrir_menu_principal(usuario)
            else:
                messagebox.showerror("Erro", "Email ou senha incorretos!")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no login: {str(e)}")
    
    def abrir_menu_principal(self, usuario_logado):
        """Abre menu principal com o usuário logado"""
        self.janela.destroy()
        
        # Importar e executar menu principal
        from menu_principal import MenuPrincipal
        menu = MenuPrincipal(usuario_logado)
        menu.executar()
    
    def executar(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = TelaLoginPrincipalSimulado()
    app.executar()
