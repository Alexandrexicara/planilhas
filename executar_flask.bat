@echo off
echo ====================================
echo  Sistema Plus - Flask Web Server
echo ====================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale o Python antes de continuar.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [AVISO] Algumas dependencias podem nao ter sido instaladas
)

echo.
echo Iniciando servidor Flask...
echo.
echo ====================================
echo  Sistema disponivel em:
echo  - Local: http://localhost:5000
echo  - Rede: http://0.0.0.0:5000
echo ====================================
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python start_flask.py

pause
