@echo off
echo [BUOC 3] Cai dat cac thu vien (pip)...

REM Bat che do UTF-8 de tranh loi doc ky tu dac biet trong requirements.txt
set PYTHONUTF8=1

set "PIP_PATH=.venv\Scripts\pip.exe"
if not exist "%PIP_PATH%" (
    echo [!] Khong tim thay pip trong .venv. Dang thu tao lai...
    python -m venv .venv
)

echo [>] Dang nang cap pip...
"%PIP_PATH%" install --upgrade pip

echo [>] Dang cai dat cac thu vien (Vui long cho, buoc nay co the mat vai phut)...
"%PIP_PATH%" install -r requirements.txt

if %errorlevel% equ 0 (
    echo [OK] Cai dat thu vien thanh cong.
) else (
    echo [!] Loi khi cai dat thu vien.
    pause
    exit /b 1
)
exit /b 0
