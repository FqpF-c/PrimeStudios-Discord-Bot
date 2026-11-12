@echo off
title Discord Server Setup Bot
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)
python bot.py
pause
