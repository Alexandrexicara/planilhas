@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo Gerando EXE desktop...
echo.

if exist ".venv\Scripts\activate.bat" (
  call .venv\Scripts\activate.bat
)

echo Compilando app.py...
pyinstaller --onefile --windowed --name=Planilhas ^
  --add-data "templates;templates" ^
  --add-data "static;static" ^
  --add-data "banco_plus.db;." ^
  --add-data "banco.db;." ^
  --add-data "usuarios.db;." ^
  --collect-all flask ^
  --collect-all werkzeug ^
  --collect-all jinja2 ^
  --collect-all openpyxl ^
  --hidden-import sistema ^
  --hidden-import sistema_plus ^
  --hidden-import menu_principal ^
  --hidden-import usuarios_db ^
  --hidden-import gerenciamento_usuarios ^
  --hidden-import sistema_online_offline ^
  --hidden-import banco_offline ^
  app.py

if exist "dist\Planilhas.exe" (
  echo EXE gerado com sucesso.
  for /f "tokens=*" %%A in ('powershell $([System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop))') do set DESKTOP=%%A
  copy /Y "dist\Planilhas.exe" "!DESKTOP!\Planilhas.exe" > nul
  echo Copiado para: !DESKTOP!\Planilhas.exe
) else (
  echo Erro: EXE nao foi criado.
)

echo.
pause
