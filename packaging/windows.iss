; Inno Setup script: wraps dist\iconshuffle into an installer in out\.
; ISCC /DAppVersion=0.3.0 packaging\windows.iss
#ifndef AppVersion
  #define AppVersion "0.0.0"
#endif

[Setup]
AppId={{6F3E2B1A-8C4D-4E5F-9A7B-1C2D3E4F5A6B}
AppName=IconShuffle
AppVersion={#AppVersion}
AppPublisher=Yakup Emre Yerli
AppPublisherURL=https://github.com/YakupEmreYerli/IconShuffle
DefaultDirName={localappdata}\Programs\IconShuffle
DefaultGroupName=IconShuffle
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
OutputDir=..\out
OutputBaseFilename=IconShuffle-{#AppVersion}-windows-x64-setup
SetupIconFile=..\build\icons\iconshuffle.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\iconshuffle.exe

[Files]
Source: "..\dist\iconshuffle\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\IconShuffle"; Filename: "{app}\iconshuffle.exe"
Name: "{autodesktop}\IconShuffle"; Filename: "{app}\iconshuffle.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Run]
Filename: "{app}\iconshuffle.exe"; Description: "Open IconShuffle"; Flags: nowait postinstall skipifsilent
