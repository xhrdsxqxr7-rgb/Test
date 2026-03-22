import os
import sys
import subprocess
import math
from PIL import Image, ImageDraw

DIR = os.path.dirname(os.path.abspath(__file__))

def make_main_icon():
    size = 256
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([0,0,size,size], fill=(88,101,242,255))
    lw = 28
    x, y, r = size//2, size//2, 70
    draw.rectangle([x-r-lw//2, y-r, x-r+lw//2, y+r], fill='white')
    draw.rectangle([x+r-lw//2, y-r, x+r+lw//2, y+r], fill='white')
    draw.rectangle([x-r, y-lw//2, x+r, y+lw//2], fill='white')
    path = os.path.join(DIR, 'main_icon.ico')
    img.save(path, format='ICO', sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
    return path

def run(cmd):
    subprocess.run(cmd, shell=True, cwd=DIR,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Установка библиотек
run("python -m pip install pyinstaller pillow pynput requests")

# Генерация иконки
icon_path = make_main_icon()

# Удаление старой сборки
for item in ['build', 'dist', 'main.spec']:
    p = os.path.join(DIR, item)
    if os.path.isdir(p):
        import shutil
        shutil.rmtree(p)
    elif os.path.isfile(p):
        os.remove(p)

# Сборка main.exe с иконкой
run(f'python -m PyInstaller --onefile --noconsole --icon="{icon_path}" main.py')

# Запуск
exe = os.path.join(DIR, 'dist', 'main.exe')
if os.path.exists(exe):
    os.startfile(exe)
