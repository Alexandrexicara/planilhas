@echo off
echo ============================================
echo 🚀 INSTALAÇÃO - planilhas.com
echo ============================================
echo.

echo 🔧 Instalando dependências Python...
"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" -m pip install -r requirements.txt

echo.
echo ✅ Dependências instaladas com sucesso!
echo.

echo 📝 Configurando sistema...
echo.
echo ⚠️  ATENÇÃO: Você precisa configurar o arquivo config_pagamento.json
echo    com suas credenciais do Mercado Pago
echo.

echo 🚀 Iniciando sistema...
"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" menu_principal_completo.py

pause
