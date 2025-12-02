#!/bin/bash
# Startup script for Wisprflow web application

echo "=========================================="
echo "  Wisprflow - Voice to Text Application"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Python $(python3 --version) found"
echo "✅ Node.js $(node --version) found"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q -r requirements.txt

echo "✅ Backend ready!"
echo ""

# Frontend setup
echo "📦 Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo "✅ Frontend ready!"
echo ""

# Start services
echo "🚀 Starting services..."
echo ""

# Start backend in background
cd ../backend
source venv/bin/activate
echo "Starting backend on http://localhost:8000"
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
cd ../frontend
echo "Starting frontend on http://localhost:5173"
echo ""
echo "=========================================="
echo "  Application is running!"
echo "=========================================="
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

npm run dev

# Cleanup on exit
kill $BACKEND_PID 2>/dev/null
