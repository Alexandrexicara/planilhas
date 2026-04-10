@echo off
cls
echo ====================================
echo  🚀 SISTEMA PLUS - ACESSO DIRETO
echo ====================================
echo.

echo 📋 Abrindo menu principal...
echo.

powershell -ExecutionPolicy Bypass -File ".\menu.ps1"

if errorlevel 1 (
    echo.
    echo [ERRO] Nao foi possivel abrir o menu.ps1
    echo.
    echo Tentando alternatives...
    echo.
    echo Opcao 1: python sistema_plus.py
    python sistema_plus.py
)

echo.
echo ====================================
