@echo off
setlocal
set "APPDIR=%~dp0"
set "APPDIR=%APPDIR:~0,-1%"
set "PY=%APPDIR%\.venv\Scripts\python.exe"
set "TITLE=Coonie AI"

if not exist "%PY%" (
  echo [ERROR] Khong tim thay Python venv: %PY%
  pause
  exit /b 1
)

cd /d "%APPDIR%"
title %TITLE%

echo ======================================
echo          COONIE AI LAUNCHER
echo ======================================
echo.
"%PY%" -X utf8 "%APPDIR%\main.py" --mode gui --protocol websocket

echo.
echo [EXIT] App da thoat. Nhan phim bat ky de dong cua so...
pause >nul
endlocal
