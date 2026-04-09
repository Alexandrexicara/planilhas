@echo off
echo ========================================
echo Adicionando Python 3.13 ao PATH
echo ========================================
echo.

:: Caminhos padrão de instalação do Python 3.13
set PYTHON_PATHS=C:\Python313;C:\Python313\Scripts;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\Scripts

:: Verificar se Python 3.13 existe nos caminhos padrão
set PYTHON_FOUND=0
for %%P in (%PYTHON_PATHS%) do (
    if exist "%%P\python.exe" (
        echo [OK] Python 3.13 encontrado em: %%P
        set PYTHON_FOUND=1
        set PYTHON_DIR=%%P
    )
)

if %PYTHON_FOUND%==0 (
    echo [ERRO] Python 3.13 nao encontrado nos caminhos padrao
    echo.
    echo Por favor, verifique onde instalou o Python 3.13
    echo Caminhos verificados:
    echo %PYTHON_PATHS%
    echo.
    echo Se instalou em outro local, edite este script e adicione o caminho correto
    pause
    exit /b 1
)

echo.
echo Adicionando ao PATH do usuario...
setx PATH "%PATH%;%PYTHON_DIR%;%PYTHON_DIR%\Scripts"

echo.
echo [OK] Python 3.13 adicionado ao PATH
echo.
echo IMPORTANTE: Feche e abra o PowerShell novamente para as alteracoes terem efeito
echo.
pause
