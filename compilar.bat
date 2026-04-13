@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         COMPILADOR - SISTEMA DE PLANILHAS                 ║
echo ║      (FixMemoryError do PyInstaller com Flask)            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

:menu
echo.
echo 1) 🔍 Diagnosticar ambiente (RECOMENDADO PRIMEIRA VEZ)
echo 2) 📦 Compilar versão normal (--onedir)
echo 3) ⚡ Compilar versão leve (para RAM limitada)
echo 4) 🗑️  Limpar arquivos de build anteriores
echo 5) 📖 Abrir guia de correção (CORRIGIR_MEMORY_ERROR.md)
echo 6) ❌ Sair
echo.

set /p choice="Escolha uma opção [1-6]: "

if "%choice%"=="1" (
    echo.
    echo Executando diagnóstico...
    echo.
    python diagnostico_pyinstaller.py
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo Compilando versão normal...
    echo.
    python build_exe.py
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo Compilando versão leve...
    echo.
    python build_exe_light.py
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo Limpando arquivos de build...
    if exist build rmdir /s /q build
    if exist dist rmdir /s /q dist
    del *.spec 2>nul
    echo ✓ Limpeza concluída!
    goto menu
)

if "%choice%"=="5" (
    echo.
    start notepad CORRIGIR_MEMORY_ERROR.md
    goto menu
)

if "%choice%"=="6" (
    exit /b 0
)

echo.
echo ❌ Opção inválida
goto menu
