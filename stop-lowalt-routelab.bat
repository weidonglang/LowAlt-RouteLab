@echo off
setlocal

cd /d "%~dp0"

echo Stopping LowAlt-RouteLab...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\stop-dev.ps1"
set EXIT_CODE=%ERRORLEVEL%

echo.
if not "%EXIT_CODE%"=="0" (
    echo Stop command failed with exit code %EXIT_CODE%.
    echo.
    pause
    exit /b %EXIT_CODE%
)

echo LowAlt-RouteLab services stopped.
echo.
pause
