@echo off
REM Startup script for Wisprflow web application (Windows)

echo ==========================================
echo   Wisprflow - Voice to Text Application
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

echo Python found
echo Node.js found
echo.

REM Backend setup
echo Setting up backend...
cd backend

if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt

echo Backend ready!
echo.

REM Frontend setup
echo Setting up frontend...
cd ..\frontend

if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

echo Frontend ready!
echo.

REM Start services
echo Starting services...
echo.

REM Start backend in background
cd ..\backend
call venv\Scripts\activate.bat
echo Starting backend on http://localhost:8000
start "Wisprflow Backend" cmd /k python main.py

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
cd ..\frontend
echo Starting frontend on http://localhost:5173
echo.
echo ==========================================
echo   Application is running!
echo ==========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Close this window to stop the frontend
echo Close the backend window to stop the backend
echo.

npm run dev
