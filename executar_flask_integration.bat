@echo off
echo ====================================
echo  Sistema Plus - Flask Integration
echo ====================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

echo Verificando banco de dados PLUS...
if not exist "banco_plus.db" (
    echo [AVISO] banco_plus.db nao encontrado. O sistema criara automaticamente.
)

echo.
echo Instalando dependencias Flask...
pip install flask werkzeug openpyxl pillow >nul 2>&1

echo.
echo Iniciando Flask com integracao ao Sistema Plus...
echo.
echo ====================================
echo  Sistema disponivel em:
echo  - Local: http://localhost:5000
echo  - Rede: http://0.0.0.0:5000
echo ====================================
echo.
echo 📊 Conectado ao banco: banco_plus.db
echo 🐍 Integrado com: sistema_plus.py
echo 🖼️  Extrator: extrator_imagens_excel.py
echo.
echo Pressione Ctrl+C para parar o servidor
echo ====================================
echo.

python flask_integration.py

pause
