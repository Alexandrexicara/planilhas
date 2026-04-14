@echo off
setlocal
set "EXE_PATH=%~dp0Planilhas_debug.exe"
set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%EXE_PATH%" (
  echo Nao encontrei "%EXE_PATH%".
  pause
  exit /b 1
)
if not exist "%PS_EXE%" (
  echo Nao encontrei o PowerShell em "%PS_EXE%".
  pause
  exit /b 1
)
"%PS_EXE%" -NoExit -ExecutionPolicy Bypass -Command "$env:AUTO_OPEN_BROWSER='1'; ^& '%EXE_PATH%'"
