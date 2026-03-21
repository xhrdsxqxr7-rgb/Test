@echo off
setlocal
cd /d "%~dp0"

:: Проверка на права администратора
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Запрашиваю права администратора...
    powershell -Command "Start-Process -FilePath '%0' -Verb RunAs"
    exit /b
)

echo --- Права получены, начинаю установку ---

:: Проверка Python 
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Установка Python... 
    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe -OutFile python-installer.exe" 
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 
    del python-installer.exe 
)

echo --- Установка библиотек ---
pip install keyboard requests pillow [cite: 3, 4]

echo --- Настройка вечного автозапуска ---
:: Удаляем старый мусор из автозагрузки, если он там был 
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup" 
if exist "%STARTUP_FOLDER%\hippo_launcher.bat" del "%STARTUP_FOLDER%\hippo_launcher.bat" 

:: Создаем задачу в Планировщике Windows
:: Это гарантирует запуск после ПЕРЕЗАГРУЗКИ с правами админа для работы keyboard
schtasks /create /f /tn "HippoAlwaysRunning" /tr "pythonw.exe '%~dp0main.py'" /sc onlogon /rl highest

echo --- Готово! ---
echo Теперь программа будет запускаться сама при включении ПК. [cite: 3]
pause