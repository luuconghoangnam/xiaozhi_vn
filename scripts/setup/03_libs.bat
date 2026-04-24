@echo off
echo [BUOC 3] Cai dat cac thu vien (pip)...
set "PIP_PATH=.venv\Scripts\pip.exe"
if not exist "%PIP_PATH%" (
    echo [!] Khong tim thay pip trong .venv
    exit /b 1
)

echo [>] Dang nang cap pip...
"%PIP_PATH%" install --upgrade pip

echo [>] Dang cai dat requirements.txt (Vui long cho)...
"%PIP_PATH%" install -r requirements.txt

if %errorlevel% equ 0 (
    echo [OK] Cai dat thu vien xong.
) else (
    echo [!] Loi khi cai dat thu vien.
    exit /b 1
)
exit /b 0
