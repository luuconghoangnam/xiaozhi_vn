@echo off
echo [DEBUG CON] Dang chay ben trong file 01_python.bat...
pause

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
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile '$env:TEMP\python_installer.exe'"

if not exist "%TEMP%\python_installer.exe" (
    echo [!] Loi tai Python.
    pause
    exit /b 1
)

echo [>] Dang cai dat...
start /wait "" "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1
del "%TEMP%\python_installer.exe"
echo [OK] Cai dat Python xong.
exit /b 0
