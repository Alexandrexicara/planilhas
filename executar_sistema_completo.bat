@echo off
echo ============================================
echo 🚀 SISTEMA COMPLETO - planilhas.com
echo ============================================
echo.
echo 🔧 Instalando dependências Python...
"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" -m pip install -r requirements.txt

echo.
echo ✅ Dependências instaladas com sucesso!
echo.

echo 📝 Configuração:
echo    • API PagBank: Configurada
echo    • Email: santossilvac992@gmail.com
echo    • Ambiente: Sandbox (testes)
echo.

echo 🚀 Iniciando sistema completo...
"C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python314\python.exe" menu_principal_pagbank.py

pause
