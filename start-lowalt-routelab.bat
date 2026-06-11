@echo off
setlocal

cd /d "%~dp0"

echo Starting LowAlt-RouteLab...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-dev.ps1"
set EXIT_CODE=%ERRORLEVEL%

echo.
if not "%EXIT_CODE%"=="0" (
    echo Startup failed with exit code %EXIT_CODE%.
    echo Check logs in: "%~dp0logs"
    echo.
    pause
    exit /b %EXIT_CODE%
)

echo LowAlt-RouteLab startup command finished.
echo.
echo Open:
echo   Frontend:              http://127.0.0.1:5173/
echo   algorithm-service:     http://127.0.0.1:8001
echo   route-adapter-service: http://127.0.0.1:8081
echo.
echo Logs:
echo   %~dp0logs
echo.
echo You can close this window. Services keep running in the background.
echo Use stop-lowalt-routelab.bat to stop them.
echo.
pause
