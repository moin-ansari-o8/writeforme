"""
Speech-to-Text using faster-whisper (LOCAL)
Faster and more efficient than original Whisper
"""
from faster_whisper import WhisperModel
import numpy as np
import wave
import io
import tempfile
import os


class FasterWhisperSTT:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        """
        Initialize faster-whisper model
        
        Args:
            model_size: "tiny", "base", "small", "medium", "large-v2", "large-v3"
                       - tiny: fastest, least accurate
                       - base: good balance (recommended for testing)
                       - small: better accuracy
                       - medium/large: highest accuracy, slower
            device: "cpu" or "cuda" (GPU)
            compute_type: "int8" (fastest), "int8_float16", "float16", "float32"
        """
        print(f"[FasterWhisper] Loading {model_size} model on {device}...")
        self.model = WhisperModel(
            model_size, 
            device=device, 
            compute_type=compute_type
        )
        print(f"[FasterWhisper] Model loaded successfully!")
        
    def transcribe_audio(self, audio_data, sample_rate=16000, language="en"):
        """
        Transcribe audio numpy array to text
        
        Args:
            audio_data: numpy array of int16 audio samples
            sample_rate: audio sample rate (default 16000)
            language: language code ("en", "es", "fr", etc.) or None for auto-detect
            
        Returns:
            str: Transcribed text
        """
        if audio_data is None or len(audio_data) == 0:
            return ""
        
        try:
            # Convert int16 numpy array to float32 normalized to [-1, 1]
            audio_float = audio_data.astype(np.float32) / 32768.0
            
            # Transcribe
            print("[FasterWhisper] Transcribing audio...")
            segments, info = self.model.transcribe(
                audio_float,
                language=language,
                beam_size=5,
                vad_filter=True,  # Voice Activity Detection
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Detected language
            print(f"[FasterWhisper] Detected language: {info.language} ({info.language_probability:.2f})")
            
            # Combine all segments
            text = " ".join([segment.text.strip() for segment in segments])
            print(f"[FasterWhisper] Transcription: {text}")
            
            return text.strip()
            
        except Exception as e:
            print(f"[FasterWhisper] Error: {e}")
            return ""
    
    def transcribe_from_file(self, audio_file_path, language="en"):
        """
        Transcribe audio from file
        
        Args:
            audio_file_path: path to audio file (wav, mp3, etc.)
            language: language code or None for auto-detect
            
        Returns:
            str: Transcribed text
        """
        try:
            print(f"[FasterWhisper] Transcribing file: {audio_file_path}")
            segments, info = self.model.transcribe(
                audio_file_path,
                language=language,
                beam_size=5,
                vad_filter=True
            )
            
            print(f"[FasterWhisper] Detected language: {info.language} ({info.language_probability:.2f})")
            text = " ".join([segment.text.strip() for segment in segments])
            
            return text.strip()
            
        except Exception as e:
            print(f"[FasterWhisper] Error: {e}")
            return ""


def test_with_microphone():
    """
    Test faster-whisper with microphone input
    Requires: pip install pyaudio
    """
    import pyaudio
    
    # Audio settings
    SAMPLE_RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5
    
    print("\n=== Faster-Whisper Microphone Test ===")
    print(f"Recording for {RECORD_SECONDS} seconds...")
    
    # Initialize faster-whisper
    stt = FasterWhisperSTT(model_size="base", device="cpu", compute_type="int8")
    
    # Record audio
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    print("Recording...")
    frames = []
    for _ in range(0, int(SAMPLE_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording complete!")
    
    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Convert to numpy array
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    
    # Transcribe
    text = stt.transcribe_audio(audio_data, sample_rate=SAMPLE_RATE)
    
    print(f"\n✅ RESULT: {text}")
    return text


def test_with_microphone_custom(model_size="base"):
    """
    Test faster-whisper with continuous microphone input
    Requires: pip install pyaudio
    Press Ctrl+C to stop
    """
    import pyaudio
    
    # Audio settings
    SAMPLE_RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 5  # Record in 5-second chunks
    
    print(f"\n=== Faster-Whisper Continuous Listening [{model_size.upper()}] ===")
    print("🎤 Starting continuous listening mode...")
    print("⏹ Press Ctrl+C to STOP\n")
    
    # Initialize faster-whisper with selected model
    stt = FasterWhisperSTT(model_size=model_size, device="cpu", compute_type="int8")
    
    # Record audio
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    try:
        chunk_count = 1
        while True:
            print(f"\n🔴 Recording chunk #{chunk_count}... (SPEAK NOW)")
            frames = []
            for _ in range(0, int(SAMPLE_RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            print("⚙ Processing...")
            
            # Convert to numpy array
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
            
            # Transcribe
            text = stt.transcribe_audio(audio_data, sample_rate=SAMPLE_RATE)
            
            if text:
                print(f"✅ TRANSCRIPTION: {text}")
            else:
                print("⚪ (silence detected)")
            
            chunk_count += 1
            
    except KeyboardInterrupt:
        print("\n\n⏹ Stopping continuous listening...")
    finally:
        # Stop recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("✅ Microphone closed. Goodbye!")
    
    return None


def test_with_file_custom(file_path, model_size="base"):
    """
    Test faster-whisper with audio file and custom model
    """
    print(f"\n=== Faster-Whisper File Test [{model_size.upper()}] ===")
    print(f"File: {file_path}")
    
    # Initialize faster-whisper with selected model
    stt = FasterWhisperSTT(model_size=model_size, device="cpu", compute_type="int8")
    
    # Transcribe
    text = stt.transcribe_from_file(file_path)
    
    print(f"\n✅ TRANSCRIPTION: {text}")
    return text


def benchmark_models():
    
    # Record audio
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    print("🎤 Recording... SPEAK NOW!")
    frames = []
    for _ in range(0, int(SAMPLE_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording complete!")
    
    # Stop recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Convert to numpy array
    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    
    # Transcribe
    text = stt.transcribe_audio(audio_data, sample_rate=SAMPLE_RATE)
    
    print(f"\n✅ TRANSCRIPTION: {text}")
    return text


def test_with_file(file_path):
    """
    Test faster-whisper with audio file
    """
    print("\n=== Faster-Whisper File Test ===")
    print(f"File: {file_path}")
    
    # Initialize faster-whisper
    stt = FasterWhisperSTT(model_size="base", device="cpu", compute_type="int8")
    
    # Transcribe
    text = stt.transcribe_from_file(file_path)
    
    print(f"\n✅ RESULT: {text}")
    return text


def benchmark_models():
    """
    Compare different model sizes
    """
    import time
    
    print("\n=== Faster-Whisper Model Benchmark ===")
    
    # Create test audio (5 seconds of silence for quick test)
    audio_data = np.zeros(16000 * 5, dtype=np.int16)
    
    models = ["tiny", "base", "small"]
    
    for model_size in models:
        print(f"\nTesting {model_size} model...")
        start = time.time()
        
        stt = FasterWhisperSTT(model_size=model_size)
        stt.transcribe_audio(audio_data)
        
        elapsed = time.time() - start
        print(f"⏱ {model_size}: {elapsed:.2f}s")


def select_model():
    """
    Let user select which model to use
    """
    print("""
╔══════════════════════════════════════════╗
║        SELECT WHISPER MODEL              ║
╚══════════════════════════════════════════╝

Available models:
  1. tiny   - 39M params  - ⚡ FASTEST (least accurate)
  2. base   - 74M params  - ⚖ BALANCED (recommended)
  3. small  - 244M params - 🎯 ACCURATE (slower)
  4. medium - 769M params - 🏆 VERY ACCURATE (slow)
  5. large  - 1550M params - 🌟 BEST (very slow)
""")
    
    model_choice = input("Choose model (1-5, default=2): ").strip() or "2"
    
    model_map = {
        "1": "tiny",
        "2": "base",
        "3": "small",
        "4": "medium",
        "5": "large-v3"
    }
    
    model_size = model_map.get(model_choice, "base")
    print(f"\n✓ Selected: {model_size} model\n")
    return model_size


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════╗
║   Faster-Whisper Speech-to-Text Test    ║
║         LOCAL - NO INTERNET NEEDED       ║
╚══════════════════════════════════════════╝

Requirements:
  pip install faster-whisper

Choose test:
  1. Microphone test (requires pyaudio)
  2. Audio file test
  3. Model benchmark
  4. Quick test with dummy data
""")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        model_size = select_model()
        test_with_microphone_custom(model_size)
    elif choice == "2":
        model_size = select_model()
        file_path = input("Enter audio file path: ").strip()
        test_with_file_custom(file_path, model_size)
    elif choice == "3":
        benchmark_models()
    elif choice == "4":
        model_size = select_model()
        print(f"\n=== Quick Test with {model_size} ===")
        stt = FasterWhisperSTT(model_size=model_size)
        # Test with 1 second of silence
        audio = np.zeros(16000, dtype=np.int16)
        result = stt.transcribe_audio(audio)
        print(f"Result: '{result}' (expected empty for silence)")
    else:
        print("Invalid choice!")
