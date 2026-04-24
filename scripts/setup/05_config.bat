@echo off
echo [BUOC 5] Cau hinh tai khoan va Lay ma 6 so...

if not exist "config" mkdir "config"

REM Lay Machine ID thuc te de lam Device ID mac dinh
for /f "delims=" %%i in ('powershell -Command "Get-CimInstance Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"') do set "MID=%%i"
set "DEVICE_ID=XZ_VN_%MID:~0,8%"

cls
echo ============================================================
echo           LAY MA LIEN KET 6 SO (AUTOMATIC)
echo ============================================================
echo.
echo [>] Dang mo Dashboard...
start https://xiaozhi.me/console/agents
echo.

REM Chay script Python de xin ma 6 so tu server
.venv\Scripts\python.exe scripts\setup\pair_device.py

echo.
echo ============================================================
echo  SAU KHI NHAP MA 6 SO VA NHAN [CONFIRM] TREN WEB:
echo  1. Thiet bi se hien trong danh sach cua ban.
echo  2. Nhan vao thiet bi do de lay [Access Token].
echo ============================================================
echo.

set /p TOKEN="Nhap Access Token ban vua lay duoc: "

if "%TOKEN%"=="" (
    echo [!] Ban chua nhap token. Quy trinh bi gian doan.
    pause
    exit /b 1
)

echo [>] Dang luu cau hinh...
powershell -Command "$path='config/config.json'; $json=(Get-Content $path | ConvertFrom-Json); $json.SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN='%TOKEN%'; $json.DEVICE_ID='%DEVICE_ID%'; $json | ConvertTo-Json -Depth 20 | Set-Content $path"

echo.
echo [OK] DA KET NOI THANH CONG!
timeout /t 3 >nul
exit /b 0
