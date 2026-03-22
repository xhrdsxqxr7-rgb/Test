@echo off
echo Создаю setup.exe...
python -m pip install pyinstaller pillow >nul 2>&1

python -c "
from PIL import Image, ImageDraw
import math
size = 256
img = Image.new('RGBA', (size, size), (0,0,0,0))
draw = ImageDraw.Draw(img)
draw.ellipse([0,0,size,size], fill=(255,152,0,255))
cx, cy = size//2, size//2
teeth, r_outer, r_inner, r_hole = 8, 90, 72, 30
points = []
for i in range(teeth*2):
    angle = math.pi*i/teeth - math.pi/2
    r = r_outer if i%2==0 else r_inner
    offset = math.pi/(teeth*2) if i%2!=0 else 0
    a = angle+offset
    points.append((cx+r*math.cos(a), cy+r*math.sin(a)))
draw.polygon(points, fill='white')
draw.ellipse([cx-r_hole,cy-r_hole,cx+r_hole,cy+r_hole], fill=(255,152,0,255))
img.save('setup_icon.ico', format='ICO', sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
"

python -m PyInstaller --onefile --noconsole --icon=setup_icon.ico setup.py >nul 2>&1

if exist dist\setup.exe (
    copy dist\setup.exe setup.exe >nul
    rmdir /s /q build dist >nul 2>&1
    del setup.spec setup_icon.ico >nul 2>&1
    echo.
    echo Готово! Теперь можешь удалить make_setup_exe.bat
    echo Запускай только setup.exe и main.py
) else (
    echo ОШИБКА: setup.exe не создан
)
pause
