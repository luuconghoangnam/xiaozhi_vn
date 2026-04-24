@echo off
echo [BUOC 5] Cau hinh tai khoan...

if not exist "config\config.json" (
    if exist "config\config.example.json" (
        copy "config\config.example.json" "config\config.json" >nul
    ) else (
        echo [!] Thieu file config template.
        exit /b 1
    )
)

REM Kiem tra xem da co Token trong file config chua
powershell -Command "$json=(Get-Content 'config/config.json' | ConvertFrom-Json); if ($json.SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN -and $json.SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN -ne 'YOUR_ACCESS_TOKEN_HERE') { exit 0 } else { exit 1 }"

if %errorlevel% equ 0 (
    echo [OK] Ban da cau hinh Token truoc do.
    set /p RECONFIG="Ban co muon nhap lai Token khong? (y/n): "
    if /i "%RECONFIG%" neq "y" exit /b 0
)

echo.
echo =======================================================
echo  BAN CAN DIEN ACCESS TOKEN DE UNG DUNG HOAT DONG
echo  Lay token tai: https://xiaozhi.me/
echo =======================================================
set /p TOKEN="Nhap Access Token cua ban: "

if "%TOKEN%"=="" (
    echo [!] Ban chua nhap token. Ban co the tu sua trong config/config.json sau.
) else (
    echo [>] Dang cap nhat config.json...
    powershell -Command "$path='config/config.json'; $json=(Get-Content $path | ConvertFrom-Json); $json.SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN='%TOKEN%'; $json | ConvertTo-Json -Depth 20 | Set-Content $path"
    echo [OK] Da cap nhat Token.
)

exit /b 0
