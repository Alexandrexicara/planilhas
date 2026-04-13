@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo 🚀 Gerando EXE para desktop...
echo.

REM Ativa o virtual environment
call .venv\Scripts\activate.bat

REM Gera o executável com PyInstaller
echo ⏳ Compilando app.py...
pyinstaller --onefile --windowed --name=SistemaPlanilhas app.py

REM Verifica se foi criado
if exist "dist\SistemaPlanilhas.exe" (
    echo ✅ EXE gerado com sucesso!
    
    REM Copia para Desktop
    for /f "tokens=*" %%A in ('powershell $([System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop))') do set DESKTOP=%%A
    
    copy "dist\SistemaPlanilhas.exe" "!DESKTOP!\SistemaPlanilhas.exe"
    
    echo 📁 Copiado para: !DESKTOP!\SistemaPlanilhas.exe
    echo 🎯 Acesse o atalho na área de trabalho!
    echo.
    pause
) else (
    echo ❌ Erro: EXE não foi criado
    pause
)
