@echo off
title Stop J.A.R.V.I.S.
echo ========================================================
echo    STOPPING J.A.R.V.I.S. VOICE ASSISTANT BACKGROUND SERVER
echo ========================================================
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo J.A.R.V.I.S. has been stopped successfully.
timeout /t 3 >nul
