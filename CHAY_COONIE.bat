@echo off
setlocal
cd /d "%~dp0"
title COONIE AI - DEBUG

echo ---------------------------------------------------
echo  DANG KIEM TRA HE THONG...
echo ---------------------------------------------------

REM Kiem tra moi truong ao
if not exist ".venv\Scripts\python.exe" (
    echo [!] KHONG TIM THAY .VENV - HAY CHAY INSTALL_XIAOZHI.bat TRUOC!
    pause
    exit /b
)

echo [>] Dang khoi dong AI...
echo [>] Neu bi crash, thong tin se hien duoi day:
echo.

.venv\Scripts\python.exe main.py

echo.
echo ---------------------------------------------------
echo  CHUONG TRINH DA DUNG.
pause
