@echo off
title XIAOZHI VN - COONIE AI
cd /d "%~dp0"

echo ==========================================
echo    DANG KHOI DONG XIAOZHI VN...
echo ==========================================

if not exist ".venv" (
    echo [!] Chua co moi truong ao. Vui long chay INSTALL_XIAOZHI.bat truoc.
    pause
    exit /b 1
)

REM Kich hoat moi truong ao va chay app
set PYTHONUTF8=1
.venv\Scripts\python.exe src\application.py

if %errorlevel% neq 0 (
    echo.
    echo [!] Ung dung da dung lai voi loi (Error Code: %errorlevel%).
    pause
)
