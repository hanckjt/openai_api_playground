 @echo off

set VENV_DIR=venv
set REQUIREMENTS_FILE=requirements.txt
set PYTHON_SCRIPT=0_Playground.py

if not exist "%VENV_DIR%\" (
    python -m venv %VENV_DIR%

    if exist "%REQUIREMENTS_FILE%" (
        %VENV_DIR%\Scripts\pip install -r "%REQUIREMENTS_FILE%"
    )
)

%VENV_DIR%\Scripts\streamlit run "%PYTHON_SCRIPT%" %*
pause