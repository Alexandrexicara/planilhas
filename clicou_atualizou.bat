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
echo Compilando Planilhas.exe...
%PY_CMD% -m PyInstaller --noconfirm --clean --onefile --windowed --name Planilhas --icon icon.ico --add-data "templates;templates" --add-data "static;static" --add-data "banco_plus.db;." --add-data "banco.db;." --add-data "usuarios.db;." --collect-all flask --collect-all werkzeug --collect-all jinja2 --collect-all openpyxl --hidden-import sistema --hidden-import sistema_plus --hidden-import menu_principal --hidden-import usuarios_db --hidden-import gerenciamento_usuarios --hidden-import sistema_online_offline --hidden-import banco_offline app.py

if errorlevel 1 (
  echo.
  echo ERRO: falha na compilacao.
  pause
  exit /b 1
)

if not exist "dist\Planilhas.exe" (
  echo.
  echo ERRO: dist\Planilhas.exe nao foi gerado.
  pause
  exit /b 1
)

if not exist "releases" mkdir "releases"
copy /y "dist\Planilhas.exe" "releases\Planilhas.exe" >nul

set "DESKTOP=%USERPROFILE%\Desktop"
copy /y "dist\Planilhas.exe" "%DESKTOP%\Planilhas.exe" >nul

echo.
echo OK: Atualizacao concluida com sucesso.
echo Arquivos atualizados:
echo - %cd%\dist\Planilhas.exe
echo - %cd%\releases\Planilhas.exe
echo - %DESKTOP%\Planilhas.exe
echo.
pause
