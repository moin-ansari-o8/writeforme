"""
Audio recording module for continuous microphone input
"""
import pyaudio
import numpy as np
import threading
import queue
import config


class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.level_queue = queue.Queue()  # For visualizer
        self.audio_buffer = []
        
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
        """Callback for audio stream - processes each audio chunk"""
        if self.is_recording:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            
            # Store in buffer for later transcription
            self.audio_buffer.append(audio_data)
            
            # Put in queue for real-time processing
            self.audio_queue.put(audio_data.copy())
            
            # Calculate audio level for visualizer
            audio_level = np.abs(audio_data).mean()
            self.level_queue.put(audio_level)
            
        return (in_data, pyaudio.paContinue)
    
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
        while not self.audio_queue.empty():
            self.audio_queue.get()
        while not self.level_queue.empty():
            self.level_queue.get()
            
        print("[AudioRecorder] Recording cancelled")
    
    def get_audio_level(self):
        """Get current audio level for visualizer"""
        try:
            return self.level_queue.get_nowait()
        except queue.Empty:
            return 0
    
    def get_audio_chunk(self):
        """Get audio chunk for real-time processing"""
        try:
            return self.audio_queue.get_nowait()
        except queue.Empty:
            return None
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            self.stream.close()
        self.audio.terminate()
