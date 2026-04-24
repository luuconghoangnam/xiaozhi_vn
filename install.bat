@echo off
echo ==========================================
echo    XiaoZhi VN - Automated Installer
echo ==========================================

set "PY_CMD=python"

:: 1. Kiem tra Python hoac Py launcher
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PY_CMD=py"
    ) else (
        echo [!] Khong tim thay Python tren he thong.
        echo [>] Dang tai xuong Python 3.12...
        
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $url = 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe'; $out = '$env:TEMP\python_installer.exe'; (New-Object System.Net.WebClient).DownloadFile($url, $out)"
        
        if not exist "%TEMP%\python_installer.exe" (
            echo [!] Khong the tai xuong Python. Vui long kiem tra mang.
            pause
            exit /b 1
        )
        
        echo [>] Dang cai dat Python (vui long cho)...
        start /wait "" "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1
        del "%TEMP%\python_installer.exe"
        
        echo [OK] Da cai dat xong Python. 
        echo [!] Vui long DONG cua so nay va MO LAI de tiep tuc.
        pause
        exit /b 0
    )
)

:: 2. Chay script cai dat chinh bang Python
echo [OK] Da tim thay Python. Bat dau qua trinh cai dat...
%PY_CMD% install.py

if %errorlevel% neq 0 (
    echo [!] Co loi xay ra trong qua trinh cai dat.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo    Hoan tat! Nhan phim bat ky de thoat.
echo ==========================================
pause
