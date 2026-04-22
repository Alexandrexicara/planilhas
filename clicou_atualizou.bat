@echo off
setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0"
if exist "%PROJECT_DIR%app.py" goto :project_ok
if exist "E:\planilhas.com\app.py" set "PROJECT_DIR=E:\planilhas.com\"
if exist "C:\planilhas.com\app.py" set "PROJECT_DIR=C:\planilhas.com\"

:project_ok
cd /d "%PROJECT_DIR%"
if not exist "app.py" (
  echo ERRO: pasta do projeto nao encontrada.
  echo Coloque este .bat na pasta do projeto ou ajuste PROJECT_DIR.
  pause
  exit /b 1
)

echo ==========================================
echo PLANILHAS - ATUALIZACAO EM 1 CLIQUE
echo ==========================================
echo Pasta do projeto: %cd%
echo.

if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
)

set "PY_CMD="
if exist ".venv\Scripts\python.exe" (
  set "PY_CMD=.venv\Scripts\python.exe"
) else (
  where python >nul 2>nul
  if not errorlevel 1 (
    set "PY_CMD=python"
  ) else (
    where py >nul 2>nul
    if not errorlevel 1 (
      set "PY_CMD=py -3"
    )
  )
)

if not defined PY_CMD (
  echo ERRO: Python nao encontrado.
  echo Instale o Python ou crie a .venv em %cd%.
  pause
  exit /b 1
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
echo [2/2] Verificando compilacao...

if not exist "dist\Planilhas.exe" (
  echo.
  echo ERRO: dist\Planilhas.exe nao foi gerado.
  pause
  exit /b 1
)

echo ✅ Planilhas.exe gerado com sucesso!

set "DESKTOP=%USERPROFILE%\Desktop"
set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if not exist "releases" mkdir "releases"

copy /y "dist\Planilhas.exe" "releases\Planilhas.exe" >nul
copy /y "dist\Planilhas.exe" "%DESKTOP%\Planilhas.exe" >nul

rem Apenas Planilhas.exe - sem debug

echo.
echo OK: Atualizacao concluida.
echo Arquivos atualizados:
echo - %cd%\dist\Planilhas.exe
echo - %cd%\releases\Planilhas.exe
echo - %DESKTOP%\Planilhas.exe
echo.

echo.
echo ✅ Atualizacao concluida com sucesso!
echo Execute: %DESKTOP%\Planilhas.exe

pause
