"""
Speech-to-Text module using Google Speech Recognition
"""
import speech_recognition as sr
import numpy as np
import config
import io
import wave


class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
    def transcribe_audio(self, audio_data):
        """
        Transcribe complete audio data to text
        
        Args:
            audio_data: numpy array of int16 audio samples
            
        Returns:
            str: Transcribed text
        """
        if audio_data is None or len(audio_data) == 0:
            return ""
        
        try:
            # Convert numpy array to WAV bytes
            audio_bytes = self._numpy_to_wav(audio_data)
            
            # Create AudioData object for speech_recognition
            audio = sr.AudioData(
                audio_bytes, 
                config.AUDIO_SAMPLE_RATE, 
                2  # 2 bytes per sample (int16)
            )
            
            # Perform speech recognition
            print("[SpeechToText] Transcribing audio...")
            text = self.recognizer.recognize_google(audio, language="en-US")
            print(f"[SpeechToText] Transcription complete: {text}")
            
            return text
            
        except sr.UnknownValueError:
            print("[SpeechToText] Could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"[SpeechToText] API error: {e}")
            # Try offline recognition as fallback
            try:
                text = self.recognizer.recognize_sphinx(audio)
                print(f"[SpeechToText] Offline transcription: {text}")
                return text
            except:
                print("[SpeechToText] Offline recognition also failed")
                return ""
        except Exception as e:
            print(f"[SpeechToText] Error: {e}")
            return ""
    
    def _numpy_to_wav(self, audio_data):
        """Convert numpy array to WAV format bytes"""
        # Create in-memory WAV file
        wav_buffer = io.BytesIO()
        
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(config.AUDIO_CHANNELS)
            wav_file.setsampwidth(2)  # 2 bytes for int16
            wav_file.setframerate(config.AUDIO_SAMPLE_RATE)
            wav_file.writeframes(audio_data.tobytes())
        
        # Get raw audio data (skip WAV header)
        wav_buffer.seek(0)
        wav_data = wav_buffer.read()
        
        # Return just the raw audio data (speech_recognition adds its own header)
        return audio_data.tobytes()
    
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
