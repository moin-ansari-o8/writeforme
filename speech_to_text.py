"""
Speech-to-Text module using Faster-Whisper (Offline, Accurate)
"""
from faster_whisper import WhisperModel
import numpy as np
import config
import io
import wave
import tempfile
import os


class SpeechToText:
    def __init__(self):
        print("[SpeechToText] Initializing Faster-Whisper (small model)...")
        
        # Initialize Faster-Whisper with small model
        # compute_type: "int8" for CPU, "float16" for GPU
        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
            download_root=None  # Uses default cache
        )
        
        print("[SpeechToText] Faster-Whisper loaded successfully!")
        
    def transcribe_audio(self, audio_data):
        """
        Transcribe complete audio data to text using Faster-Whisper
        
        Args:
            audio_data: numpy array of int16 audio samples
            
        Returns:
            str: Transcribed text
        """
        if audio_data is None or len(audio_data) == 0:
            return ""
        
        try:
            # Convert int16 to float32 normalized to [-1.0, 1.0]
            audio_float = audio_data.astype(np.float32) / 32768.0
            
            print("[SpeechToText] Transcribing with Faster-Whisper...")
            
            # Transcribe using Faster-Whisper
            segments, info = self.model.transcribe(
                audio_float,
                language="en",
                beam_size=5,
                vad_filter=True,  # Voice Activity Detection
                vad_parameters=dict(
                    min_silence_duration_ms=500,
                    threshold=0.3
                )
            )
            
            # Combine all segments into single text
            transcription = " ".join([segment.text for segment in segments]).strip()
            
            print(f"[SpeechToText] Transcription complete: {transcription}")
            
            return transcription
            
        except Exception as e:
            print(f"[SpeechToText] Error: {e}")
            return ""
    
    def _numpy_to_wav(self, audio_data):
        """Convert numpy array to WAV format bytes (kept for compatibility)"""
        wav_buffer = io.BytesIO()
        
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(config.AUDIO_CHANNELS)
            wav_file.setsampwidth(2)  # 2 bytes for int16
            wav_file.setframerate(config.AUDIO_SAMPLE_RATE)
            wav_file.writeframes(audio_data.tobytes())
        
        wav_buffer.seek(0)
        return wav_buffer.read()
    
    def transcribe_stream(self, audio_stream):
        """
        Real-time transcription from audio stream (for future enhancement)
        
        Args:
            audio_stream: Generator yielding audio chunks
            
        Returns:
            str: Transcribed text
        """
        # This is a placeholder for potential streaming implementation
        # Currently we transcribe the complete audio after stop is pressed
        pass
