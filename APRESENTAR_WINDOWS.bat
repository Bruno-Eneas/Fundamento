@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Fundamento - Demonstracao local
if not exist .venv\Scripts\python.exe (
  py -3.12 -m venv .venv
  if errorlevel 1 (
    echo Nao foi possivel criar o ambiente. Instale Python 3.12.
    pause
    exit /b 1
  )
)
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
  echo Falha ao instalar dependencias.
  pause
  exit /b 1
)
set "FUNDAMENTO_PRESENTATION_MODE=1"
set "FUNDAMENTO_PUBLIC_SHOWCASE="
echo.
echo DEMONSTRACAO COM DADOS FICTICIOS - sem senhas.
echo Abra a Local URL no terminal (geralmente http://localhost:8501).
echo Caso apareca porta 8502, feche o Fundamento anterior.
echo.
.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.headless true
pause
