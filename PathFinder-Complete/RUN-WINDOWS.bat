@echo off
setlocal
cd /d "%~dp0"
echo ======================================
echo   PathFinder - Interactive Algorithm Lab
echo ======================================
echo.
where py >nul 2>&1
if errorlevel 1 (
    echo Python launcher "py" was not found.
    echo Install Python from https://www.python.org/downloads/windows/
    pause
    exit /b 1
)
echo Installing or checking Python dependencies...
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed. Check your internet connection and Python installation.
    pause
    exit /b 1
)
echo Starting PathFinder. Press Ctrl+C to stop the server.
py -m streamlit run app.py
if errorlevel 1 (
    echo The app could not be started. Please read docs\WINDOWS_SETUP.md.
    pause
    exit /b 1
)
