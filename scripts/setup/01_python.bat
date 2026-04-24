@echo off
echo [BUOC 1] Kiem tra moi truong Python...

REM Su dung PowerShell de kiem tra mot cach chinh xac va an toan
powershell -Command "if (Get-Command python -ErrorAction SilentlyContinue) { exit 0 } else { if (Get-Command py -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 } }"

if %errorlevel% equ 0 (
    echo [OK] May ban da co san Python. Bo qua buoc cai dat.
    timeout /t 2 >nul
    exit /b 0
)

echo [!] Khong tim thay Python. Bat dau quy trinh tai va cai dat...
echo.
echo [>] Dang tai Python 3.12 tu python.org (Vui long cho)...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile '$env:TEMP\python_installer.exe'"

if not exist "%TEMP%\python_installer.exe" (
    echo [!] LOI: Khong the tai file. Kiem tra ket noi mang.
    pause
    exit /b 1
)

echo [OK] Da tai xong bộ cài.
echo.
echo ======================================================
echo  HUONG DAN:
echo  1. Bang cai dat Python se hien len.
echo  2. Tich vao o [Add Python to PATH] o phia duoi.
echo  3. Nhan [Install Now].
echo ======================================================
echo.
pause

start /wait "" "%TEMP%\python_installer.exe"
del "%TEMP%\python_installer.exe"

echo.
echo [OK] Da hoan tat Buoc 1.
exit /b 0
