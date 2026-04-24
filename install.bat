@echo off
setlocal enabledelayedexpansion
echo ==========================================
echo    XiaoZhi VN - Automated Installer
echo ==========================================

:: 1. Kiem tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Khong tim thay Python tren he thong.
    echo [>] Dang tai xuong Python 3.12 tu python.org...
    
    set "PYTHON_URL=https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe"
    set "PYTHON_EXE=%TEMP%\python_installer.exe"
    
    :: Dung PowerShell de tai xuong
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('!PYTHON_URL!', '!PYTHON_EXE!')"
    
    if not exist "!PYTHON_EXE!" (
        echo [!] Khong the tai xuong Python. Vui long kiem tra ket noi mang.
        pause
        exit /b 1
    )
    
    echo [>] Dang cai dat Python (vui long cho trong giay lat)...
    :: Cai dat im lang, add vao PATH
    start /wait "" "!PYTHON_EXE!" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    del "!PYTHON_EXE!"
    
    echo [OK] Da cai dat xong Python. 
    echo [!] LUU Y: Ban can DONG cua so nay va MO LAI de cap nhat bien moi truong.
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
