@echo off
setlocal
set "APPDIR=%~dp0"
set "APPDIR=%APPDIR:~0,-1%"
set "PY=%APPDIR%\.venv\Scripts\python.exe"

if not exist "%PY%" (
  echo [ERROR] Khong tim thay Python venv: %PY%
  pause
  exit /b 1
)

set "XIAOZHI_START_MINIMIZED=1"
powershell -WindowStyle Hidden -NoProfile -Command "Start-Process -FilePath '%PY%' -ArgumentList @('-X','utf8','\"%APPDIR%\main.py\"','--mode','gui','--protocol','websocket') -WorkingDirectory '%APPDIR%' -WindowStyle Hidden"
exit /b 0
