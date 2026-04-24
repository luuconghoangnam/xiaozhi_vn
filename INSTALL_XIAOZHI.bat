@echo off
:: Chuyen vao thu muc chua file bat nay
cd /d "%~dp0"

title CAI DAT XIAOZHI VN - TU DONG
cls
echo ============================================================
echo           XIAOZHI VN - QUY TRINH CAI DAT TU DONG
echo ============================================================
echo.

:: 1. Python
if not exist "scripts\setup\01_python.bat" (
    echo [!] Loi: Khong tim thay thu muc scripts\setup.
    pause
    exit /b 1
)

call "scripts\setup\01_python.bat"
if %errorlevel% neq 0 goto :failed

:: 2. Venv
call "scripts\setup\02_venv.bat"
if %errorlevel% neq 0 goto :failed

:: 3. Libs
call "scripts\setup\03_libs.bat"
if %errorlevel% neq 0 goto :failed

:: 4. Models
call "scripts\setup\04_models.bat"
if %errorlevel% neq 0 goto :failed

:: 5. Config
call "scripts\setup\05_config.bat"
if %errorlevel% neq 0 goto :failed

echo.
echo ============================================================
echo   CHUC MUNG! BAN DA CAI DAT THANH CONG XIAOZHI VN.
echo   De khoi dong, hay chay file: RUN_COONIE.cmd
echo ============================================================
pause
exit /b 0

:failed
echo.
echo [X] CO LOI XAY RA TRONG QUA TRINH CAI DAT.
echo Vui long kiem tra lai cac buoc tren hoac lien he ho tro.
pause
exit /b 1
