@echo off
echo [BUOC 1] Kiem tra moi truong Python...

REM Kiem tra nhanh qua PowerShell
powershell -Command "if (Get-Command python -ErrorAction SilentlyContinue) { exit 0 } else { if (Get-Command py -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 } }"

if %errorlevel% equ 0 (
    echo [OK] May ban da co san Python.
    timeout /t 2 >nul
    exit /b 0
)

echo [!] Khong tim thay Python. Dang tai ve...
echo [>] Dang tai Python 3.12 (Vui long cho)...

REM Tai truc tiep vao thu muc hien tai de tranh loi duong dan TEMP
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile 'python_installer.exe'"

if not exist "python_installer.exe" (
    echo [!] LOI: Khong the tai file. Kiem tra mang.
    pause
    exit /b 1
)

echo [OK] Da tai xong.
echo.
echo ======================================================
echo  HUONG DAN:
echo  1. Bang cai dat Python se hien len.
echo  2. PHAI TICH VAO: [Add Python to PATH] o duoi cung.
echo  3. Nhan [Install Now].
echo ======================================================
echo.
pause

start /wait "" "python_installer.exe"
del "python_installer.exe"

echo.
echo [OK] Da hoan tat Buoc 1.
exit /b 0
