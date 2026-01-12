@echo off
echo Starting Video Transcription Tool...
echo.

REM Check if virtual environment exists and activate it
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Run setup.bat first!
    pause
    exit /b 1
)

echo Starting server...
echo Open http://localhost:8000 in your browser
echo.
python main.py
pause
