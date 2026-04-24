@echo off
title XIAOZHI VN - COONIE AI
cd /d "%~dp0"

echo ============================================================
echo           DANG KHOI DONG COONIE AI (XIAOZHI VN)
echo ============================================================

set PYTHONUTF8=1

if not exist ".venv\Scripts\python.exe" (
    echo [!] LOI: Khong tim thay moi truong ao (.venv).
    echo [>] Hay chay file INSTALL_XIAOZHI.bat truoc.
    pause
    exit /b 1
)

REM Chạy file main.py và bắt lỗi
.venv\Scripts\python.exe main.py

if %errorlevel% neq 0 (
    echo.
    echo [!] UNG DUNG BI DUNG DOT NGOT (Error Code: %errorlevel%).
    if exist "crash_report.txt" (
        echo [>] THONG TIN LOI CHI TIET:
        type crash_report.txt
    )
    pause
)

echo.
echo [DEBUG] Nhan phim bat ky de thoat...
pause
