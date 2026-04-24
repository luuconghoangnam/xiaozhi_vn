@echo off
echo [BUOC 5] Cau hinh tai khoan...
if not exist "config\config.json" (
    if exist "config\config.example.json" (
        copy "config\config.example.json" "config\config.json"
    ) else (
        echo [!] Thieu file config template.
        exit /b 1
    )
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
    powershell -Command "$path='config/config.json'; $json=(Get-Content $path | ConvertFrom-Json); $json.SYSTEM_OPTIONS.NETWORK.WEBSOCKET_ACCESS_TOKEN='!TOKEN!'; $json | ConvertTo-Json -Depth 20 | Set-Content $path"
)

echo [OK] Da cau hinh xong.
exit /b 0
