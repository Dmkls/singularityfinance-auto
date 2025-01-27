@echo off

IF EXIST ".\.venv" (
	call .\.venv\Scripts\activate
) ELSE (
	echo creating env..
	python -m venv .venv
)

pip install -r requirements.txt
pause