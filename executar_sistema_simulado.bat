@echo off
echo ============================================
echo 🚀 SISTEMA SIMULADO - planilhas.com
echo ============================================
echo.
echo 🔧 Instalando dependências Python...
python -m pip install -r requirements.txt

echo.
echo ✅ Dependências instaladas com sucesso!
echo.

echo 📝 Configuração:
echo    • API PagBank: SIMULADA (não precisa HTTPS)
echo    • Email: santossilvac992@gmail.com
echo    • Ambiente: Simulado (testes completos)
echo.

echo 🧪 Executando testes do sistema...
python testar_pagbank_simulado.py

echo.
echo 🚀 Iniciando sistema simulado...
python menu_principal_simulado.py

pause
