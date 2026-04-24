@echo off
setlocal enabledelayedexpansion
echo ==========================================
echo    XiaoZhi VN - Automated Installer
echo ==========================================

:: 1. Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Khong tim thay Python tren he thong.
    echo [>] Dang thu tu dong cai dat Python 3.12 qua winget...
    
    :: Kiem tra winget
    winget --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [!] Khong tim thay winget. Vui long cai dat Python thu cong tai: https://www.python.org/
        pause
        exit /b 1
    )
    
    :: Cai dat Python
    winget install Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    if %errorlevel% neq 0 (
        echo [!] Cai dat Python that bai. Vui long cai dat thu cong.
        pause
        exit /b 1
    )
    
    echo [OK] Da cai dat xong Python. Vui long KHOI DONG LAI cua so CMD nay de tiep tuc.
    pause
    exit /b 0
)

:: 2. Chay script cai dat chinh bang Python
echo [OK] Da tim thay Python. Bat dau qua trinh cai dat...
python install.py

echo.
echo ==========================================
echo    Hoan tat! Nhan phim bat ky de thoat.
echo ==========================================
pause
