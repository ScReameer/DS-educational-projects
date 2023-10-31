cd app
if not exist venv (
	python -m venv venv
	call .\venv\Scripts\activate
	.\venv\Scripts\python.exe -m pip install --upgrade pip
	pip install -r requirements.txt
)
if exist venv (
	call .\venv\Scripts\activate
)
python main.py

