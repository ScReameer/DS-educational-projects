@echo off
cd app
if exist venv (
	echo Virtual environment already exists...
	call .\venv\Scripts\activate
)
if not exist venv (
	echo Creating virtual environment...
	python -m venv venv
	call .\venv\Scripts\activate
	echo.
	echo Installing dependencies...
	echo.
	.\venv\Scripts\python.exe -m pip install --upgrade pip
	pip install -r requirements.txt
	echo.
	echo Dependencies installed successfully
)
echo.
echo Starting...
python src\main.py

