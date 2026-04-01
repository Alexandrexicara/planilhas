# 🪶 planilhas.com - Sistema Completo com Login

## 🚀 Como Executar

### Opção 1: PowerShell (Recomendado)
```powershell
.\menu.ps1
```

### Opção 2: Batch
```cmd
.\menu_fixed.bat
```

### Opção 3: Python Direto
```powershell
& "C:\Users\Positivo\AppData\Local\Programs\Python\Python314\python.exe" menu_principal.py
```

## 🔐 Acesso Padrão

### Administrador
- **Email**: `admin@planilhas.com`
- **Senha**: `admin123`

## ✅ Funcionalidades Implementadas

### 📋 Tela de Login
- ✅ Login com email e senha
- ✅ Validação de campos
- ✅ Sistema de hash SHA-256 para senhas

### 👤 Cadastro de Usuários
- ✅ Nome completo
- ✅ Email válido
- ✅ Senha com confirmação
- ✅ Validação de força de senha
- ✅ Limpeza automática de campos

### 🏠 Menu Principal
- ✅ Informações do usuário logado
- ✅ Nível de acesso (Admin/Usuário)
- ✅ Acesso aos sistemas (Original e PLUS)
- ✅ Botão de sair que retorna ao login

### 👥 Gerenciamento de Usuários (Apenas Admin)
- ✅ Lista completa de usuários
- ✅ Criar novos usuários
- ✅ Editar usuários existentes
- ✅ Resetar senha (padrão: 123456)
- ✅ Ativar/Desativar usuários
- ✅ Excluir usuários
- ✅ Interface profissional com TreeView

### 🔄 Navegação Entre Sistemas
- ✅ Botões nos sistemas para alternar
- ✅ Fechamento automático ao alternar
- ✅ Confirmação antes de alternar

## 🗂️ Estrutura de Arquivos

```
planilhas.com/
├── menu_principal.py          # Sistema principal com login
├── usuarios_db.py             # Banco de dados de usuários
├── gerenciamento_usuarios.py  # Interface de gerenciamento
├── menu.ps1                   # Script PowerShell
├── menu_fixed.bat             # Script Batch corrigido
├── sistema.py                 # Sistema original
├── sistema_plus.py            # Sistema PLUS
├── usuarios.db               # Banco de dados de usuários
└── README_LOGIN.md           # Este arquivo
```

## 🔧 Níveis de Acesso

### 🔑 Administrador
- Acesso total ao gerenciamento de usuários
- Pode criar, editar, excluir usuários
- Pode resetar senhas
- Acesso aos dois sistemas

### 👤 Usuário Comum
- Apenas acesso aos sistemas
- Não pode gerenciar outros usuários
- Pode alterar própria senha (via admin)

## 🛡️ Segurança

- ✅ Senhas armazenadas com hash SHA-256
- ✅ Validação de email
- ✅ Senha mínima de 4 caracteres
- ✅ Confirmação de senha no cadastro
- ✅ Sistema de ativação/desativação

## 📝 Como Usar

1. **Execute o sistema**: `.\menu.ps1`
2. **Faça login** com o usuário admin
3. **Crie novos usuários** pelo gerenciamento
4. **Acesse os sistemas** através do menu
5. **Navegue entre sistemas** usando os botões internos

## 🎯 Próximos Passos (Opcionais)

- [ ] Sistema de logs
- [ ] Backup automático
- [ ] Permissões granulares
- [ ] Recuperação de senha por email
- [ ] Autenticação de dois fatores

---
**Desenvolvido com ❤️ para planilhas.com**
