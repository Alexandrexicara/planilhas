@echo off
echo ====================================
echo  Sistema Plus - Web Interface
echo ====================================
echo.

echo Verificando Python...
python --version
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    pause
    exit /b 1
)

echo.
echo Iniciando servidor web...
echo.
echo ====================================
echo  Sistema disponivel em:
echo  - Local: http://localhost:8000
echo  - Rede: http://0.0.0.0:8000
echo ====================================
echo.
echo Recursos disponiveis:
echo  - Pagina inicial com design moderno
echo  - Sistema de R$5.000 por R$4.500  
echo  - Interface de upload
echo  - Catalogo de produtos
echo.
echo Pressione Ctrl+C para parar
echo ====================================
echo.

python simple_app.py

pause
