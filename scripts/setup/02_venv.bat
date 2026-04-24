@echo off
echo [BUOC 2] Khoi tao moi truong ao (venv)...

if exist ".venv" (
    echo [OK] Moi truong ao da ton tai.
    exit /b 0
)

REM 1. Thu voi lenh 'python'
python -m venv .venv >nul 2>&1
if %errorlevel% equ 0 goto :success

REM 2. Thu voi lenh 'py'
py -m venv .venv >nul 2>&1
if %errorlevel% equ 0 goto :success

REM 3. Thu tim duong dan mac dinh tren Windows (neu thieu PATH)
set "LOCAL_PY=%LocalAppData%\Programs\Python\Python312\python.exe"
if exist "%LOCAL_PY%" (
    echo [>] Tim thay Python tai duong dan mac dinh. Dang tao venv...
    "%LOCAL_PY%" -m venv .venv
    if %errorlevel% equ 0 goto :success
)

set "LOCAL_PY_ALL=%ProgramFiles%\Python312\python.exe"
if exist "%LOCAL_PY_ALL%" (
    echo [>] Tim thay Python (All Users) tai duong dan mac dinh. Dang tao venv...
    "%LOCAL_PY_ALL%" -m venv .venv
    if %errorlevel% equ 0 goto :success
)

echo [!] Khong the tu dong tim thay Python de tao venv.
echo [!] Loi khuyen: Hay DONG cua so nay va MO LAI file INSTALL_XIAOZHI.bat.
exit /b 1

:success
echo [OK] Da tao xong moi truong ao (.venv).
exit /b 0
