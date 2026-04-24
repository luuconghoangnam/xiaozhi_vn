@echo off
cd /d "%~dp0"
title XIAOZHI VN - TU DONG CAI DAT
cls

echo ============================================================
echo           XIAOZHI VN - QUY TRINH CAI DAT TU DONG
echo ============================================================
echo.

REM Buoc 1: Python
echo [BUOC 1/5] Dang chuan bi cai dat Python...
call "scripts\setup\01_python.bat"
if %errorlevel% neq 0 goto :failed

REM Buoc 2: Venv
echo [BUOC 2/5] Dang khoi tao moi truong ao...
call "scripts\setup\02_venv.bat"
if %errorlevel% neq 0 goto :failed

REM Buoc 3: Libs
echo [BUOC 3/5] Dang cai dat thu vien...
call "scripts\setup\03_libs.bat"
if %errorlevel% neq 0 goto :failed

REM Buoc 4: Models
echo [BUOC 4/5] Dang tai Models AI...
call "scripts\setup\04_models.bat"
if %errorlevel% neq 0 goto :failed

REM Buoc 5: Config
echo [BUOC 5/5] Cau hinh tai khoan...
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
echo [X] CO LOI XAY RA. Vui long kiem tra cac thong bao phia tren.
pause
exit /b 1
