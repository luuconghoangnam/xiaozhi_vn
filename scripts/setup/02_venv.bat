@echo off
echo [BUOC 2] Khoi tao moi truong ao (venv)...
if exist ".venv" (
    echo [OK] Moi truong ao da ton tai.
    exit /b 0
)

python -m venv .venv
if %errorlevel% neq 0 (
    py -m venv .venv
)

if exist ".venv" (
    echo [OK] Da tao xong .venv
) else (
    echo [!] Khong the tao .venv
    exit /b 1
)
exit /b 0
