@echo off
echo [BUOC 4] Tai va cai dat Models AI (Sherpa-ONNX)...
if exist "models\encoder.onnx" (
    echo [OK] Models da co san.
    exit /b 0
)

echo [>] Dang tai Models tu GitHub...
set "URL=https://github.com/luuconghoangnam/xiaozhi_vn/releases/download/v1.0.0/models_vn.zip"
set "ZIP=%TEMP%\models_vn.zip"

powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('%URL%', '%ZIP%')"

if not exist "%ZIP%" (
    echo [!] Khong the tai models.
    exit /b 1
)

echo [>] Dang giai nen...
if not exist "models" mkdir models
powershell -Command "Expand-Archive -Path '%ZIP%' -DestinationPath 'models' -Force"
del "%ZIP%"

echo [OK] Models da duoc cai dat.
exit /b 0
