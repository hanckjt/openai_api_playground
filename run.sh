#!/bin/bash

VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
PYTHON_SCRIPT="0_Playground.py"

if [ ! -d "${VENV_DIR}" ]; then
    python3 -m venv "${VENV_DIR}"

    if [ -f "${REQUIREMENTS_FILE}" ]; then
        ${VENV_DIR}/bin/pip install -r "${REQUIREMENTS_FILE}"
    fi
fi

sudo "${VENV_DIR}/bin/streamlit run" "${PYTHON_SCRIPT}" "$@"