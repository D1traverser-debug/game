@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 goto use_py

where python >nul 2>nul
if %errorlevel%==0 goto use_python

echo Python 3 was not found. Opening the standalone HTML fallback.
echo For full local module loading and reliable browser storage, install Python 3.
start "" "%~dp0index.html"
goto done

:use_py
py -3 scripts\serve_web.py --open
goto done

:use_python
python scripts\serve_web.py --open
goto done

:done
if errorlevel 1 pause
endlocal
