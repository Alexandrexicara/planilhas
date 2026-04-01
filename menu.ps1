# Script PowerShell para iniciar o sistema
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🚀 SISTEMA COM LOGIN - planilhas.com" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Usar Python do sistema
$pythonPath = "C:\Users\Positivo\AppData\Local\Programs\Python\Python314\python.exe"

if (Test-Path $pythonPath) {
    & $pythonPath menu_principal.py
} else {
    Write-Host "❌ Python não encontrado em: $pythonPath" -ForegroundColor Red
    Write-Host "Por favor, verifique a instalação do Python." -ForegroundColor Red
}

Write-Host ""
Read-Host "Pressione Enter para sair"
