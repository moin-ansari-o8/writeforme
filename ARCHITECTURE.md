# Wisprflow Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│                     http://localhost:5173                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  App.jsx (Main UI)                        │  │
│  │  - Controls and state management                          │  │
│  │  - Transcription display                                  │  │
│  │  - Theme and error handling                               │  │
│  └────────┬─────────────────────────────────┬────────────────┘  │
│           │                                  │                   │
│           ▼                                  ▼                   │
│  ┌─────────────────────┐          ┌──────────────────────────┐ │
│  │  VoiceVisualizer    │          │  useAudioRecorder Hook   │ │
│  │  - Canvas rendering │          │  - MediaRecorder API     │ │
│  │  - FFT analysis     │          │  - WebSocket client      │ │
│  │  - Idle/Active UI   │          │  - Audio streaming       │ │
│  └─────────────────────┘          └──────────┬───────────────┘ │
│                                               │                  │
└───────────────────────────────────────────────┼──────────────────┘
                                                │
                                    WebSocket Connection
                                    (binary audio chunks)
                                                │
┌───────────────────────────────────────────────▼──────────────────┐
│                      BACKEND (FastAPI)                            │
│                   http://localhost:8000                           │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              WebSocket Handler                              │ │
│  │              /ws/transcribe                                 │ │
│  │  - Receive audio chunks                                     │ │
│  │  - Send acknowledgments                                     │ │
│  │  - Handle audio_end signal                                  │ │
│  └────────┬───────────────────────────────────┬────────────────┘ │
│           │                                    │                 │
│           ▼                                    ▼                 │
│  ┌──────────────────┐              ┌────────────────────────┐  │
│  │  AudioBuffer     │              │  TranscriptionService  │  │
│  │  - Accumulate    │──────────▶   │  - Whisper Model       │  │
│  │  - WAV convert   │   WAV bytes  │  - Audio processing    │  │
│  │  - Manage state  │              │  - Text extraction     │  │
│  └──────────────────┘              └────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Recording Start
```
User clicks "Start Recording"
    ↓
App.jsx calls startRecording()
    ↓
useAudioRecorder requests microphone access
    ↓
MediaRecorder starts capturing audio
    ↓
VoiceVisualizer animates (active state)
```

### 2. Audio Streaming
```
MediaRecorder captures chunks (100ms)
    ↓
FileReader converts to base64
    ↓
WebSocket sends JSON: { type: "audio_chunk", data: "..." }
    ↓
Backend AudioBuffer accumulates data
    ↓
Server sends acknowledgment
```

### 3. Transcription
```
User clicks "Stop Recording"
    ↓
useAudioRecorder sends { type: "audio_end" }
    ↓
Backend converts buffer to WAV
    ↓
Whisper model processes audio
    ↓
Server sends: { type: "transcription_result", text: "..." }
    ↓
Frontend displays transcription
    ↓
VoiceVisualizer returns to idle state
```

## Component Breakdown

### Frontend Components

**App.jsx** (Main Application)
- State management (recording, processing, transcription)
- UI rendering and theme control
- Error handling and user feedback

**VoiceVisualizer.jsx** (Audio Visualization)
- Web Audio API integration
- Canvas 2D rendering
- Idle pulse animation
- Active frequency blob animation

**useAudioRecorder.js** (Audio Capture Hook)
- MediaRecorder API setup
- WebSocket connection management
- Audio chunk streaming
- State management (recording, processing, errors)

### Backend Components

**main.py** (FastAPI Server)
- WebSocket endpoint `/ws/transcribe`
- REST endpoints `/` and `/api/status`
- CORS middleware
- Request/response handling

**AudioBuffer** (Audio Management)
- Byte array accumulation
- WAV format conversion
- Buffer size tracking
- State reset

**TranscriptionService** (AI Processing)
- Whisper model loading
- Audio file processing
- Text extraction
- Error handling

## Technology Stack

### Frontend
- **React 18**: UI framework with hooks
- **Vite**: Build tool and dev server
- **MediaRecorder API**: Audio capture
- **Web Audio API**: Real-time analysis
- **WebSocket**: Binary data streaming
- **Canvas API**: Visualization rendering

### Backend
- **FastAPI**: Async web framework
- **Uvicorn**: ASGI server
- **WebSockets**: Real-time communication
- **OpenAI Whisper**: Speech recognition
- **PyTorch**: ML framework for Whisper

## Network Protocol

### WebSocket Messages

**Client → Server:**
```json
{
  "type": "audio_chunk",
  "data": "base64_encoded_audio_blob"
}

{
  "type": "audio_end"
}

{
  "type": "ping"
}
```

**Server → Client:**
```json
{
  "type": "chunk_received",
  "buffer_size": 12345
}

{
  "type": "transcription_result",
  "text": "Your transcribed text"
}

{
  "type": "error",
  "message": "Error description"
}

{
  "type": "pong"
}
```

## Performance Characteristics

- **Latency**: ~100-500ms (depends on audio length and model)
- **Chunk Size**: 100ms audio chunks
- **Sample Rate**: 16kHz (optimal for Whisper)
- **Channels**: Mono (1 channel)
- **Format**: WebM/Opus (streaming), WAV (processing)

## Scalability Considerations

### Current Limitations
- Single-user per WebSocket connection
- Synchronous transcription (blocking)
- No audio buffering for long recordings

### Potential Improvements
- Queue system for multiple users
- Async transcription with Celery
- Streaming transcription for long audio
- GPU acceleration for Whisper
- Redis for session management
