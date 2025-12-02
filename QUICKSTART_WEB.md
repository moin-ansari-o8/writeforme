# Quick Setup Guide

## Prerequisites Check

```bash
# Check Python
python3 --version
# Should be 3.8 or higher

# Check Node.js
node --version
# Should be 16 or higher

# Check FFmpeg (required for Whisper)
ffmpeg -version
```

## One-Command Setup

### Linux/macOS
```bash
./start.sh
```

### Windows
```cmd
start.bat
```

## Manual Setup (if scripts don't work)

### Terminal 1 - Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Terminal 2 - Frontend

```bash
cd frontend
npm install
npm run dev
```

## Access the App

Open browser: **http://localhost:5173**

## First-Time Setup Notes

1. **Whisper Model Download**: First run will download ~140MB Whisper model
2. **Microphone Permission**: Browser will ask for microphone access
3. **Port Conflicts**: Ensure ports 8000 and 5173 are free

## Troubleshooting

### Backend won't start
```bash
# Install FFmpeg first
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: choco install ffmpeg
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules
npm install
```

### Connection issues
- Ensure backend is running on port 8000
- Check browser console for errors
- Try different browser (Chrome recommended)

## Production Deployment

See [WEB_APP_README.md](WEB_APP_README.md) for detailed deployment instructions.
