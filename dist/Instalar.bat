@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Instalar Planilhas
C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -ExecutionPolicy Bypass -File "Instalar.ps1"
pause
