import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from usuarios_db import autenticar_usuario, criar_usuario, inicializar_banco_usuarios

class GerenciamentoUsuarios:
    def __init__(self, janela_pai):
        self.janela_pai = janela_pai
        self.janela = tk.Toplevel(janela_pai)
        self.janela.title("👥 Gerenciamento de Usuários")
        self.janela.geometry("800x600")
        self.janela.resizable(True, True)
        self.janela.transient(janela_pai)
        self.janela.grab_set()
        
        # Centralizar janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (600 // 2)
        self.janela.geometry(f"800x600+{x}+{y}")
        
        self.criar_interface()
        self.carregar_usuarios()
        
    def criar_interface(self):
        # Frame principal
        frame_principal = ttk.Frame(self.janela, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(frame_principal, text="👥 Gerenciamento de Usuários", 
                          font=("Arial", 16, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Frame de botões superiores
        frame_botoes_top = ttk.Frame(frame_principal)
        frame_botoes_top.pack(fill='x', pady=(0, 20))
        
        ttk.Button(frame_botoes_top, text="➕ Novo Usuário", 
                  command=self.abrir_formulario_usuario).pack(side='left', padx=(0, 10))
        ttk.Button(frame_botoes_top, text="🔄 Atualizar Lista", 
                  command=self.carregar_usuarios).pack(side='left', padx=(0, 10))
        ttk.Button(frame_botoes_top, text="❌ Fechar", 
                  command=self.janela.destroy).pack(side='right')
        
        # Frame da tabela
        frame_tabela = ttk.Frame(frame_principal)
        frame_tabela.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para lista de usuários
        colunas = ('id', 'nome', 'email', 'nivel_acesso', 'data_cadastro', 'ativo')
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show='headings', height=15)
        
        # Configurar colunas
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.heading('email', text='Email')
        self.tree.heading('nivel_acesso', text='Nível')
        self.tree.heading('data_cadastro', text='Cadastro')
        self.tree.heading('ativo', text='Status')
        
        # Largura das colunas
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('nome', width=150)
        self.tree.column('email', width=200)
        self.tree.column('nivel_acesso', width=80, anchor='center')
        self.tree.column('data_cadastro', width=120)
        self.tree.column('ativo', width=60, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame de botões de ação
        frame_acoes = ttk.Frame(frame_principal)
        frame_acoes.pack(fill='x', pady=(10, 0))
        
        ttk.Button(frame_acoes, text="✏️ Editar", 
                  command=self.editar_usuario).pack(side='left', padx=(0, 10))
        ttk.Button(frame_acoes, text="🔓 Resetar Senha", 
                  command=self.resetar_senha).pack(side='left', padx=(0, 10))
        ttk.Button(frame_acoes, text="🔄 Ativar/Desativar", 
                  command=self.toggle_ativo).pack(side='left', padx=(0, 10))
        ttk.Button(frame_acoes, text="🗑️ Excluir", 
                  command=self.excluir_usuario).pack(side='left')
        
    def carregar_usuarios(self):
        """Carrega usuários do banco de dados"""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn, cursor = inicializar_banco_usuarios()
        
        try:
            cursor.execute("""
            SELECT id, nome, email, nivel_acesso, data_cadastro, ativo 
            FROM usuarios 
            ORDER BY id DESC
            """)
            
            usuarios = cursor.fetchall()
            
            for usuario in usuarios:
                status = "✅ Ativo" if usuario[5] == 1 else "❌ Inativo"
                nivel = "🔑 Admin" if usuario[3] == 'admin' else "👤 Usuário"
                
                self.tree.insert('', 'end', values=(
                    usuario[0],  # id
                    usuario[1],  # nome
                    usuario[2],  # email
                    nivel,       # nivel_acesso
                    usuario[4],  # data_cadastro
                    status       # ativo
                ))
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar usuários: {str(e)}")
        finally:
            conn.close()
    
    def abrir_formulario_usuario(self, usuario_id=None):
        """Abre formulário para criar/editar usuário"""
        FormularioUsuario(self.janela, usuario_id, self.carregar_usuarios)
    
    def editar_usuario(self):
        """Edita usuário selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar!")
            return
        
        item = self.tree.item(selecionado[0])
        usuario_id = item['values'][0]
        self.abrir_formulario_usuario(usuario_id)
    
    def resetar_senha(self):
        """Reseta senha do usuário selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para resetar a senha!")
            return
        
        item = self.tree.item(selecionado[0])
        usuario_id = item['values'][0]
        nome = item['values'][1]
        
        if messagebox.askyesno("Resetar Senha", 
                              f"Deseja resetar a senha do usuário '{nome}'?\n\nNova senha será: '123456'"):
            try:
                conn, cursor = inicializar_banco_usuarios()
                
                # Hash da nova senha
                nova_senha_hash = hashlib.sha256("123456".encode()).hexdigest()
                
                cursor.execute("""
                UPDATE usuarios 
                SET senha = ? 
                WHERE id = ?
                """, (nova_senha_hash, usuario_id))
                
                conn.commit()
                messagebox.showinfo("Sucesso", f"Senha do usuário '{nome}' resetada para: 123456")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao resetar senha: {str(e)}")
            finally:
                conn.close()
    
    def toggle_ativo(self):
        """Ativa/desativa usuário selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para ativar/desativar!")
            return
        
        item = self.tree.item(selecionado[0])
        usuario_id = item['values'][0]
        nome = item['values'][1]
        status_atual = "Ativo" in item['values'][5]
        
        nova_status = "desativar" if status_atual else "ativar"
        
        if messagebox.askyesno("Alterar Status", 
                              f"Deseja {nova_status} o usuário '{nome}'?"):
            try:
                conn, cursor = inicializar_banco_usuarios()
                
                novo_ativo = 0 if status_atual else 1
                
                cursor.execute("""
                UPDATE usuarios 
                SET ativo = ? 
                WHERE id = ?
                """, (novo_ativo, usuario_id))
                
                conn.commit()
                self.carregar_usuarios()
                messagebox.showinfo("Sucesso", f"Usuário '{nome}' {nova_status}do com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao alterar status: {str(e)}")
            finally:
                conn.close()
    
    def excluir_usuario(self):
        """Exclui usuário selecionado"""
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para excluir!")
            return
        
        item = self.tree.item(selecionado[0])
        usuario_id = item['values'][0]
        nome = item['values'][1]
        
        if messagebox.askyesno("Excluir Usuário", 
                              f"Tem certeza que deseja excluir o usuário '{nome}'?\n\nEsta ação não pode ser desfeita!"):
            try:
                conn, cursor = inicializar_banco_usuarios()
                
                cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
                conn.commit()
                
                self.carregar_usuarios()
                messagebox.showinfo("Sucesso", f"Usuário '{nome}' excluído com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir usuário: {str(e)}")
            finally:
                conn.close()

class FormularioUsuario:
    def __init__(self, janela_pai, usuario_id=None, callback_atualizar=None):
        self.janela_pai = janela_pai
        self.usuario_id = usuario_id
        self.callback_atualizar = callback_atualizar
        
        self.janela = tk.Toplevel(janela_pai)
        self.janela.title("➕ Novo Usuário" if not usuario_id else "✏️ Editar Usuário")
        self.janela.geometry("400x350")
        self.janela.resizable(False, False)
        self.janela.transient(janela_pai)
        self.janela.grab_set()
        
        # Centralizar janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (350 // 2)
        self.janela.geometry(f"400x350+{x}+{y}")
        
        self.criar_interface()
        
        if usuario_id:
            self.carregar_dados_usuario()
    
    def criar_interface(self):
        # Frame principal
        frame_principal = ttk.Frame(self.janela, padding="20")
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(frame_principal, 
                          text="➕ Novo Usuário" if not self.usuario_id else "✏️ Editar Usuário", 
                          font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 20))
        
        # Nome
        ttk.Label(frame_principal, text="Nome:").pack(anchor='w', pady=(0, 5))
        self.nome_entry = ttk.Entry(frame_principal, width=40)
        self.nome_entry.pack(fill='x', pady=(0, 15))
        
        # Email
        ttk.Label(frame_principal, text="Email:").pack(anchor='w', pady=(0, 5))
        self.email_entry = ttk.Entry(frame_principal, width=40)
        self.email_entry.pack(fill='x', pady=(0, 15))
        
        # Senha
        ttk.Label(frame_principal, text="Senha:").pack(anchor='w', pady=(0, 5))
        self.senha_entry = ttk.Entry(frame_principal, width=40, show="*")
        self.senha_entry.pack(fill='x', pady=(0, 15))
        
        # Nível de acesso
        ttk.Label(frame_principal, text="Nível de Acesso:").pack(anchor='w', pady=(0, 5))
        self.nivel_var = tk.StringVar(value="usuario")
        frame_nivel = ttk.Frame(frame_principal)
        frame_nivel.pack(fill='x', pady=(0, 15))
        
        ttk.Radiobutton(frame_nivel, text="👤 Usuário", variable=self.nivel_var, 
                       value="usuario").pack(side='left', padx=(0, 20))
        ttk.Radiobutton(frame_nivel, text="🔑 Administrador", variable=self.nivel_var, 
                       value="admin").pack(side='left')
        
        # Status (apenas para edição)
        if self.usuario_id:
            self.ativo_var = tk.BooleanVar(value=True)
            self.check_ativo = ttk.Checkbutton(frame_principal, text="Usuário Ativo", 
                                               variable=self.ativo_var)
            self.check_ativo.pack(anchor='w', pady=(0, 20))
        
        # Botões
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(fill='x')
        
        ttk.Button(frame_botoes, text="💾 Salvar", 
                  command=self.salvar_usuario).pack(side='left', padx=(0, 10))
        ttk.Button(frame_botoes, text="❌ Cancelar", 
                  command=self.janela.destroy).pack(side='left')
    
    def carregar_dados_usuario(self):
        """Carrega dados do usuário para edição"""
        conn, cursor = inicializar_banco_usuarios()
        
        try:
            cursor.execute("""
            SELECT nome, email, nivel_acesso, ativo 
            FROM usuarios 
            WHERE id = ?
            """, (self.usuario_id,))
            
            usuario = cursor.fetchone()
            
            if usuario:
                self.nome_entry.insert(0, usuario[0])
                self.email_entry.insert(0, usuario[1])
                self.nivel_var.set(usuario[2])
                self.ativo_var.set(usuario[3] == 1)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar usuário: {str(e)}")
        finally:
            conn.close()
    
    def salvar_usuario(self):
        """Salva usuário (cria ou atualiza)"""
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()
        nivel = self.nivel_var.get()
        
        # Validações
        if not nome or not email:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        if not self.usuario_id and not senha:
            messagebox.showerror("Erro", "Senha é obrigatória para novos usuários!")
            return
        
        if senha and len(senha) < 4:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 4 caracteres!")
            return
        
        conn, cursor = inicializar_banco_usuarios()
        
        try:
            if self.usuario_id:
                # Atualizar usuário existente
                if senha:
                    # Atualizar com nova senha
                    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                    cursor.execute("""
                    UPDATE usuarios 
                    SET nome = ?, email = ?, nivel_acesso = ?, senha = ?, ativo = ?
                    WHERE id = ?
                    """, (nome, email, nivel, senha_hash, 
                          1 if self.ativo_var.get() else 0, self.usuario_id))
                else:
                    # Atualizar sem alterar senha
                    cursor.execute("""
                    UPDATE usuarios 
                    SET nome = ?, email = ?, nivel_acesso = ?, ativo = ?
                    WHERE id = ?
                    """, (nome, email, nivel, 
                          1 if self.ativo_var.get() else 0, self.usuario_id))
                
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            else:
                # Criar novo usuário
                sucesso, mensagem = criar_usuario(nome, email, senha, nivel)
                
                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                else:
                    messagebox.showerror("Erro", mensagem)
                    return
            
            conn.commit()
            
            # Fechar formulário
            self.janela.destroy()
            
            # Atualizar lista
            if self.callback_atualizar:
                self.callback_atualizar()
                
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este email já está cadastrado!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar usuário: {str(e)}")
        finally:
            conn.close()

# Import necessário para hash
import hashlib
