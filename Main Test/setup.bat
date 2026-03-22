@echo off
set "DIR=%~dp0"
powershell -WindowStyle Hidden -Command "& {$dir = '%DIR%'; cd $dir; python -m pip install pyinstaller pillow pynput requests 2>$null; Remove-Item -Recurse -Force build,dist,main.spec -ErrorAction SilentlyContinue; python -m PyInstaller --onefile --noconsole main.py 2>$null; Start-Sleep -Seconds 3; Start-Process (Join-Path $dir 'dist\main.exe')}"