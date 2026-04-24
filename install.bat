@echo off
setlocal
echo ==========================================
echo    XiaoZhi VN - Automated Installer
echo ==========================================

:: Check if python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH.
    pause
    exit /b 1
)

:: Run the python setup script
python install.py

echo.
echo Setup finished. Press any key to exit.
pause
