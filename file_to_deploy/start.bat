@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 9009 (
    echo Python is not installed. Please install Python and rerun this script.
    exit /b 1
)

:: Install required Python packages
echo Installing required Python packages...
pip install selenium

:: Run the Python script
echo Running the script...
python bot.py

echo Script has finished running.
pause
