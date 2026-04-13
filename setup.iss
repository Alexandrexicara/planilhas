[Setup]
AppName=Planilhas
AppVersion=1.0.0
AppPublisher=planilhas.com
AppPublisherURL=https://planilhas.com
AppSupportURL=https://planilhas.com
AppUpdatesURL=https://planilhas.com
DefaultDirName={autopf}\Planilhas
DefaultGroupName=Planilhas
AllowNoIcons=yes
LicenseFile=
OutputDir=dist\instalador
OutputBaseFilename=Planilhas_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
WizardStyle=modern
ShowLanguageDialog=no
VersionInfoVersion=1.0.0
VersionInfoCompany=planilhas.com
VersionInfoProductName=Planilhas
UninstallDisplayIcon={app}\Planilhas.exe

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\Planilhas.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "app.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "banco.db"; DestDir: "{app}"; Flags: ignoreversion
Source: "banco_plus.db"; DestDir: "{app}"; Flags: ignoreversion
Source: "usuarios.db"; DestDir: "{app}"; Flags: ignoreversion
Source: "config_sistema.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Planilhas"; Filename: "{app}\Planilhas.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\{cm:UninstallProgram,Planilhas}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Planilhas"; Filename: "{app}\Planilhas.exe"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\Planilhas.exe"; Description: "{cm:LaunchProgram,Planilhas}"; Flags: nowait postinstall skipifsilent
