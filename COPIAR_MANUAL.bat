@echo off
echo ========================================
echo COPIA MANUAL DO PLANILHAS.EXE
echo ========================================
echo.

echo 1. Finalizando Planilhas.exe se estiver rodando...
taskkill /IM Planilhas.exe /F 2>nul

echo 2. Procurando Planilhas.exe nos Downloads...
for %%d in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\Users\%USERNAME%\Downloads\Planilhas.exe" (
        echo ENCONTRADO em: %%d:\Users\%USERNAME%\Downloads\
        set "DOWNLOADS=%%d:\Users\%USERNAME%\Downloads"
        set "DESKTOP=%%d:\Users\%USERNAME%\Desktop"
        goto :copiar
    )
)

echo NAO ENCONTRADO! Verifique se baixou o arquivo.
goto :fim

:copiar
echo 3. Copiando para area de trabalho...
copy /Y "%DOWNLOADS%\Planilhas.exe" "%DESKTOP%\Planilhas.exe"

if exist "%DESKTOP%\Planilhas.exe" (
    echo.
    echo ========================================
    echo SUCESSO! Planilhas.exe copiado!
    echo DE: %DOWNLOADS%\Planilhas.exe
    echo PARA: %DESKTOP%\Planilhas.exe
    echo ========================================
    echo.
    echo AGORA EXECUTE DA AREA DE TRABALHO!
) else (
    echo ERRO! Falha ao copiar.
)

:fim
echo.
pause
