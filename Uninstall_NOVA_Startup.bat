@echo off
setlocal

set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP%\NOVA.lnk"

if exist "%SHORTCUT%" (
    del "%SHORTCUT%"
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'pythonw.exe' -and $_.CommandLine -like '*NOVA*nova.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"

echo.
echo NOVA was removed from Windows startup.
echo.
pause