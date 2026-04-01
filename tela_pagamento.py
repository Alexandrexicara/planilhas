import tkinter as tk
from tkinter import ttk, messagebox, Canvas
import qrcode
from PIL import Image, ImageTk
import io
from sistema_pagamento_pagbank import SistemaPagamentoPagBank
import threading
import time
import base64

class TelaCadastroPagamento:
    def __init__(self, callback_sucesso):
        self.callback_sucesso = callback_sucesso
        self.sistema_pg = SistemaPagamentoPagBank()
        
        self.janela = tk.Tk()
        self.janela.title("planilhas.com - Cadastro e Pagamento")
        self.janela.geometry("500x700")
        self.janela.resizable(False, False)
        self.janela.configure(bg='#f0f0f0')
        
        # Centralizar janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (700 // 2)
        self.janela.geometry(f"500x700+{x}+{y}")
        
        self.usuario_logado = None
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        frame_principal = ttk.Frame(self.janela, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Logo/Título
        titulo = ttk.Label(frame_principal, text="🪶 planilhas.com", 
                          font=("Arial", 20, "bold"))
        titulo.pack(pady=(0, 5))
        
        subtitulo = ttk.Label(frame_principal, text="Cadastro e Pagamento", 
                            font=("Arial", 12))
        subtitulo.pack(pady=(0, 20))
        
        # Notebook para abas
        self.notebook = ttk.Notebook(frame_principal)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba de Cadastro
        self.frame_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_cadastro, text="1️⃣ Cadastro")
        self.criar_aba_cadastro()
        
        # Aba de Planos
        self.frame_planos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_planos, text="2️⃣ Planos")
        self.criar_aba_planos()
        
        # Aba de Pagamento
        self.frame_pagamento = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_pagamento, text="3️⃣ Pagamento PIX")
        self.criar_aba_pagamento()
        
        # Aba de Acesso
        self.frame_acesso = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_acesso, text="4️⃣ Meu Acesso")
        self.criar_aba_acesso()
        
        # Botões inferiores
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(fill='x', pady=(20, 0))
        
        self.btn_entrar = ttk.Button(frame_botoes, text="🚀 Entrar no Sistema", 
                                   command=self.entrar_sistema, state='disabled')
        self.btn_entrar.pack(side='left', padx=(0, 10))
        
        ttk.Button(frame_botoes, text="❌ Sair", 
                 command=self.janela.destroy).pack(side='right')
    
    def criar_aba_cadastro(self):
        frame = ttk.Frame(self.frame_cadastro, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Nome
        ttk.Label(frame, text="Nome Completo:").pack(anchor='w', pady=(0, 5))
        self.nome_entry = ttk.Entry(frame, width=40)
        self.nome_entry.pack(fill='x', pady=(0, 15))
        
        # Email
        ttk.Label(frame, text="Email:").pack(anchor='w', pady=(0, 5))
        self.email_entry = ttk.Entry(frame, width=40)
        self.email_entry.pack(fill='x', pady=(0, 15))
        
        # Telefone
        ttk.Label(frame, text="Telefone (opcional):").pack(anchor='w', pady=(0, 5))
        self.telefone_entry = ttk.Entry(frame, width=40)
        self.telefone_entry.pack(fill='x', pady=(0, 15))
        
        # Senha
        ttk.Label(frame, text="Senha:").pack(anchor='w', pady=(0, 5))
        self.senha_entry = ttk.Entry(frame, width=40, show="*")
        self.senha_entry.pack(fill='x', pady=(0, 15))
        
        # Confirmar Senha
        ttk.Label(frame, text="Confirmar Senha:").pack(anchor='w', pady=(0, 5))
        self.confirma_senha_entry = ttk.Entry(frame, width=40, show="*")
        self.confirma_senha_entry.pack(fill='x', pady=(0, 20))
        
        # Botão Cadastrar
        btn_cadastrar = ttk.Button(frame, text="✅ Cadastrar", 
                                command=self.cadastrar_usuario)
        btn_cadastrar.pack(fill='x')
        
        # Info
        info = ttk.Label(frame, 
                        text="Após o cadastro, você precisará realizar o pagamento para liberar acesso.",
                        font=("Arial", 9), foreground='gray')
        info.pack(pady=(20, 0))
    
    def criar_aba_planos(self):
        frame = ttk.Frame(self.frame_planos, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Escolha seu plano:", 
                 font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        # Obter planos
        planos = self.sistema_pg.obter_planos_disponiveis()
        
        self.plano_var = tk.StringVar(value="mensal")
        
        for plano in planos:
            # Frame do plano
            frame_plano = ttk.LabelFrame(frame, text=plano['nome'].upper(), padding="15")
            frame_plano.pack(fill='x', pady=10)
            
            # Info do plano
            ttk.Label(frame_plano, text=f"R$ {plano['valor']:.2f}", 
                     font=("Arial", 16, "bold")).pack()
            
            ttk.Label(frame_plano, text=f"{plano['dias_validade']} dias de acesso", 
                     font=("Arial", 10)).pack()
            
            ttk.Label(frame_plano, text=plano['descricao'], 
                     font=("Arial", 9), foreground='gray').pack()
            
            # Radio button
            ttk.Radiobutton(frame_plano, text="Selecionar este plano", 
                           variable=self.plano_var, value=plano['nome']).pack(pady=(10, 0))
        
        # Info adicional
        info_frame = ttk.LabelFrame(frame, text="💡 Informações", padding="10")
        info_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Label(info_frame, text="• Acesso imediato após pagamento", 
                 font=("Arial", 9)).pack(anchor='w')
        ttk.Label(info_frame, text="• Pagamento 100% seguro via PIX", 
                 font=("Arial", 9)).pack(anchor='w')
        ttk.Label(info_frame, text="• Cancelamento a qualquer momento", 
                 font=("Arial", 9)).pack(anchor='w')
    
    def criar_aba_pagamento(self):
        frame = ttk.Frame(self.frame_pagamento, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="Pagamento via PIX", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Frame do QR Code
        frame_qr = ttk.LabelFrame(frame, text="📱 Escaneie o QR Code", padding="20")
        frame_qr.pack(fill='x', pady=(0, 20))
        
        # Canvas para QR Code
        self.canvas_qr = Canvas(frame_qr, width=250, height=250, bg='white')
        self.canvas_qr.pack()
        
        # Frame de informações
        frame_info = ttk.LabelFrame(frame, text="💰 Informações do Pagamento", padding="15")
        frame_info.pack(fill='x', pady=(0, 20))
        
        self.valor_label = ttk.Label(frame_info, text="Valor: ---", 
                                  font=("Arial", 12, "bold"))
        self.valor_label.pack(anchor='w', pady=(0, 5))
        
        self.chave_label = ttk.Label(frame_info, text="Chave PIX: ---", 
                                   font=("Arial", 10))
        self.chave_label.pack(anchor='w', pady=(0, 5))
        
        self.status_label = ttk.Label(frame_info, text="Status: Aguardando cadastro", 
                                   font=("Arial", 10), foreground='orange')
        self.status_label.pack(anchor='w', pady=(0, 10))
        
        # Botões
        frame_botoes_pg = ttk.Frame(frame)
        frame_botoes_pg.pack(fill='x')
        
        self.btn_gerar_pix = ttk.Button(frame_botoes_pg, text="🔄 Gerar PIX", 
                                      command=self.gerar_pix)
        self.btn_gerar_pix.pack(side='left', padx=(0, 10))
        
        self.btn_verificar = ttk.Button(frame_botoes_pg, text="✅ Verificar Pagamento", 
                                    command=self.verificar_pagamento)
        self.btn_verificar.pack(side='left')
        
        # Instruções
        frame_instrucoes = ttk.LabelFrame(frame, text="📋 Instruções", padding="10")
        frame_instrucoes.pack(fill='x', pady=(20, 0))
        
        instrucoes = """1. Clique em "Gerar PIX" para criar seu pagamento
2. Escaneie o QR Code com app do seu banco
3. Ou copie a chave PIX e cole no app
4. Após pagar, clique em "Verificar Pagamento"
5. Se aprovado, seu acesso será liberado automaticamente"""
        
        ttk.Label(frame_instrucoes, text=instrucoes, 
                 font=("Arial", 9), justify='left').pack()
    
    def criar_aba_acesso(self):
        frame = ttk.Frame(self.frame_acesso, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="🔐 Meu Acesso", 
                 font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        # Frame de informações do usuário
        frame_usuario = ttk.LabelFrame(frame, text="👤 Dados do Usuário", padding="15")
        frame_usuario.pack(fill='x', pady=(0, 20))
        
        self.info_nome_label = ttk.Label(frame_usuario, text="Nome: ---")
        self.info_nome_label.pack(anchor='w', pady=2)
        
        self.info_email_label = ttk.Label(frame_usuario, text="Email: ---")
        self.info_email_label.pack(anchor='w', pady=2)
        
        self.info_plano_label = ttk.Label(frame_usuario, text="Plano: ---")
        self.info_plano_label.pack(anchor='w', pady=2)
        
        # Frame de status de acesso
        frame_status = ttk.LabelFrame(frame, text="🔓 Status do Acesso", padding="15")
        frame_status.pack(fill='x', pady=(0, 20))
        
        self.status_acesso_label = ttk.Label(frame_status, text="Status: ---", 
                                         font=("Arial", 12, "bold"))
        self.status_acesso_label.pack(anchor='w', pady=2)
        
        self.data_cadastro_label = ttk.Label(frame_status, text="Cadastro: ---")
        self.data_cadastro_label.pack(anchor='w', pady=2)
        
        self.data_expiracao_label = ttk.Label(frame_status, text="Expiração: ---")
        self.data_expiracao_label.pack(anchor='w', pady=2)
        
        # Botão de verificação automática
        self.btn_verificar_auto = ttk.Button(frame, text="🔄 Verificar Status Automaticamente", 
                                         command=self.iniciar_verificacao_auto)
        self.btn_verificar_auto.pack(pady=20)
        
        # Inicialmente desabilitado
        self.btn_verificar_auto.config(state='disabled')
    
    def cadastrar_usuario(self):
        """Cadastra novo usuário"""
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        senha = self.senha_entry.get().strip()
        confirma_senha = self.confirma_senha_entry.get().strip()
        
        # Validações
        if not nome or not email or not senha or not confirma_senha:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
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
            sucesso, resultado = self.sistema_pg.cadastrar_usuario(nome, email, senha, telefone)
            
            if sucesso:
                self.usuario_logado = resultado
                messagebox.showinfo("Sucesso", resultado['mensagem'])
                
                # Limpar campos
                self.nome_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)
                self.telefone_entry.delete(0, tk.END)
                self.senha_entry.delete(0, tk.END)
                self.confirma_senha_entry.delete(0, tk.END)
                
                # Atualizar aba de acesso
                self.atualizar_aba_acesso()
                
                # Mudar para aba de pagamento
                self.notebook.select(2)  # Aba de pagamento
                
            else:
                messagebox.showerror("Erro", resultado['erro'])
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro no cadastro: {str(e)}")
    
    def gerar_pix(self):
        """Gera pagamento PIX via PagBank"""
        if not self.usuario_logado:
            messagebox.showerror("Erro", "Cadastre-se primeiro!")
            return
        
        try:
            plano = self.plano_var.get()
            sucesso, resultado = self.sistema_pg.gerar_pagamento_pix_pagbank(self.usuario_logado['id'], plano)
            
            if sucesso:
                # Converter QR Code base64 para imagem
                qr_code_base64 = resultado['qr_code']
                
                # Remover prefixo se existir
                if qr_code_base64.startswith('data:image/png;base64,'):
                    qr_code_base64 = qr_code_base64.replace('data:image/png;base64,', '')
                
                # Decodificar base64
                qr_code_bytes = base64.b64decode(qr_code_base64)
                
                # Criar imagem PIL
                img = Image.open(io.BytesIO(qr_code_bytes))
                
                # Redimensionar para o canvas
                img = img.resize((250, 250), Image.Resampling.LANCZOS)
                
                # Converter para PhotoImage
                self.photo = ImageTk.PhotoImage(img)
                
                # Mostrar no canvas
                self.canvas_qr.delete("all")
                self.canvas_qr.create_image(125, 125, image=self.photo)
                
                # Atualizar informações
                self.valor_label.config(text=f"Valor: R$ {resultado['valor']:.2f}")
                self.chave_label.config(text=f"Chave PIX: {resultado['chave_pix']}")
                self.status_label.config(text="Status: Aguardando pagamento", foreground='orange')
                
                messagebox.showinfo("PIX Gerado", resultado['mensagem'])
                
            else:
                messagebox.showerror("Erro", resultado['erro'])
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PIX: {str(e)}")
    
    def verificar_pagamento(self):
        """Verifica status do pagamento no PagBank"""
        if not self.usuario_logado:
            messagebox.showerror("Erro", "Cadastre-se primeiro!")
            return
        
        try:
            sucesso, resultado = self.sistema_pg.verificar_status_pagamento_pagbank(self.usuario_logado['id'])
            
            if sucesso:
                status = resultado.get('status', 'desconhecido')
                
                if status == 'aprovado':
                    self.status_label.config(text="Status: PAGAMENTO APROVADO! ✅", foreground='green')
                    messagebox.showinfo("Aprovado!", "Pagamento aprovado! Acesso liberado!")
                    
                    # Atualizar aba de acesso
                    self.atualizar_aba_acesso()
                    
                    # Habilitar botão de entrar
                    self.btn_entrar.config(state='normal')
                    
                elif status == 'pendente':
                    self.status_label.config(text="Status: Pagamento pendente ⏳", foreground='orange')
                    messagebox.showinfo("Pendente", "Pagamento ainda não confirmado. Tente novamente em alguns minutos.")
                    
                else:
                    self.status_label.config(text=f"Status: {status}", foreground='red')
                    messagebox.showwarning("Status", f"Status do pagamento: {status}")
                    
            else:
                messagebox.showerror("Erro", resultado['erro'])
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar pagamento: {str(e)}")
    
    def atualizar_aba_acesso(self):
        """Atualiza informações na aba de acesso"""
        if not self.usuario_logado:
            return
        
        try:
            dados = self.sistema_pg.obter_dados_usuario(self.usuario_logado['id'])
            
            if dados:
                self.info_nome_label.config(text=f"Nome: {dados['nome']}")
                self.info_email_label.config(text=f"Email: {dados['email']}")
                self.info_plano_label.config(text=f"Plano: {dados['plano'].upper()}")
                
                if dados['acesso_liberado']:
                    self.status_acesso_label.config(text="Status: ✅ ACESSO LIBERADO", foreground='green')
                    self.btn_entrar.config(state='normal')
                    self.btn_verificar_auto.config(state='disabled')
                else:
                    self.status_acesso_label.config(text="Status: ❌ AGUARDANDO PAGAMENTO", foreground='red')
                    self.btn_entrar.config(state='disabled')
                    self.btn_verificar_auto.config(state='normal')
                
                self.data_cadastro_label.config(text=f"Cadastro: {dados['data_cadastro']}")
                
                if dados['data_expiracao']:
                    self.data_expiracao_label.config(text=f"Expiração: {dados['data_expiracao']}")
                else:
                    self.data_expiracao_label.config(text="Expiração: ---")
                    
        except Exception as e:
            print(f"Erro ao atualizar aba de acesso: {str(e)}")
    
    def iniciar_verificacao_auto(self):
        """Inicia verificação automática de pagamento"""
        if not self.usuario_logado:
            return
        
        def verificar():
            for i in range(10):  # Verificar por 50 segundos (10 x 5 segundos)
                try:
                    sucesso, resultado = self.sistema_pg.verificar_status_pagamento_pagbank(self.usuario_logado['id'])
                    
                    if sucesso and resultado.get('status') == 'aprovado':
                        self.janela.after(0, lambda: messagebox.showinfo("Aprovado!", "Pagamento aprovado! Acesso liberado!"))
                        self.janela.after(0, self.atualizar_aba_acesso)
                        break
                        
                except:
                    pass
                
                time.sleep(5)  # Esperar 5 segundos
            
            self.janela.after(0, lambda: self.btn_verificar_auto.config(state='normal', text="🔄 Verificar Status Automaticamente"))
        
        self.btn_verificar_auto.config(state='disabled', text="⏳ Verificando...")
        
        thread = threading.Thread(target=verificar, daemon=True)
        thread.start()
    
    def entrar_sistema(self):
        """Entra no sistema principal"""
        if not self.usuario_logado:
            messagebox.showerror("Erro", "Cadastre-se e pague para acessar!")
            return
        
        try:
            sucesso, resultado = self.sistema_pg.verificar_login(
                self.usuario_logado['email'], 
                self.senha_entry.get() if hasattr(self, 'senha_entry') else ""
            )
            
            if sucesso and resultado.get('acesso_liberado'):
                self.janela.destroy()
                self.callback_sucesso(resultado)
            else:
                messagebox.showerror("Erro", "Acesso não liberado. Verifique seu pagamento.")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao entrar: {str(e)}")
    
    def executar(self):
        self.janela.mainloop()
