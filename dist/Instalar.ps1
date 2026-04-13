# Instalador Planilhas - Copiar para Program Files e criar atalhos
param([switch]$Admin)

if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Reiniciando com privilégios de administrador..."
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Admin" -Verb RunAs
    exit
}

$sourceDir = "E:\planilhas.com\dist"
$installDir = "C:\Program Files\Planilhas"

if (-not (Test-Path $sourceDir)) {
    Write-Host "❌ Pasta de instalacao nao encontrada: $sourceDir"
    exit 1
}

Write-Host "📦 Criando pasta de instalacao..."
if (Test-Path $installDir) {
    Remove-Item $installDir -Recurse -Force
}
New-Item -ItemType Directory -Path $installDir | Out-Null

Write-Host "📂 Copiando arquivos..."
Copy-Item -Path "$sourceDir\*" -Destination $installDir -Recurse -Force -ErrorAction SilentlyContinue

$exePath = "$installDir\Planilhas.exe"
if (-not (Test-Path $exePath)) {
    Write-Host "❌ Exe nao encontrado em $exePath"
    exit 1
}

Write-Host "🔗 Criando atalhos..."
$desktopPath = [Environment]::GetFolderPath("Desktop")
$startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Planilhas"

New-Item -ItemType Directory -Path $startMenuPath -Force | Out-Null

$shortcutDesk = "$desktopPath\Planilhas.lnk"
$shortcutMenu = "$startMenuPath\Planilhas.lnk"
$iconPath = "$installDir\icon.ico"

$WshShell = New-Object -ComObject WScript.Shell

foreach ($shortcutPath in @($shortcutDesk, $shortcutMenu)) {
    if (Test-Path $shortcutPath) { Remove-Item $shortcutPath -Force }
    
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $exePath
    $shortcut.WorkingDirectory = $installDir
    if (Test-Path $iconPath) { $shortcut.IconLocation = $iconPath }
    $shortcut.Save()
}

Write-Host "✅ Planilhas instalado com sucesso!"
Write-Host "🚀 Abrindo aplicacao..."
Start-Process $exePath
