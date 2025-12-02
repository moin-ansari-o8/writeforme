# Wisprflow - Professional Voice-to-Text Web Application

A production-grade voice transcription application with real-time audio streaming and Whisper AI transcription. Built with FastAPI, React, and WebSocket for seamless real-time communication.

## 🚀 Features

- **Real-time Audio Streaming**: WebSocket-based audio chunk streaming (100ms intervals)
- **Whisper AI Transcription**: High-accuracy speech-to-text using OpenAI Whisper
- **Beautiful UI**: Professional, responsive interface with dark mode support
- **Audio Visualizer**: Real-time audio visualization with pill-shaped design
- **Low Latency**: Optimized pipeline for minimal processing delay
- **Error Handling**: Robust error handling and connection management

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI server with WebSocket
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── VoiceVisualizer.jsx
│   │   │   └── VoiceVisualizerExample.jsx
│   │   ├── hooks/           # Custom React hooks
│   │   │   └── useAudioRecorder.js
│   │   ├── App.jsx          # Main app component
│   │   ├── App.css          # App styles
│   │   └── main.jsx         # React entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js       # Vite configuration
└── WEB_APP_README.md        # This file
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance async web framework
- **Uvicorn**: ASGI server for production
- **WebSockets**: Real-time bidirectional communication
- **OpenAI Whisper**: State-of-the-art speech recognition

### Frontend
- **React 18**: Modern UI library with hooks
- **Vite**: Lightning-fast build tool and dev server
- **Web Audio API**: Native audio capture and processing
- **MediaRecorder API**: Audio recording and streaming
- **Canvas API**: Real-time audio visualization

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- FFmpeg (required for Whisper)

## 🚦 Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

Backend will run on `http://localhost:8000`

**Note**: First run will download the Whisper model (~140MB for base model)

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:5173`

## 🎯 Usage

1. **Start Backend**: Ensure FastAPI server is running on port 8000
2. **Start Frontend**: Open browser to `http://localhost:5173`
3. **Grant Permissions**: Allow microphone access when prompted
4. **Start Recording**: Click "Start Recording" button
5. **Speak Clearly**: The visualizer shows real-time audio input
6. **Stop Recording**: Click "Stop Recording" when done
7. **View Transcription**: Your speech will be transcribed and displayed

## 🔧 Configuration

### Backend Configuration

Edit `backend/main.py` to configure:

- **Whisper Model**: Change model size (tiny, base, small, medium, large)
  ```python
  self.model = whisper.load_model("base")  # Change to "small", "medium", etc.
  ```

- **Audio Settings**: Modify `AudioBuffer` class
  ```python
  self.sample_rate = 16000  # 16kHz is optimal for Whisper
  self.channels = 1         # Mono audio
  ```

- **CORS Origins**: Update allowed origins
  ```python
  allow_origins=["http://localhost:5173"]
  ```

### Frontend Configuration

Edit `frontend/src/hooks/useAudioRecorder.js`:

- **WebSocket URL**: Change backend URL
  ```javascript
  const WS_URL = 'ws://localhost:8000/ws/transcribe';
  ```

- **Audio Constraints**: Modify recording settings
  ```javascript
  audio: {
    channelCount: 1,
    sampleRate: 16000,
    echoCancellation: true,
    noiseSuppression: true,
  }
  ```

## 🎨 Customization

### Theme

The app auto-detects system theme (light/dark). Customize colors in `frontend/src/App.css`:

```css
:root {
  --color-primary: #6366f1;  /* Primary color */
  --color-background: #ffffff;  /* Background */
  /* ... more variables */
}
```

### Visualizer

Customize the voice visualizer in `frontend/src/components/VoiceVisualizer.jsx`:

```javascript
const PILL_WIDTH_IDLE = 120;    // Idle width
const PILL_WIDTH_ACTIVE = 180;  // Active width
const PILL_HEIGHT = 40;         // Height
```

## 📊 Performance Optimization

### Whisper Model Selection

| Model  | Size | Accuracy | Speed | Use Case |
|--------|------|----------|-------|----------|
| tiny   | 39MB | Good     | Very Fast | Testing |
| base   | 74MB | Better   | Fast | General Use ✅ |
| small  | 244MB | Very Good | Medium | High Quality |
| medium | 769MB | Excellent | Slow | Best Quality |

**Recommendation**: Use `base` for development, `small` or `medium` for production

### Audio Chunk Size

Smaller chunks = lower latency, larger chunks = better accuracy

```javascript
mediaRecorder.start(100);  // 100ms chunks (default)
```

### Browser Compatibility

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari (iOS 14.5+)
- ❌ IE11 (not supported)

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'whisper'`
```bash
pip install openai-whisper
```

**Problem**: FFmpeg not found
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (chocolatey)
choco install ffmpeg
```

### Frontend Issues

**Problem**: WebSocket connection failed
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**Problem**: Microphone access denied
- Grant microphone permissions in browser settings
- Use HTTPS in production (required for getUserMedia)

**Problem**: No audio captured
- Check system audio input device
- Verify microphone is not muted
- Try different browser

## 🚀 Production Deployment

### Backend

1. **Environment Variables**: Use `.env` file for configuration
2. **HTTPS**: Deploy with SSL certificate (required for microphone access)
3. **Process Manager**: Use `systemd` or `supervisor`
4. **Reverse Proxy**: Nginx or Caddy for WebSocket support

Example Nginx config:
```nginx
location /ws {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### Frontend

```bash
# Build for production
cd frontend
npm run build

# Output in dist/ directory
# Deploy to Netlify, Vercel, or any static host
```

### Docker (Optional)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    depends_on:
      - backend
```

## 📝 API Documentation

### WebSocket Endpoint: `/ws/transcribe`

**Connect**: `ws://localhost:8000/ws/transcribe`

**Messages (Client → Server)**:

```json
// Send audio chunk
{
  "type": "audio_chunk",
  "data": "base64_encoded_audio"
}

// End recording
{
  "type": "audio_end"
}

// Keep-alive
{
  "type": "ping"
}
```

**Messages (Server → Client)**:

```json
// Chunk received
{
  "type": "chunk_received",
  "buffer_size": 12345
}

// Transcription result
{
  "type": "transcription_result",
  "text": "Your transcribed text here"
}

// Error
{
  "type": "error",
  "message": "Error description"
}
```

### REST Endpoints

**GET** `/` - Health check
```json
{
  "status": "online",
  "service": "Wisprflow API",
  "whisper_available": true
}
```

**GET** `/api/status` - Service status
```json
{
  "transcription": {
    "available": true,
    "engine": "whisper"
  }
}
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- OpenAI Whisper for transcription engine
- Wisprflow for inspiration
- React and FastAPI communities

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Documentation: See inline code comments
- Community: Join discussions

---

**Built with ❤️ using FastAPI, React, and Whisper AI**
