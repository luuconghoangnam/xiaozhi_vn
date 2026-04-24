@echo off
echo [DEBUG CON 1] Da vao file 01_python.bat thành công.
pause

echo [>] Dang kiem tra lenh 'python' (Vui lòng chờ 2-3 giây)...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] May ban da co san Python.
    exit /b 0
)
echo [!] Lenh 'python' khong hoat dong.
pause

echo [>] Dang kiem tra lenh 'py' (Python Launcher)...
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] May ban co san Python Launcher (py).
    exit /b 0
)
echo [!] Lenh 'py' cung khong hoat dong.
pause

echo [DEBUG CON 2] Bat dau tai Python tu python.org...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe' -OutFile '$env:TEMP\python_installer.exe'"

if not exist "%TEMP%\python_installer.exe" (
    echo [!] LOI: Khong the tai file cai dat.
    pause
    exit /b 1
)

echo [DEBUG CON 3] Da tai xong. Dang mo trinh cai dat...
echo [!] LUU Y: Khi bang cai dat hien len, hay tich vao o 'Add Python to PATH' roi moi nhan Install.
pause

start /wait "" "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1
del "%TEMP%\python_installer.exe"

echo [OK] Da cai dat xong Python.
exit /b 0
