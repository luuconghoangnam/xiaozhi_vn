@echo off
REM Chuyen vao thu muc chua file bat nay
cd /d "%~dp0"

title CAI DAT XIAOZHI VN - TU DONG
cls
echo ============================================================
echo           XIAOZHI VN - QUY TRINH CAI DAT TU DONG
echo ============================================================
echo.

REM Kiem tra file ton tai
echo [DEBUG 3] Kiem tra file scripts\setup\01_python.bat...
if not exist "scripts\setup\01_python.bat" (
    echo [!] LOI: Khong tim thay file scripts\setup\01_python.bat
    pause
    exit /b 1
)
echo [OK] Da tim thay file con.
pause

REM Bat dau goi file con
echo [DEBUG 4] Dang goi 01_python.bat...
call "%~dp0scripts\setup\01_python.bat"

echo [DEBUG 5] Da quay lai tu 01_python.bat voi errorlevel: %errorlevel%
if %errorlevel% neq 0 goto :failed
pause

echo [>] Tiep tuc cac buoc khac...
call "%~dp0scripts\setup\02_venv.bat"
call "%~dp0scripts\setup\03_libs.bat"
call "%~dp0scripts\setup\04_models.bat"
call "%~dp0scripts\setup\05_config.bat"

echo.
echo ============================================================
echo   CHUC MUNG! BAN DA CAI DAT THANH CONG XIAOZHI VN.
echo ============================================================
pause
exit /b 0

:failed
echo.
echo [X] CO LOI XAY RA TRONG QUA TRINH CAI DAT.
pause
exit /b 1
