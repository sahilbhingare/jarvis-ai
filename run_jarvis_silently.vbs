' =====================================================================
' 🤖 J.A.R.V.I.S. AI - Silent Background Launcher & Auto-Start Engine
' =====================================================================
' Starts Flask server with pythonw.exe (zero black console window)
' and opens the HUD interface in Chrome App Mode for continuous listening.
' =====================================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Set working directory to jarvis-ai project root
WshShell.CurrentDirectory = "c:\Users\Public\jarvis-ai"

' 1. Start JARVIS server silently
WshShell.Run "pythonw.exe app.py", 0, False

' 2. Wait 2.5 seconds for server to initialize
WScript.Sleep 2500

' 3. Open Iron Man HUD Interface
chromePath1 = WshShell.ExpandEnvironmentStrings("%ProgramFiles%\Google\Chrome\Application\chrome.exe")
chromePath2 = WshShell.ExpandEnvironmentStrings("%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe")
chromePath3 = WshShell.ExpandEnvironmentStrings("%LocalAppData%\Google\Chrome\Application\chrome.exe")
edgePath = WshShell.ExpandEnvironmentStrings("%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe")

flags = " --use-fake-ui-for-media-stream --autoplay-policy=no-user-gesture-required --app=http://localhost:5000"

If fso.FileExists(chromePath1) Then
    WshShell.Run """" & chromePath1 & """" & flags, 1, False
ElseIf fso.FileExists(chromePath2) Then
    WshShell.Run """" & chromePath2 & """" & flags, 1, False
ElseIf fso.FileExists(chromePath3) Then
    WshShell.Run """" & chromePath3 & """" & flags, 1, False
ElseIf fso.FileExists(edgePath) Then
    WshShell.Run """" & edgePath & """" & flags, 1, False
Else
    WshShell.Run "cmd /c start http://localhost:5000", 0, False
End If
