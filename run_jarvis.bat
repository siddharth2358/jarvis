@echo off
set "PYTHON_CMD=python"
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 'python' command not found, trying 'py'...
    set "PYTHON_CMD=py"
)

echo Checking dependencies...
%PYTHON_CMD% -c "import streamlit; import pinecone; import langchain_ollama; print('Dependencies look good!')"
if %errorlevel% neq 0 (
    echo.
    echo ------------------------------------------------------------------
    echo Dependencies are NOT fully installed yet or Python environment issue! 
    echo Installing dependencies...
    echo ------------------------------------------------------------------
    echo.
    %PYTHON_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies.
        pause
        exit /b
    )
)

echo CHECKING FOR OLLAMA...
where ollama >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ollama is NOT installed or NOT found in PATH.
    echo Jarvis requires Ollama to run the AI model.
    echo.
    echo Please read 'SETUP_OLLAMA.md' for installation instructions.
    echo.
    pause
    exit /b
)

echo Starting Jarvis...
echo Note: Using existing Ollama service or starting a new request...
start /B "Ollama Service" ollama serve >nul 2>nul
timeout /t 2 >nul
%PYTHON_CMD% -m streamlit run app.py
pause
