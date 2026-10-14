@echo off
echo ==============================================================
echo   Incredible Journeys - Setup and Installation
echo ==============================================================
echo [1/2] Installing Python backend dependencies...
pip install -r requirements.txt
echo.
echo [2/2] Installing Node frontend dependencies...
cd frontend
call npm install
cd ..
echo.
echo ==============================================================
echo   Installation completed successfully!
echo   Launching application on http://localhost:3000...
echo ==============================================================
python run.py
pause
