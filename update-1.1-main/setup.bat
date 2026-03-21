@echo off
echo --- Checking Python ---
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Installing...
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe -OutFile python-installer.exe"
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe
)

echo --- Installing dependencies ---
pip show keyboard >nul 2>&1 || pip install keyboard
pip show requests >nul 2>&1 || pip install requests
pip show pillow >nul 2>&1 || pip install pillow

echo Done!
pause
