@echo off
echo [BUOC 1] Kiem tra va cai dat Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python da san sang.
    exit /b 0
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python Launcher (py) da san sang.
    exit /b 0
)

echo [!] Khong tim thay Python. Dang tai ve...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $url = 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe'; $out = '$env:TEMP\python_installer.exe'; (New-Object System.Net.WebClient).DownloadFile($url, $out)"
if not exist "%TEMP%\python_installer.exe" (
    echo [!] Loi tai Python.
    pause
    exit /b 1
)

echo [>] Dang cai dat...
start /wait "" "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1
del "%TEMP%\python_installer.exe"
echo [OK] Cai dat Python xong. Vui long khoi dong lai may hoac CMD sau khi tat ca hoan tat.
exit /b 0
