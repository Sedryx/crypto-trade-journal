#define MyAppName "Bybit Trade Journal"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Joach"
#define MyAppExeName "BybitTradeJournal.exe"
#define MyAppIcon "..\..\bybit_journal\frontend\asset\icon.ico"

[Setup]
AppId={{2A4B53E3-9A31-4B70-A7ED-5C7C4A9E4F44}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Bybit Trade Journal
DefaultGroupName=Bybit Trade Journal
DisableProgramGroupPage=yes
OutputDir=..\..\dist_installer
OutputBaseFilename=BybitTradeJournalSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
SetupIconFile={#MyAppIcon}
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "..\..\dist\BybitTradeJournal\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Bybit Trade Journal"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Bybit Trade Journal"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Bybit Trade Journal"; Flags: nowait postinstall skipifsilent

[Code]
function IsWebView2Installed: Boolean;
var
  Version: String;
begin
  Result :=
    RegQueryStringValue(HKLM, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version)
    or RegQueryStringValue(HKLM, 'SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version)
    or RegQueryStringValue(HKCU, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version);
end;

function InitializeSetup(): Boolean;
begin
  Result := True;
  if not IsWebView2Installed then
  begin
    MsgBox(
      'Microsoft Edge WebView2 Runtime is required before first launch.'#13#10 +
      'Install it from:'#13#10 +
      'https://go.microsoft.com/fwlink/p/?LinkId=2124703',
      mbInformation,
      MB_OK
    );
  end;
end;
