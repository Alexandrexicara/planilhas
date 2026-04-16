@echo off
echo ========================================
echo COPIANDO PLANILHAS.EXE AUTOMATICO
echo ========================================
echo.

echo Finalizando Planilhas.exe se estiver rodando...
taskkill /IM Planilhas.exe /F 2>nul

echo Procurando Planilhas.exe nos Downloads...
for %%d in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\Users\%USERNAME%\Downloads\Planilhas.exe" (
        echo Encontrado em: %%d:\Users\%USERNAME%\Downloads\
        set "DOWNLOADS=%%d:\Users\%USERNAME%\Downloads"
        set "DESKTOP=%%d:\Users\%USERNAME%\Desktop"
        goto :copiar
    )
)

echo Planilhas.exe nao encontrado nos Downloads!
echo Verifique se voce baixou o arquivo do sistema.
goto :fim

:copiar
echo Copiando para area de trabalho...
copy /Y "%DOWNLOADS%\Planilhas.exe" "%DESKTOP%\Planilhas.exe"

if exist "%DESKTOP%\Planilhas.exe" (
    echo.
    echo ========================================
    echo SUCESSO! Planilhas.exe copiado!
    echo Local: %DESKTOP%\Planilhas.exe
    echo ========================================
    echo.
    echo Agora pode executar da area de trabalho!
) else (
    echo ERRO! Falha ao copiar arquivo.
)

:fim
echo.
pause
