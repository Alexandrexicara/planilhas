@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ==========================================
echo PLANILHAS - ATUALIZACAO EM 1 CLIQUE
echo ==========================================
echo Pasta do projeto: %cd%
echo.

set "PY_CMD=python"
where python >nul 2>nul
if errorlevel 1 (
  where py >nul 2>nul
  if errorlevel 1 (
    echo ERRO: Python nao encontrado.
    echo Instale o Python e tente novamente.
    pause
    exit /b 1
  )
  set "PY_CMD=py -3"
)

if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
)

if not exist "icon.ico" (
  if exist "static\branding\logo-planilhas.png" (
    echo Criando icon.ico a partir do logo...
    %PY_CMD% -c "from PIL import Image; im=Image.open('static/branding/logo-planilhas.png').convert('RGBA'); im.save('icon.ico', format='ICO', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])"
  )
)

echo Limpando build anterior...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

echo.
echo [1/2] Compilando Planilhas.exe...
%PY_CMD% -m PyInstaller --noconfirm --clean --onefile --windowed --name Planilhas --icon icon.ico --add-data "templates;templates" --add-data "static;static" --add-data "banco_plus.db;." --add-data "banco.db;." --add-data "usuarios.db;." --collect-all flask --collect-all werkzeug --collect-all jinja2 --collect-all openpyxl --hidden-import sistema --hidden-import sistema_plus --hidden-import menu_principal --hidden-import usuarios_db --hidden-import gerenciamento_usuarios --hidden-import sistema_online_offline --hidden-import banco_offline app.py

if errorlevel 1 (
  echo.
  echo ERRO: falha na compilacao do Planilhas.exe.
  pause
  exit /b 1
)

echo.
echo [2/2] Compilando Planilhas_debug.exe...
%PY_CMD% -m PyInstaller --noconfirm --onefile --console --name Planilhas_debug --icon icon.ico --add-data "templates;templates" --add-data "static;static" --add-data "banco_plus.db;." --add-data "banco.db;." --add-data "usuarios.db;." --collect-all flask --collect-all werkzeug --collect-all jinja2 --collect-all openpyxl --hidden-import sistema --hidden-import sistema_plus --hidden-import menu_principal --hidden-import usuarios_db --hidden-import gerenciamento_usuarios --hidden-import sistema_online_offline --hidden-import banco_offline app.py

if errorlevel 1 (
  echo.
  echo ERRO: falha na compilacao do Planilhas_debug.exe.
  pause
  exit /b 1
)

if not exist "dist\Planilhas.exe" (
  echo.
  echo ERRO: dist\Planilhas.exe nao foi gerado.
  pause
  exit /b 1
)

if not exist "dist\Planilhas_debug.exe" (
  echo.
  echo ERRO: dist\Planilhas_debug.exe nao foi gerado.
  pause
  exit /b 1
)

set "DESKTOP=%USERPROFILE%\Desktop"
set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if not exist "releases" mkdir "releases"

copy /y "dist\Planilhas.exe" "releases\Planilhas.exe" >nul
copy /y "dist\Planilhas_debug.exe" "releases\Planilhas_debug.exe" >nul
copy /y "dist\Planilhas.exe" "%DESKTOP%\Planilhas.exe" >nul
copy /y "dist\Planilhas_debug.exe" "%DESKTOP%\Planilhas_debug.exe" >nul

(
  echo @echo off
  echo setlocal
  echo set "EXE_PATH=%%~dp0Planilhas_debug.exe"
  echo set "PS_EXE=%%SystemRoot%%\System32\WindowsPowerShell\v1.0\powershell.exe"
  echo if not exist "%%EXE_PATH%%" ^(
  echo   echo Nao encontrei "%%EXE_PATH%%".
  echo   pause
  echo   exit /b 1
  echo ^)
  echo if not exist "%%PS_EXE%%" ^(
  echo   echo Nao encontrei o PowerShell em "%%PS_EXE%%".
  echo   pause
  echo   exit /b 1
  echo ^)
  echo "%%PS_EXE%%" -NoExit -ExecutionPolicy Bypass -Command "$env:AUTO_OPEN_BROWSER='1'; ^& '%%EXE_PATH%%'"
) > "releases\abrir_planilhas_debug_powershell.bat"

copy /y "releases\abrir_planilhas_debug_powershell.bat" "%DESKTOP%\abrir_planilhas_debug_powershell.bat" >nul

echo.
echo OK: Atualizacao concluida.
echo Arquivos atualizados:
echo - %cd%\dist\Planilhas.exe
echo - %cd%\dist\Planilhas_debug.exe
echo - %cd%\releases\Planilhas.exe
echo - %cd%\releases\Planilhas_debug.exe
echo - %DESKTOP%\Planilhas.exe
echo - %DESKTOP%\Planilhas_debug.exe
echo - %DESKTOP%\abrir_planilhas_debug_powershell.bat
echo.

if exist "%DESKTOP%\abrir_planilhas_debug_powershell.bat" (
  echo Abrindo Planilhas_debug automaticamente...
  start "" "%DESKTOP%\abrir_planilhas_debug_powershell.bat"
)

pause
