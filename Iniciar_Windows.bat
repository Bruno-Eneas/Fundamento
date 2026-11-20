@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3.12 -m venv .venv
  if errorlevel 1 (
    echo Instale Python 3.12 e tente novamente.
    pause
    exit /b 1
  )
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo Falha ao instalar. Copie a mensagem de erro para o chat.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m streamlit run app.py
pause
