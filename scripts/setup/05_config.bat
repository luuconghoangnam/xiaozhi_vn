@echo off
echo [BUOC 5] Cau hinh tai khoan...

if not exist "config" mkdir "config"

if not exist "config\config.json" (
    if exist "config\config.example.json" (
        copy "config\config.example.json" "config\config.json" >nul
    ) else (
        echo [>] Dang khoi tao file cau hinh moi...
        powershell -Command "$json = @{ SYSTEM_OPTIONS = @{ NETWORK = @{ WEBSOCKET_URL = 'wss://api.xiaozhi.me/v1/robot/protocol'; WEBSOCKET_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN_HERE' } }; DEVICE_ID = 'COONIE_AI_VN'; LLM_OPTIONS = @{ LANGUAGE = 'vi-VN' } }; $json | ConvertTo-Json -Depth 20 | Set-Content 'config/config.json'"
    )
)

REM Kiem tra xem da co Token thuc su chua
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
    echo [OK] Da cau hinh xong Token.
)

exit /b 0
