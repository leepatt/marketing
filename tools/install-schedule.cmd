@echo off
REM Register a weekly Windows scheduled task so the IG collector runs autonomously.
REM Run this once (double-click, or let Claude Code on the desktop run it).
REM Re-run any time to refresh/replace the task.
REM
REM Prereqs (one-time): Node.js installed, `npm install` + `npx playwright install
REM chromium` done in this folder, and `node ig-collect.mjs login` completed so the
REM saved session exists. The PC must be on/awake at the scheduled time.
setlocal
set "BAT=%~dp0ig-collect.bat"

schtasks /Create /TN "Craftons IG Inspiration" /SC WEEKLY /D MON /ST 09:07 /F /TR "\"%BAT%\""
if errorlevel 1 (
  echo.
  echo Failed to create the task. Re-run this from an Administrator command prompt.
  exit /b 1
)

echo.
echo Created weekly task "Craftons IG Inspiration".
echo   When : every Monday at 09:07 (PC must be on)
echo   Runs : "%BAT%"  (handle defaults to modernconcreteco)
echo.
echo To change the day/time, edit it in Task Scheduler, or re-run with different
echo /D and /ST values. To remove it:  schtasks /Delete /TN "Craftons IG Inspiration" /F
endlocal
