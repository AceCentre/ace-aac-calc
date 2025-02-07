!include "MUI2.nsh"

Name "Scientific Calculator"
OutFile "ScientificCalculator-Setup.exe"
RequestExecutionLevel user
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
    File "..\dist\logo_44I_icon.ico"
    
    # Create calculator directory and copy files
    CreateDirectory "$INSTDIR\calculator"
    SetOutPath "$INSTDIR\calculator"
    File "..\dist\calculator\calcstandalone.html"
    
    # Create shortcuts
    CreateDirectory "$DESKTOP"
    CreateShortCut "$DESKTOP\Scientific Calculator.lnk" "$INSTDIR\calculator\calcstandalone.html" "" "$INSTDIR\logo_44I_icon.ico"
    
    # Start Menu shortcuts
    CreateDirectory "$SMPROGRAMS\Scientific Calculator"
    CreateShortCut "$SMPROGRAMS\Scientific Calculator\Scientific Calculator.lnk" "$INSTDIR\calculator\calcstandalone.html" "" "$INSTDIR\logo_44I_icon.ico"
    CreateShortCut "$SMPROGRAMS\Scientific Calculator\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "DisplayName" "Scientific Calculator"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "DisplayIcon" "$INSTDIR\logo_44I_icon.ico"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "Publisher" "AAC Tools"
SectionEnd

Section "Uninstall"
    Delete "$DESKTOP\Scientific Calculator.lnk"
    Delete "$SMPROGRAMS\Scientific Calculator\Scientific Calculator.lnk"
    Delete "$SMPROGRAMS\Scientific Calculator\Uninstall.lnk"
    RMDir "$SMPROGRAMS\Scientific Calculator"
    
    Delete "$INSTDIR\calculator\calcstandalone.html"
    RMDir "$INSTDIR\calculator"
    Delete "$INSTDIR\logo_44I_icon.ico"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
    RMDir "$LOCALAPPDATA\AAC Tools"
    
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator"
SectionEnd 