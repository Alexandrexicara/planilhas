@echo off
echo ========================================
echo Configurando Python 3.13 para o projeto
echo ========================================
echo.

:: Verificar se Python 3.13 está instalado
py -3.13 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python 3.13 nao encontrado no sistema!
    echo Por favor, instale o Python 3.13 primeiro:
    echo https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

echo [OK] Python 3.13 encontrado
py -3.13 --version
echo.

:: Remover virtual environment antigo se existir
if exist .venv (
    echo Removendo virtual environment antigo...
    rmdir /s /q .venv
)

:: Criar novo virtual environment com Python 3.13
echo Criando virtual environment com Python 3.13...
py -3.13 -m venv .venv

if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar virtual environment
    pause
    exit /b 1
)

echo [OK] Virtual environment criado
echo.

:: Ativar virtual environment
echo Ativando virtual environment...
call .venv\Scripts\activate.bat

:: Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip

:: Instalar dependências
echo Instalando dependencias...
if exist requirements.txt (
    python -m pip install -r requirements.txt
) else (
    echo [AVISO] requirements.txt nao encontrado, instalando dependencias basicas...
    python -m pip install openpyxl pillow tk
)

echo.
echo ========================================
echo Configuracao concluida com sucesso!
echo ========================================
echo.
echo Para ativar o ambiente:
echo   .venv\Scripts\activate.bat
echo.
echo Para executar o sistema:
echo   python sistema.py
echo.
pause
