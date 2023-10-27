cd app
if exist venv (
	call venv\Scripts\activate
	pip install -r requirements.txt
	python app.py
)
if not exist venv (
	python -m venv venv
	call venv\Scripts\activate
	pip install -r requirements.txt
	python app.py
)
