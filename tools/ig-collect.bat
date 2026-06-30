@echo off
REM Craftons IG inspiration collector - desktop wrapper (manual or scheduled runs).
REM
REM Usage:  ig-collect.bat [handle] [maxPosts]
REM   handle   defaults to modernconcreteco
REM   maxPosts optional cap, e.g.  ig-collect.bat modernconcreteco 60
REM
REM Downloads into the Drive "01 Inspiration" mount (the script's default --out),
REM so files sync into Google Drive automatically. Run the one-time login first:
REM   node ig-collect.mjs login
setlocal
cd /d "%~dp0"

set "HANDLE=%~1"
if "%HANDLE%"=="" set "HANDLE=modernconcreteco"
set "MAXARG="
if not "%~2"=="" set "MAXARG=--max %~2"

set "LOG=%~dp0ig-collect.log"
echo ============================================================>> "%LOG%"
echo [%date% %time%] collecting @%HANDLE% %MAXARG%>> "%LOG%"

where node >nul 2>nul
if errorlevel 1 (
  echo [%date% %time%] ERROR: node not found on PATH - install Node.js first.>> "%LOG%"
  echo node not found on PATH. Install Node.js, then re-run.
  exit /b 1
)

node "%~dp0ig-collect.mjs" %HANDLE% %MAXARG% >> "%LOG%" 2>&1
set "RC=%errorlevel%"
echo [%date% %time%] finished, exit code %RC%>> "%LOG%"
if not "%RC%"=="0" echo Collector exited with code %RC% - see "%LOG%".
exit /b %RC%
