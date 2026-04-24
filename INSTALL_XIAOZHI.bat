@echo off
echo [DEBUG] Dang khoi chay...
pause
cd /d "%~dp0"
echo [DEBUG] Thu muc hien tai: %cd%

title CAI DAT XIAOZHI VN - TU DONG
cls
echo ============================================================
echo           XIAOZHI VN - QUY TRINH CAI DAT TU DONG
echo ============================================================
echo.

:: 1. Python
if not exist "scripts\setup\01_python.bat" (
    echo [!] Loi: Khong tim thay scripts\setup\01_python.bat
    echo [DEBUG] Toan bo duong dan: "%~dp0scripts\setup\01_python.bat"
    pause
    exit /b 1
)

echo [>] Bat dau Buoc 1...
call "scripts\setup\01_python.bat"
if %errorlevel% neq 0 goto :failed

echo [>] Bat dau Buoc 2...
call "scripts\setup\02_venv.bat"
if %errorlevel% neq 0 goto :failed

echo [>] Bat dau Buoc 3...
call "scripts\setup\03_libs.bat"
if %errorlevel% neq 0 goto :failed

echo [>] Bat dau Buoc 4...
call "scripts\setup\04_models.bat"
if %errorlevel% neq 0 goto :failed

echo [>] Bat dau Buoc 5...
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
pause
exit /b 1
