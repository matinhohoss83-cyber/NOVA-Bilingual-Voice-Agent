@echo off
setlocal

set "NOVA_DIR=%USERPROFILE%\Documents\NOVA"
set "PYTHONW=%NOVA_DIR%\.venv\Scripts\pythonw.exe"
set "NOVA_SCRIPT=%NOVA_DIR%\nova.py"
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP%\NOVA.lnk"

if not exist "%PYTHONW%" (
    echo Python environment not found:
    echo %PYTHONW%
    pause
    exit /b 1
)

if not exist "%NOVA_SCRIPT%" (
    echo nova.py not found:
    echo %NOVA_SCRIPT%
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$s=New-Object -ComObject WScript.Shell; $l=$s.CreateShortcut('%SHORTCUT%'); $l.TargetPath='%PYTHONW%'; $l.Arguments='\"%NOVA_SCRIPT%\"'; $l.WorkingDirectory='%NOVA_DIR%'; $l.Save()"

if errorlevel 1 (
    echo Installation failed.
    pause
    exit /b 1
)

start "" "%SHORTCUT%"

echo.
echo NOVA installed successfully.
echo NOVA is running in the background.
echo Say: Hey NOVA
echo.
pause