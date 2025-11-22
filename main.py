"""
Wispr Flow Local - Main Application
A local Python clone of Wispr Flow using speech recognition and LLaMA AI

Usage:
    python main.py
"""
import threading
import time
from audio_recorder import AudioRecorder
from speech_to_text import SpeechToText
from ai_refiner import AIRefiner
from paste_manager import PasteManager
from gui_widget import WidgetGUI
from data_storage import DataStorage


class WisprFlowLocal:
    def __init__(self):
        print("=" * 60)
        print("Wispr Flow Local - Starting...")
        print("=" * 60)
        
        # Initialize components
        self.audio_recorder = AudioRecorder()
        self.speech_to_text = SpeechToText()
        self.ai_refiner = AIRefiner()
        self.paste_manager = PasteManager()
        self.data_storage = DataStorage()
        
        # GUI will be initialized in main thread
        self.gui = None
        
        # State
        self.is_processing = False
        
    def on_cancel(self):
        """Handle cancel button press"""
        print("\n[Main] Cancelling recording...")
        self.audio_recorder.cancel_recording()
        
        # Hide widget instead of restarting
        if self.gui:
            self.gui.hide()
            print("[Main] Widget hidden (Cancelled)")
        
        # time.sleep(0.2)
        # self.audio_recorder.start_recording()
        # print("[Main] Recording restarted. Speak to continue...\n")
    
    def on_stop(self):
        """Handle stop button press"""
        if self.is_processing:
            print("[Main] Already processing, please wait...")
            return
        
        self.is_processing = True
        
        print("\n[Main] Stop button pressed - Processing...")
        print("-" * 60)
        
        # Switch UI to processing mode immediately
        if self.gui:
            self.gui.show_processing()
        
        # Stop recording and get audio data
        audio_data = self.audio_recorder.stop_recording()
        
        if audio_data is None or len(audio_data) == 0:
            print("[Main] No audio recorded")
            self.is_processing = False
            # Restart recording
            self.audio_recorder.start_recording()
            return
        
        # Process in separate thread to avoid blocking GUI
        threading.Thread(target=self._process_audio, args=(audio_data,), daemon=True).start()
    
    def _process_audio(self, audio_data):
        """Process audio in background thread"""
        try:
            # Get current mode from GUI
            current_mode = "default"
            if self.gui:
                current_mode = self.gui.get_current_mode()
                # Update AI refiner mode
                self.ai_refiner.set_mode(current_mode)
            
            # Step 1: Speech to Text
            print("[Main] Step 1/4: Transcribing speech...")
            transcribed_text = self.speech_to_text.transcribe_audio(audio_data)
            
            if not transcribed_text or transcribed_text.strip() == "":
                print("[Main] No speech detected in recording")
                self.is_processing = False
                if self.gui:
                    self.gui.show_recording()
                self.audio_recorder.start_recording()
                return
            
            print(f"[Main] Transcribed: {transcribed_text}")
            
            # Step 2: AI Refinement
            print("[Main] Step 2/4: Refining with AI...")
            refined_text = self.ai_refiner.refine_text(transcribed_text)
            
            print(f"[Main] Refined: {refined_text}")
            
            # Step 3: Save to storage (ALWAYS save, regardless of paste success)
            print("[Main] Step 3/4: Saving to storage...")
            self.data_storage.save_transcription(
                mode=current_mode,
                raw_text=transcribed_text,
                refined_text=refined_text,
                paste_success=False  # Will update if paste succeeds
            )
            
            # Step 4: Paste
            print("[Main] Step 4/4: Pasting text...")
            success = self.paste_manager.paste_text(refined_text)
            
            if success:
                print("[Main] ✓ Text pasted successfully!")
                # Update storage with paste success
                self.data_storage.save_transcription(
                    mode=current_mode,
                    raw_text=transcribed_text,
                    refined_text=refined_text,
                    paste_success=True
                )
            else:
                print("[Main] ✗ Failed to paste text")
                print("[Main] Text copied to clipboard and saved to storage")
            
            print("-" * 60)
            print("[Main] Ready for next dictation\n")
            
        except Exception as e:
            print(f"[Main] Error processing audio: {e}")
        
        finally:
            # Switch GUI back to recording mode but HIDE it
            if self.gui:
                self.gui.show_recording() # Reset state internally
                self.gui.hide() # Hide the window
                print("[Main] Widget hidden. Processing complete.")
            
            # Do NOT restart recording automatically
            self.is_processing = False
            # time.sleep(0.5)
            # self.audio_recorder.start_recording()
    
    def _update_visualizer_loop(self):
        """Update visualizer with audio levels"""
        while True:
            try:
                level = self.audio_recorder.get_audio_level()
                if self.gui:
                    self.gui.update_visualizer(level)
                time.sleep(0.05)  # 20 FPS
            except:
                break
    
    def run(self):
        """Main application loop"""
        # Test AI connection
        print("\n[Main] Testing AI connection...")
        if not self.ai_refiner.test_connection():
            print("[Main] WARNING: AI connection test failed")
            print("[Main] Make sure Ollama is running: ollama serve")
            print("[Main] Continuing anyway (will use original transcription if AI fails)")
        
        print("\n[Main] Initializing GUI...")
        
        # Create GUI (must be in main thread)
        self.gui = WidgetGUI(
            on_cancel_callback=self.on_cancel,
            on_stop_callback=self.on_stop
        )
        
        # Start audio recording
        print("[Main] Starting audio recording...")
        self.audio_recorder.start_recording()
        
        # Start visualizer update thread
        visualizer_thread = threading.Thread(target=self._update_visualizer_loop, daemon=True)
        visualizer_thread.start()
        
        print("\n" + "=" * 60)
        print("Ready! Speak and press STOP when done.")
        print("Press CANCEL to discard and restart.")
        print("=" * 60 + "\n")
        
        # Start GUI (blocking call)
        try:
            self.gui.start()
        except KeyboardInterrupt:
            print("\n[Main] Interrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\n[Main] Cleaning up...")
        self.audio_recorder.cleanup()
        if self.gui:
            self.gui.destroy()
        print("[Main] Goodbye!")


def main():
    """Entry point"""
    app = WisprFlowLocal()
    app.run()


if __name__ == "__main__":
    main()
