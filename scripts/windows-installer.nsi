!include "MUI2.nsh"

Name "Scientific Calculator"
OutFile "ScientificCalculator-Setup.exe"
RequestExecutionLevel user
InstallDir "$LOCALAPPDATA\Ace Centre\Scientific Calculator"

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
    CreateDirectory "$INSTDIR\calculator\lib"
    CreateDirectory "$INSTDIR\calculator\lib\fonts"
    SetOutPath "$INSTDIR\calculator"
    File "..\dist\calculator\calcstandalone.html"
    SetOutPath "$INSTDIR\calculator\lib"
    File "..\dist\calculator\lib\math.js"
    File "..\dist\calculator\lib\katex.min.css"
    File "..\dist\calculator\lib\katex.min.js"
    SetOutPath "$INSTDIR\calculator\lib\fonts"
    File "..\dist\calculator\lib\fonts\*.*"
    
    # Copy CreateGridSet files first
    SetOutPath "$INSTDIR\gridset"
    File /r "..\dist\gridset\*.*"
    
    # Create gridset directory and copy initial gridset
    CreateDirectory "$APPDATA\Ace Centre\Scientific Calculator"
    SetOutPath "$APPDATA\Ace Centre\Scientific Calculator"
    File "..\dist\gridset\ScientificCalc.gridset"
    
    # Now run CreateGridSet after files are in place
    ExecWait '"$INSTDIR\gridset\CreateGridSet.exe"'
    
    # Create shortcuts
    CreateDirectory "$DESKTOP"
    CreateShortCut "$DESKTOP\Scientific Calculator.lnk" "$INSTDIR\calculator\calcstandalone.html" "" "$INSTDIR\logo_44I_icon.ico"
    CreateShortCut "$DESKTOP\Scientific Calculator Grid.lnk" "$APPDATA\Ace Centre\Scientific Calculator\ScientificCalc.gridset" "" "$INSTDIR\logo_44I_icon.ico"
    
    # Start Menu shortcuts
    CreateDirectory "$SMPROGRAMS\Scientific Calculator"
    CreateShortCut "$SMPROGRAMS\Scientific Calculator\Scientific Calculator.lnk" "$INSTDIR\calculator\calcstandalone.html" "" "$INSTDIR\logo_44I_icon.ico"
    CreateShortCut "$SMPROGRAMS\Scientific Calculator\Scientific Calculator Grid.lnk" "$APPDATA\Ace Centre\Scientific Calculator\ScientificCalc.gridset" "" "$INSTDIR\logo_44I_icon.ico"
    CreateShortCut "$SMPROGRAMS\Scientific Calculator\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
    
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "DisplayName" "Scientific Calculator"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "DisplayIcon" "$INSTDIR\logo_44I_icon.ico"
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator" "Publisher" "Ace Centre"
SectionEnd

Section "Uninstall"
    Delete "$DESKTOP\Scientific Calculator.lnk"
    Delete "$DESKTOP\Scientific Calculator Grid.lnk"
    Delete "$SMPROGRAMS\Scientific Calculator\Scientific Calculator.lnk"
    Delete "$SMPROGRAMS\Scientific Calculator\Scientific Calculator Grid.lnk"
    Delete "$SMPROGRAMS\Scientific Calculator\Uninstall.lnk"
    RMDir "$SMPROGRAMS\Scientific Calculator"
    
    Delete "$INSTDIR\calculator\calcstandalone.html"
    Delete "$INSTDIR\calculator\lib\math.js"
    Delete "$INSTDIR\calculator\lib\katex.min.css"
    Delete "$INSTDIR\calculator\lib\katex.min.js"
    Delete "$INSTDIR\calculator\lib\fonts\*.*"
    RMDir "$INSTDIR\calculator\lib\fonts"
    RMDir "$INSTDIR\calculator\lib"
    RMDir "$INSTDIR\calculator"
    Delete "$INSTDIR\gridset\*.*"
    RMDir "$INSTDIR\gridset"
    Delete "$INSTDIR\logo_44I_icon.ico"
    Delete "$INSTDIR\Uninstall.exe"
    RMDir "$INSTDIR"
    
    Delete "$APPDATA\Ace Centre\Scientific Calculator\ScientificCalc.gridset"
    RMDir "$APPDATA\Ace Centre\Scientific Calculator"
    
    DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\ScientificCalculator"
SectionEnd 