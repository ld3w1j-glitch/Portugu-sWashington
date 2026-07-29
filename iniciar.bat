@echo off
chcp 65001 > nul
title Gramática em Análise
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py"
) else (
    set "PYTHON_CMD=python"
)

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo Preparando o sistema pela primeira vez...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto :python_error
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 goto :install_error
)

echo.
echo Iniciando Gramática em Análise...
".venv\Scripts\python.exe" server.py
goto :end

:python_error
echo.
echo Não foi possível encontrar ou preparar o Python.
echo Instale o Python 3.10 ou superior e marque "Add Python to PATH".
pause
goto :end

:install_error
echo.
echo Não foi possível instalar os componentes.
echo Verifique a conexão com a internet na primeira execução.
pause

:end
