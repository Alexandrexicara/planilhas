# Deploy no PythonAnywhere com Python 3.13.12

## Configuração do Projeto

### 1. Arquivo runtime.txt
✅ Já criado - especifica Python 3.13.12

### 2. requirements.txt
✅ Já configurado com as dependências necessárias

## Passo a Passo no PythonAnywhere

### 1. Criar Conta
- Acesse: https://www.pythonanywhere.com/
- Crie uma conta (gratuita ou paga)

### 2. Criar Web App
1. Vá em "Web" → "Add a new web app"
2. Escolha "Manual configuration"
3. Selecione "Python 3.13"
4. Escolha domínio (ex: seu-usuario.pythonanywhere.com)

### 3. Upload do Código
```bash
# No PythonAnywhere (Bash console)
cd ~/myproject
git clone https://github.com/seu-usuario/planilhas.com.git
# OU
# Faça upload dos arquivos via SFTP ou interface web
```

### 4. Configurar Virtual Environment
```bash
cd ~/myproject
mkvirtualenv --python=/usr/bin/python3.13 myenv
source ~/myenv/bin/activate
pip install -r requirements.txt
```

### 5. Configurar Web App
- Em "Web" → "Code" → "Source code": `/home/seu-usuario/myproject`
- "Working directory": `/home/seu-usuario/myproject`
- "WSGI configuration file": `/home/seu-usuario/myproject/wsgi.py`

### 6. Criar arquivo wsgi.py
```python
import sys
sys.path.insert(0, '/home/seu-usuario/myproject')

from menu_principal import app
application = app
```

### 7. Arquivos Estáticos
- Em "Web" → "Static files"
- URL: `/static/`
- Directory: `/home/seu-usuario/myproject/static/`

### 8. Atualizar Banco de Dados
```bash
cd ~/myproject
python sistema.py
```

### 9. Reiniciar Web App
- Em "Web" → "Reload"

## Diferença Local vs PythonAnywhere

### Local (seu PC):
- Python 3.14.3 (já instalado)
- Funciona normalmente

### PythonAnywhere:
- Python 3.13.12 (especificado em runtime.txt)
- Usa as mesmas dependências do requirements.txt

## Troubleshooting

### Se der erro de versão:
```bash
# No PythonAnywhere
python3.13 --version  # Deve mostrar 3.13.12
```

### Se faltar dependências:
```bash
pip install -r requirements.txt
```

### Se o banco de dados não funcionar:
```bash
# O SQLite funciona no PythonAnywhere sem configuração extra
# Certifique-se que o arquivo banco.db está no projeto
```

## Deploy Automático (Git)

```bash
# Local
git add .
git commit -m "Deploy PythonAnywhere Python 3.13.12"
git push

# PythonAnywhere
cd ~/myproject
git pull
source ~/myenv/bin/activate
pip install -r requirements.txt
# Reiniciar web app na interface
```

## Suporte
Se tiver problemas, verifique:
1. Logs em "Web" → "Log files"
2. Versão do Python: `python --version`
3. Dependências instaladas: `pip list`
