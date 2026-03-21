@echo off
echo [1] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не установлен или не добавлен в PATH!
    pause
    exit
)

echo [2] Установка инструментов сборки...
python -m pip install pyinstaller pillow keyboard requests

echo [3] Сборка одного EXE файла (подожди минуту)...
:: Мы используем python -m PyInstaller, это надежнее
python -m PyInstaller --noconsole --onefile --add-data "image.jpg;." main.py

if exist "dist\main.exe" (
    echo.
    echo --- УСПЕХ! ---
    echo Твой файл готов и лежит в папке: dist\main.exe
    echo Теперь можешь переименовать его и скинуть другу.
) else (
    echo.
    echo --- ОШИБКА СБОРКИ ---
    echo Что-то пошло не так. Проверь текст выше.
)
pause