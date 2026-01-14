"""
Audio recording module for continuous microphone input
"""
import pyaudio
import numpy as np
import threading
import queue
import config
import webrtcvad


class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_queue = queue.Queue() # For transcription (full audio)
        self.raw_queue = queue.Queue()   # For visualizer processing
        self.level_queue = queue.Queue() # For GUI updates
        self.audio_buffer = []
        
        # Initialize VAD
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(3)  # Most aggressive (human voice only)
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self._process_visualizer_data, daemon=True)
        self.processing_thread.start()
        
    def start_recording(self):
        """Start recording audio from microphone"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.audio_buffer = []
        
        # Open audio stream
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=config.AUDIO_CHANNELS,
            rate=config.AUDIO_SAMPLE_RATE,
            input=True,
            frames_per_buffer=config.AUDIO_CHUNK_SIZE,
            stream_callback=self._audio_callback
        )
        
        self.stream.start_stream()
        print("[AudioRecorder] Recording started")
        
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio stream - FAST: just store data"""
        if self.is_recording:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            
            # Store in buffer for later transcription
            self.audio_buffer.append(audio_data)
            
            # Put in queue for visualizer processing (decoupled)
            self.raw_queue.put(audio_data.copy())
            
        return (in_data, pyaudio.paContinue)
    
    def _process_visualizer_data(self):
        """Process audio data for visualizer in a separate thread"""
        while True:
            try:
                audio_data = self.raw_queue.get()
                
                # --- VOICE ACTIVITY DETECTION (VAD) ---
                # webrtcvad needs 10, 20, or 30ms frames. 
                # config.AUDIO_CHUNK_SIZE is 1024, at 16000Hz that's 64ms.
                # We'll split the chunk into smaller pieces for VAD.
                is_speech = False
                frame_duration_ms = 20 # ms
                samples_per_frame = int(config.AUDIO_SAMPLE_RATE * frame_duration_ms / 1000)
                bytes_per_sample = 2 # 16-bit
                
                # Convert numpy back to bytes for VAD
                in_data = audio_data.tobytes()
                
                for i in range(0, len(in_data), samples_per_frame * bytes_per_sample):
                    frame = in_data[i:i + samples_per_frame * bytes_per_sample]
                    if len(frame) < samples_per_frame * bytes_per_sample:
                        break
                    if self.vad.is_speech(frame, config.AUDIO_SAMPLE_RATE):
                        is_speech = True
                        break
                
                # --- ADVANCED VISUALIZER PROCESSING ---
                # 1. Apply Hanning window to reduce spectral leakage
                window = np.hanning(len(audio_data))
                windowed_data = audio_data * window
                
                # 2. Perform FFT
                fft_data = np.abs(np.fft.rfft(windowed_data))
                
                # 3. Group into frequency bands (logarithmic scaling)
                num_bands = 12
                bands = []
                
                max_bin = int(len(fft_data) * 0.5) 
                indices = np.logspace(0, np.log10(max_bin), num_bands + 1, dtype=int)
                
                for i in range(num_bands):
                    start, end = indices[i], indices[i+1]
                    if start == end: end = start + 1
                    band_val = np.mean(fft_data[start:end])
                    bands.append(float(band_val))
                
                # Put the frequency bands AND the speech flag in the queue
                self.level_queue.put((bands, is_speech))
                
            except Exception as e:
                # print(f"Error in visualizer processing: {e}")
                pass
    
    def stop_recording(self):
        """Stop recording and return complete audio data"""
        if not self.is_recording:
            return None
            
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            
        print("[AudioRecorder] Recording stopped")
        
        # Combine all audio chunks
        if self.audio_buffer:
            complete_audio = np.concatenate(self.audio_buffer)
            self.audio_buffer = []  # Clear buffer to free memory
            return complete_audio
        return None
    
    def cancel_recording(self):
        """Cancel recording without returning data"""
        self.is_recording = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            
        self.audio_buffer = []
        
        # Clear queues
        while not self.raw_queue.empty():
            self.raw_queue.get()
        while not self.level_queue.empty():
            self.level_queue.get()
            
        print("[AudioRecorder] Recording cancelled")
    
    def get_audio_level(self):
        """Get current audio frequency bands and speech flag for visualizer"""
        try:
            return self.level_queue.get_nowait()
        except queue.Empty:
            return None
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            self.stream.close()
        self.audio.terminate()
