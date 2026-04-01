@echo off
echo ============================================
echo 🚀 INICIANDO SISTEMA DE PLANILHAS FIXED
echo ============================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não está instalado!
    echo Por favor, instale o Python 3.8 ou superior.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Verificar se openpyxl está instalado
python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Instalando dependências...
    pip install openpyxl pillow
    echo.
)

echo ✅ Dependências verificadas
echo.

REM Limpar arquivos temporários
echo 🧹 Limpando arquivos temporários...
python limpar_bancos.py
echo.

REM Iniciar sistema
echo 🚀 Iniciando sistema...
echo.
python sistema_fixed.py

pause
