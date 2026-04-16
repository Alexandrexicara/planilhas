@echo off
echo Finalizando Planilhas.exe...
taskkill /IM Planilhas.exe /F 2>nul

echo Procurando Planilhas.exe baixado do navegador...
for %%d in (C D E F G H I J K L M N O P Q R S T U V W X Y Z) do (
    if exist "%%d:\Users\%USERNAME%\Downloads\Planilhas.exe" (
        set "DOWNLOADS=%%d:\Users\%USERNAME%\Downloads"
        set "DESKTOP=%%d:\Users\%USERNAME%\Desktop"
        goto :found
    )
)

:found
if defined DOWNLOADS (
    echo Copiando Planilhas.exe do Downloads para Desktop...
    copy /Y "%DOWNLOADS%\Planilhas.exe" "%DESKTOP%\Planilhas.exe"
    
    if exist "%DESKTOP%\Planilhas.exe" (
        echo.
        echo ========================================
        echo SUCESSO! Planilhas.exe copiado!
        echo De: %DOWNLOADS%\Planilhas.exe
        echo Para: %DESKTOP%\Planilhas.exe
        echo ========================================
        echo.
        echo Agora pode executar da area de trabalho!
    ) else (
        echo ERRO! Falha ao copiar arquivo.
    )
) else (
    echo.
    echo ========================================
    echo ATENCAO! Planilhas.exe nao encontrado!
    echo ========================================
    echo.
    echo Verifique se voce baixou o arquivo do site:
    echo 1. Acesse o sistema web
    echo 2. Faca o download do Planilhas.exe
    echo 3. Verifique na pasta Downloads
    echo.
)

pause
