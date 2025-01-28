!include "MUI2.nsh"

Name "Scientific Calculator"
OutFile "ScientificCalculator-Setup.exe"
InstallDir "$PROGRAMFILES\Scientific Calculator"

!define MUI_ICON "..\resources\logo_44I_icon.ico"
!define MUI_UNICON "..\resources\logo_44I_icon.ico"

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
  File "dist\scicalc.exe"
  File "..\resources\logo_44I_icon.ico"
  
  # Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\Scientific Calculator"
  CreateShortcut "$SMPROGRAMS\Scientific Calculator\Scientific Calculator.lnk" "$INSTDIR\scicalc.exe" "" "$INSTDIR\logo_44I_icon.ico"
  CreateShortcut "$SMPROGRAMS\Scientific Calculator\Calculator Watch Mode.lnk" "$INSTDIR\scicalc.exe" "--readpasteboard" "$INSTDIR\logo_44I_icon.ico"
  
  # Create Desktop shortcuts
  CreateShortcut "$DESKTOP\Scientific Calculator.lnk" "$INSTDIR\scicalc.exe" "" "$INSTDIR\logo_44I_icon.ico"
  
  # Add to PATH
  EnVar::AddValue "PATH" "$INSTDIR"
  
  # Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  
  # Add uninstall information to Add/Remove Programs
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "DisplayName" "Scientific Calculator"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "DisplayIcon" "$INSTDIR\scicalc.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "Publisher" "AAC Tools"
SectionEnd

Section "Uninstall"
  # Remove shortcuts
  Delete "$DESKTOP\Scientific Calculator.lnk"
  Delete "$SMPROGRAMS\Scientific Calculator\Scientific Calculator.lnk"
  Delete "$SMPROGRAMS\Scientific Calculator\Calculator Watch Mode.lnk"
  RMDir "$SMPROGRAMS\Scientific Calculator"
  
  # Remove from PATH
  EnVar::DeleteValue "PATH" "$INSTDIR"
  
  # Remove program files
  Delete "$INSTDIR\scicalc.exe"
  Delete "$INSTDIR\logo_44I_icon.ico"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
  
  # Remove registry entries
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator"
SectionEnd 