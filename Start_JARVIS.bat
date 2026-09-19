@echo off
title Start J.A.R.V.I.S.
echo ========================================================
echo    STARTING J.A.R.V.I.S. VOICE ASSISTANT IN BACKGROUND
echo ========================================================
start wscript.exe "c:\Users\Public\jarvis-ai\run_jarvis_silently.vbs"
echo J.A.R.V.I.S. is now running in the background!
timeout /t 3 >nul
