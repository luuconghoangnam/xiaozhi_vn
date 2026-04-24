@echo off
echo [DEBUG 1] Bat dau script...
pause

:: Chuyen vao thu muc chua file bat nay
cd /d "%~dp0"
echo [DEBUG 2] Da CD vao: %cd%
pause

title CAI DAT XIAOZHI VN - TU DONG
cls
echo ============================================================
echo           XIAOZHI VN - QUY TRINH CAI DAT TU DONG
echo ============================================================
echo.

:: 1. Kiem tra file con
echo [DEBUG 3] Kiem tra file scripts\setup\01_python.bat...
if not exist "scripts\setup\01_python.bat" (
    echo [!] LOI: Khong tim thay file scripts\setup\01_python.bat
    echo [!] Duong dan hien tai: %cd%
    dir /b scripts\setup
    pause
    exit /b 1
)
echo [OK] Da tim thay file con.
pause

:: 2. Goi file con
echo [DEBUG 4] Dang goi 01_python.bat...
call "scripts\setup\01_python.bat"
echo [DEBUG 5] Quay lai tu 01_python.bat voi errorlevel: %errorlevel%
if %errorlevel% neq 0 goto :failed
pause

echo [>] Tiep tuc cac buoc khac...
call "scripts\setup\02_venv.bat"
call "scripts\setup\03_libs.bat"
call "scripts\setup\04_models.bat"
call "scripts\setup\05_config.bat"

echo.
echo ============================================================
echo   CHUC MUNG! BAN DA CAI DAT THANH CONG XIAOZHI VN.
echo ============================================================
pause
exit /b 0

:failed
echo.
echo [X] CO LOI XAY RA.
pause
exit /b 1
