!include "MUI2.nsh"

Name "Scientific Calculator"
OutFile "ScientificCalculator-Setup.exe"
InstallDir "$PROGRAMFILES\Ace Centre\Scientific Calculator"

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
  
  # Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\Ace Centre\Scientific Calculator"
  CreateShortcut "$SMPROGRAMS\Ace Centre\Scientific Calculator\Scientific Calculator.lnk" "$INSTDIR\scicalc.exe" "" "$INSTDIR\logo_44I_icon.ico"
  CreateShortcut "$SMPROGRAMS\Ace Centre\Scientific Calculator\Calculator Watch Mode.lnk" "$INSTDIR\scicalc.exe" "--readpasteboard" "$INSTDIR\logo_44I_icon.ico"
  
  # Create Desktop shortcuts
  CreateShortcut "$DESKTOP\Ace Centre Scientific Calculator.lnk" "$INSTDIR\scicalc.exe" "" "$INSTDIR\logo_44I_icon.ico"
  
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
  Delete "$DESKTOP\Ace Centre Scientific Calculator.lnk"
  Delete "$SMPROGRAMS\Ace Centre\Scientific Calculator\Scientific Calculator.lnk"
  Delete "$SMPROGRAMS\Ace Centre\Scientific Calculator\Calculator Watch Mode.lnk"
  RMDir "$SMPROGRAMS\Ace Centre\Scientific Calculator"
  RMDir "$SMPROGRAMS\Ace Centre"
  
  # Remove program files
  Delete "$INSTDIR\scicalc.exe"
  Delete "$INSTDIR\logo_44I_icon.ico"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"
  RMDir "$PROGRAMFILES\Ace Centre"
  
  # Remove registry entries
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator"
SectionEnd 