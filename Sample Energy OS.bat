@echo off
TITLE Sample Energy OS - Henkel Pilot Dashboard Launcher
cd /d "%~dp0"

echo ==================================================================
echo   Sample Energy OS -- Henkel Pilot Streamlit Dashboard Launcher
echo ==================================================================
echo.

:: Verify that the repository is extracted
if not exist "src\app.py" (
    echo [ERROR] Could not find "src\app.py"!
    echo.
    echo [IMPORTANT] If you are running this file directly from inside a ZIP archive,
    echo please EXTRACT ALL files from the ZIP folder to a local folder first.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

:: Set PYTHONPATH to project root and user site-packages
set PYTHONPATH=.;%APPDATA%\Python\Python314\site-packages;%PYTHONPATH%

echo [1/2] Checking dependencies...
python -c "import streamlit, pandas, pulp, plotly" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing required dependencies from requirements.txt...
    python -m pip install -r requirements.txt
)

echo.
echo [2/2] Launching Sample Energy OS Web Dashboard...
echo Dashboard will open automatically in your default browser at http://localhost:8501...
echo.
python -m streamlit run src/app.py

if %errorlevel% neq 0 (
    echo.
    echo [NOTE] Streamlit closed or encountered an issue. Press any key to exit.
    pause
)
