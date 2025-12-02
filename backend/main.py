"""
FastAPI Backend for Wisprflow Clone
Real-time audio streaming with WebSocket and Whisper transcription
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
import base64
import io
import wave
import logging
from typing import Optional
import tempfile
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Wisprflow API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and React dev servers
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Audio buffer management
class AudioBuffer:
    def __init__(self):
        self.buffer = bytearray()
        self.sample_rate = 16000
        self.channels = 1
        self.sample_width = 2  # 16-bit audio
        
    def add_chunk(self, chunk: bytes):
        """Add audio chunk to buffer"""
        self.buffer.extend(chunk)
        
    def get_wav_bytes(self) -> bytes:
        """Convert buffer to WAV format"""
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(self.sample_width)
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(bytes(self.buffer))
        return wav_buffer.getvalue()
    
    def clear(self):
        """Clear the buffer"""
        self.buffer = bytearray()
    
    def size(self) -> int:
        """Get buffer size in bytes"""
        return len(self.buffer)


# Transcription service
class TranscriptionService:
    """Handles audio transcription using Whisper"""
    
    def __init__(self):
        self.whisper_available = False
        self._init_whisper()
    
    def _init_whisper(self):
        """Initialize Whisper model"""
        try:
            import whisper
            self.model = whisper.load_model("base")
            self.whisper_available = True
            logger.info("Whisper model loaded successfully")
        except ImportError:
            logger.warning("Whisper not installed. Install with: pip install openai-whisper")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
    
    async def transcribe_audio(self, audio_bytes: bytes) -> Optional[str]:
        """Transcribe audio bytes to text"""
        if not self.whisper_available:
            return None
        
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_path = tmp_file.name
            
            # Transcribe
            result = self.model.transcribe(tmp_path, fp16=False)
            
            # Cleanup
            os.unlink(tmp_path)
            
            return result["text"].strip()
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return None


# Initialize services
transcription_service = TranscriptionService()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Wisprflow API",
        "whisper_available": transcription_service.whisper_available
    }


@app.get("/api/status")
async def get_status():
    """Get service status"""
    return {
        "transcription": {
            "available": transcription_service.whisper_available,
            "engine": "whisper" if transcription_service.whisper_available else "none"
        }
    }


@app.websocket("/ws/transcribe")
async def websocket_transcribe(websocket: WebSocket):
    """
    WebSocket endpoint for real-time audio transcription
    
    Expected message format:
    {
        "type": "audio_chunk",  # or "audio_end"
        "data": "base64_encoded_audio"
    }
    """
    await websocket.accept()
    audio_buffer = AudioBuffer()
    
    logger.info("WebSocket connection established")
    
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_json()
            
            msg_type = message.get("type")
            
            if msg_type == "audio_chunk":
                # Decode and buffer audio chunk
                audio_data = base64.b64decode(message.get("data", ""))
                audio_buffer.add_chunk(audio_data)
                
                # Send acknowledgment
                await websocket.send_json({
                    "type": "chunk_received",
                    "buffer_size": audio_buffer.size()
                })
                
            elif msg_type == "audio_end":
                # Process complete audio
                logger.info(f"Processing audio buffer ({audio_buffer.size()} bytes)")
                
                if audio_buffer.size() == 0:
                    await websocket.send_json({
                        "type": "error",
                        "message": "No audio data received"
                    })
                    continue
                
                # Get WAV bytes
                wav_bytes = audio_buffer.get_wav_bytes()
                
                # Transcribe
                text = await transcription_service.transcribe_audio(wav_bytes)
                
                if text:
                    await websocket.send_json({
                        "type": "transcription_result",
                        "text": text
                    })
                    logger.info(f"Transcription: {text}")
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Transcription failed"
                    })
                
                # Clear buffer for next recording
                audio_buffer.clear()
                
            elif msg_type == "ping":
                # Keep-alive
                await websocket.send_json({"type": "pong"})
                
            else:
                await websocket.send_json({
                    "type": "error",
                    "message": f"Unknown message type: {msg_type}"
                })
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
