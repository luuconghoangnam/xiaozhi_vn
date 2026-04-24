@echo off
echo [BUOC 5] Cau hinh tai khoan va Ket noi thiet bi...

if not exist "config" mkdir "config"

REM Lay Machine ID thuc te de lam Device ID
for /f "delims=" %%i in ('powershell -Command "Get-CimInstance Win32_ComputerSystemProduct | Select-Object -ExpandProperty UUID"') do set "MID=%%i"
set "DEVICE_ID=XZ_VN_%MID:~0,8%"

cls
echo ============================================================
echo           HUONG DAN KET NOI THIET BI XIAOZHI
echo ============================================================
echo.
echo  BUOC A: Script se mo trang Web Dashboard cho ban.
echo  BUOC B: Nhan [Add Device] (Them thiet bi).
echo  BUOC C: Nhap ma so sau day vao o [Device ID] tren Web:
echo.
powershell -Command "Write-Host '      >>> ' -NoNewline; Write-Host '%DEVICE_ID%' -ForegroundColor Yellow -BackgroundColor Black; Write-Host ''"
echo.
echo  BUOC D: Sau khi Save, hay Copy [Access Token] va dan vao day.
echo.
echo ============================================================
echo [>] Dang mo trinh duyet...
start https://xiaozhi.me/dashboard/devices
echo.

set /p TOKEN="NHAP ACCESS TOKEN CUA BAN TAI DAY: "

if "%TOKEN%"=="" (
    echo [!] Ban chua nhap token. Quy trinh bi gian doan.
    pause
    exit /b 1
)

echo [>] Dang luu cau hinh he thong...
powershell -Command "$path='config/config.json'; $json=(Get-Content $path | ConvertFrom-Json); $json.SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN='%TOKEN%'; $json.DEVICE_ID='%DEVICE_ID%'; $json | ConvertTo-Json -Depth 20 | Set-Content $path"

echo.
echo ============================================================
echo   [OK] LIEN KET THANH CONG! 
echo   Thiet bi cua ban hien da san sang hoat dong.
echo ============================================================
timeout /t 3 >nul
exit /b 0
