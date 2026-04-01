# 🪶 planilhas.com - Sistema Completo com PagBank

## 🚀 Como Executar

### Opção 1: Sistema Completo (Recomendado)
```cmd
executar_sistema_completo.bat
```

### Opção 2: Apenas PagBank
```cmd
python menu_principal_pagbank.py
```

### Opção 3: Testar PagBank
```cmd
python testar_pagbank.py
```

## 🔐 Credenciais Configuradas

### PagBank (Sandbox)
- **Client ID**: `16a9aa69-d7e4-42c7-9688-ed95ac1e47cf`
- **Client Secret**: `5b77fe6e4bb0b273825a39cf3919dc700987-52dd-45fa-9d9c-29137dd10a7c`
- **Ambiente**: `sandbox`
- **Email**: `santossilvac992@gmail.com`

## ✅ Sistema Implementado

### 🎯 Fluxo Completo
1. **Cadastro** → Usuário se cadastra no sistema
2. **Pagamento** → Gera PIX automaticamente via PagBank
3. **Liberação** → Acesso liberado após confirmação
4. **Login** → Acesso controlado por pagamento

### 🔥 Funcionalidades

#### 📱 Tela de Cadastro e Pagamento
- ✅ Formulário completo de cadastro
- ✅ Escolha de planos (Mensal/Trimestral/Anual)
- ✅ Geração automática de QR Code PIX
- ✅ Verificação automática de pagamento
- ✅ Status em tempo real

#### 💳 Pagamento PagBank
- ✅ Autenticação automática
- ✅ Geração de cobrança PIX
- ✅ QR Code integrado
- ✅ Verificação de status
- ✅ Liberação automática

#### 🔐 Controle de Acesso
- ✅ Login bloqueado até pagamento
- ✅ Liberação automática após aprovação
- ✅ Controle de expiração
- ✅ Sistema offline/online

#### 📊 Sistema Principal
- ✅ Menu com acesso aos sistemas
- ✅ Gerenciamento de usuários
- ✅ Navegação entre sistemas
- ✅ Status online/offline

## 🗂️ Estrutura de Arquivos

```
planilhas.com/
├── menu_principal_pagbank.py      # Menu principal com PagBank
├── sistema_pagamento_pagbank.py   # Sistema de pagamento PagBank
├── tela_pagamento.py             # Interface cadastro/pagamento
├── testar_pagbank.py             # Testes da API PagBank
├── config_pagamento.json         # Configurações PagBank
├── executar_sistema_completo.bat # Script de instalação/execução
├── requirements.txt              # Dependências Python
├── sistema.py                  # Sistema original
├── sistema_plus.py             # Sistema PLUS
├── usuarios.db                 # Banco de usuários local
├── sistema_pagamento.db        # Banco de pagamentos
└── README_PAGBANK.md           # Este arquivo
```

## 📋 Planos Disponíveis

### 🥉 Plano Mensal
- **Valor**: R$ 97,00
- **Validade**: 30 dias
- **Descrição**: Acesso mensal ao sistema

### 🥈 Plano Trimestral  
- **Valor**: R$ 267,00
- **Validade**: 90 dias
- **Desconto**: 10% (economia R$ 24,00)
- **Descrição**: Acesso trimestral com desconto

### 🥇 Plano Anual
- **Valor**: R$ 897,00
- **Validade**: 365 dias
- **Desconto**: 30% (economia R$ 267,00)
- **Descrição**: Acesso anual com super desconto

## 🔧 Como Funciona

### 1. Cadastro
- Preenche nome, email, senha
- Sistema cria usuário bloqueado
- Redireciona para pagamento

### 2. Pagamento
- Escolhe plano desejado
- Sistema gera QR Code PIX
- Usuário escaneia e paga

### 3. Liberação
- Sistema verifica aprovação
- Acesso liberado automaticamente
- Usuário pode usar o sistema

### 4. Acesso
- Login validado por pagamento
- Controle de data de expiração
- Sistema online/offline automático

## 🧪 Testes

Para testar a integração:
```cmd
python testar_pagbank.py
```

O teste verifica:
- ✅ Conexão com PagBank
- ✅ Geração de token
- ✅ Cadastro de usuário
- ✅ Geração de PIX
- ✅ Verificação de status

## 🛡️ Segurança

- ✅ Senhas com hash SHA-256
- ✅ Autenticação segura PagBank
- ✅ Controle de acesso por pagamento
- ✅ Validação de expiração
- ✅ Sistema offline/online

## 🚀 Para Produção

Para usar em produção:

1. **Alterar ambiente** em `config_pagamento.json`:
```json
"ambiente": "producao"
```

2. **Configurar webhook** para notificações automáticas

3. **Atualizar chave PIX** para sua chave real

4. **Testar thoroughly** antes de ir para produção

## 🎯 Próximos Passos

- [ ] Configurar webhook PagBank
- [ ] Implementar notificações automáticas
- [ ] Adicionar outros métodos de pagamento
- [ ] Sistema de assinatura recorrente
- [ ] Painel administrativo completo

---

## 🎉 Sistema 100% Funcional!

✅ **Cadastro → Pagamento → Liberação** implementado  
✅ **PagBank integrado** com credenciais reais  
✅ **PIX automático** com QR Code  
✅ **Controle de acesso** por pagamento  
✅ **Interface profissional** e intuitiva  
✅ **Testes automatizados** para validação  

**Execute `executar_sistema_completo.bat` para começar!** 🚀
