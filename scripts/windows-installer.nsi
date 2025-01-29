!include "MUI2.nsh"

Name "Scientific Calculator"
OutFile "ScientificCalculator-Setup.exe"
InstallDir "$LOCALAPPDATA\AAC Tools\Scientific Calculator"

!define MUI_ICON "..\dist\logo_44I_icon.ico"
!define MUI_UNICON "..\dist\logo_44I_icon.ico"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  File "..\dist\scicalc.exe"
  File "..\dist\logo_44I_icon.ico"
  
  SetShellVarContext current
  
  CreateDirectory "$SMPROGRAMS\AAC Tools\Scientific Calculator"
  CreateShortcut "$SMPROGRAMS\AAC Tools\Scientific Calculator\Scientific Calculator.lnk" "$INSTDIR\scicalc.exe" "" "$INSTDIR\logo_44I_icon.ico"
  CreateShortcut "$SMPROGRAMS\AAC Tools\Scientific Calculator\Calculator Watch Mode.lnk" "$INSTDIR\scicalc.exe" "--readpasteboard" "$INSTDIR\logo_44I_icon.ico"
  
  CreateShortcut "$DESKTOP\AAC Tools Scientific Calculator.lnk" "$INSTDIR\scicalc.exe" "" "$INSTDIR\logo_44I_icon.ico"
  
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "DisplayName" "Scientific Calculator"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "DisplayIcon" "$INSTDIR\scicalc.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "Publisher" "AAC Tools"
SectionEnd

Section "Uninstall"
  SetShellVarContext current

  Delete "$DESKTOP\AAC Tools Scientific Calculator.lnk"
  Delete "$SMPROGRAMS\AAC Tools\Scientific Calculator\Scientific Calculator.lnk"
  Delete "$SMPROGRAMS\AAC Tools\Scientific Calculator\Calculator Watch Mode.lnk"
  RMDir "$SMPROGRAMS\AAC Tools\Scientific Calculator"
  RMDir "$SMPROGRAMS\AAC Tools"
  
  Delete "$INSTDIR\scicalc.exe"
  Delete "$INSTDIR\logo_44I_icon.ico"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
  RMDir "$LOCALAPPDATA\AAC Tools"
  
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator"
SectionEnd 