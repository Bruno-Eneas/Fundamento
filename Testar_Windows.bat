@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
 echo Execute Iniciar_Windows.bat primeiro.
 pause
 exit /b 1
)
.venv\Scripts\python.exe -m unittest discover -s tests -v
set "TEST_EXIT=%ERRORLEVEL%"
pause
exit /b %TEST_EXIT%
