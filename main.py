"""
Wispr Flow Local - Main Application
A local Python clone of Wispr Flow using speech recognition and AI
Now with global hotkey support, multiple AI providers, and streaming chunk processing

Features:
    - Streaming transcription: Processes audio in 15-second chunks during recording
    - Handles long speeches with pauses without breaking context
    - Combines all chunks when you stop for complete, refined output
    - Background processing: Keep speaking while previous chunks transcribe

Usage:
    python main.py
    
Hotkeys:
    Win+Shift (Hold) - Push-to-talk mode
    Win+Ctrl+Shift (Press) - Toggle recording mode
"""
import threading
import time
import ctypes # For High DPI awareness
from pynput import keyboard as pynput_keyboard
from colorama import Fore, Back, Style, init
from audio_recorder import AudioRecorder
from speech_to_text import SpeechToText
from ai_provider_manager import AIProviderManager
from paste_manager import PasteManager
from gui_widget import WidgetGUI
from data_storage import DataStorage
import config

# Initialize colorama for colored terminal output
init(autoreset=True)

# Enable High DPI Awareness to fix pixelation
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()


class WisprFlowLocal:
    def __init__(self, silent_mode=False):
        # Default to NO AI mode - direct speech-to-text only
        self.use_ai_refinement = False
        self.ai_manager = None
        
        if not silent_mode:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
            print(f"{Fore.CYAN}{Style.BRIGHT}{'🎤  WriteForMe - Speech-to-Text Assistant':^70}")
            print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")
            print(f"{Fore.YELLOW}✓ Mode: Direct transcription (no AI refinement){Style.RESET_ALL}")
            print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")
        
        # Initialize other components
        if not silent_mode:
            print(f"{Fore.YELLOW}⏳ Initializing components...{Style.RESET_ALL}")
        self.audio_recorder = AudioRecorder()
        self.speech_to_text = SpeechToText()
        self.paste_manager = PasteManager()
        self.data_storage = DataStorage(max_entries=config.MAX_HISTORY_ENTRIES)
        
        # Set up chunk callback for streaming transcription
        self.audio_recorder.set_chunk_callback(self._on_audio_chunk)
        self.transcribed_chunks = []  # Store chunks during recording
        self.chunk_lock = threading.Lock()  # Thread safety for chunk list
        self.active_chunk_threads = []  # Track in-flight chunk processing threads
        self.thread_lock = threading.Lock()  # Thread safety for thread list
        self.recording_start_time = None  # Track total time
        
        if not silent_mode:
            print(f"{Fore.GREEN}✓ All components ready!{Style.RESET_ALL}\n")
        
        # GUI will be initialized in main thread
        self.gui = None
        
        # Recording state
        self.is_processing = False
        self.is_recording = False
        self.toggle_mode_active = False  # For Win+Ctrl+Shift toggle mode
        
        # Hotkey tracking
        self.hotkey_listener = None
        self.push_to_talk_pressed = False
        self.current_modifiers = set()
        
    def on_cancel(self):
        """Handle cancel button press"""
        print(f"\n{Fore.RED}✖ Cancelling recording...{Style.RESET_ALL}")
        self.audio_recorder.cancel_recording()
        
        # Hide widget and reset state
        if self.gui:
            self.gui.hide()
            print(f"{Fore.YELLOW}⦿ Widget hidden (Cancelled){Style.RESET_ALL}")
        
        self.is_recording = False
        self.toggle_mode_active = False
    
    def start_recording(self):
        """Start recording - called by hotkey"""
        if self.is_processing:
            print(f"{Fore.YELLOW}⏳ Already processing, please wait...{Style.RESET_ALL}")
            return
        
        if self.is_recording:
            print(f"{Fore.YELLOW}⦿ Already recording...{Style.RESET_ALL}")
            return
        
        from datetime import datetime
        start_timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{Fore.GREEN}{Style.BRIGHT}▶ [{start_timestamp}] Started listening...{Style.RESET_ALL}")
        self.is_recording = True
        self.recording_start_time = time.time()  # Track start time
        
        # Clear previous chunks
        with self.chunk_lock:
            self.transcribed_chunks = []
        
        # Start audio recording
        self.audio_recorder.start_recording()
        print(f"{Fore.CYAN}🎤 Listening... Speak now!{Style.RESET_ALL}")
        
        # Show GUI after starting recording
        if self.gui:
            self.gui.show()
            self.gui.show_recording()
            # Force window to top and update
            self.gui.root.lift()
            self.gui.root.attributes('-topmost', True)
            self.gui.root.update()
    
    def stop_recording_and_process(self):
        """Stop recording and process audio - called by hotkey"""
        if not self.is_recording:
            print(f"{Fore.YELLOW}⦿ Not recording, ignoring...{Style.RESET_ALL}")
            return
        
        if self.is_processing:
            print(f"{Fore.YELLOW}⏳ Already processing, please wait...{Style.RESET_ALL}")
            return
        
        self.is_recording = False
        self.is_processing = True
        
        from datetime import datetime
        stop_timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n{Fore.YELLOW}⏹ [{stop_timestamp}] Stopped recording - Processing...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        
        # Switch UI to processing mode immediately
        if self.gui:
            self.gui.show_processing()
        
        # Stop recording and get remaining audio (only what hasn't been chunked yet)
        audio_data = self.audio_recorder.stop_recording()
        
        # Process in separate thread to avoid blocking
        processing_start = time.time()
        threading.Thread(target=self._process_audio, args=(audio_data, processing_start), daemon=True).start()
    
    def _remove_duplicate_sentences(self, chunks):
        """Remove duplicate sentences from combined chunks"""
        if not chunks:
            return ""
        
        # Combine all chunks
        full_text = " ".join(chunks)
        
        # Split into phrases (using both punctuation and commas)
        import re
        # Split on: . ! ? , ; and multiple spaces
        phrases = re.split(r'[.,;!?]+\s*', full_text)
        
        # Clean and filter phrases
        cleaned_phrases = []
        for phrase in phrases:
            phrase = phrase.strip()
            if phrase:  # Skip empty
                cleaned_phrases.append(phrase)
        
        # Remove consecutive duplicates (case-insensitive)
        unique_phrases = []
        previous_normalized = None
        
        for phrase in cleaned_phrases:
            normalized = phrase.lower().strip()
            
            # Skip if same as previous phrase
            if normalized != previous_normalized:
                unique_phrases.append(phrase)
                previous_normalized = normalized
        
        # Count removed duplicates
        removed = len(cleaned_phrases) - len(unique_phrases)
        if removed > 0:
            print(f"{Fore.YELLOW}🔧 Removed {removed} duplicate phrase(s){Style.RESET_ALL}")
        
        # Join back with proper spacing
        result = ", ".join(unique_phrases) + "."
        
        return result
    
    def _on_audio_chunk(self, chunk_audio, chunk_start_time):
        """Callback for processing audio chunks in background"""
        # Track this thread
        current_thread = threading.current_thread()
        with self.thread_lock:
            self.active_chunk_threads.append(current_thread)
        
        try:
            # Don't process chunks if recording already stopped
            if not self.is_recording:
                return
            
            from datetime import datetime
            chunk_num = len(self.transcribed_chunks) + 1
            start_timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{Fore.MAGENTA}📦 [{start_timestamp}] Chunk #{chunk_num} - Starting transcription...{Style.RESET_ALL}")
            
            # Transcribe chunk
            transcribe_start = time.time()
            chunk_text = self.speech_to_text.transcribe_audio(chunk_audio)
            transcribe_duration = time.time() - transcribe_start
            
            if chunk_text and chunk_text.strip():
                with self.chunk_lock:
                    # Avoid duplicates - check if this chunk is already processed
                    if not self.transcribed_chunks or chunk_text.strip() != self.transcribed_chunks[-1]:
                        self.transcribed_chunks.append(chunk_text.strip())
                        end_timestamp = datetime.now().strftime("%H:%M:%S")
                        print(f"{Fore.GREEN}✓ [{end_timestamp}] Chunk #{chunk_num} completed in {transcribe_duration:.1f}s: {chunk_text[:50]}...{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}✗ Chunk transcription error: {e}{Style.RESET_ALL}")
        finally:
            # Always remove thread from tracking when done
            with self.thread_lock:
                if current_thread in self.active_chunk_threads:
                    self.active_chunk_threads.remove(current_thread)
    
    def on_stop(self, mode="ai"):
        """Handle stop button press from GUI"""
        self.stop_recording_and_process()
    
    def _process_audio(self, audio_data, processing_start):
        """Process audio in background thread"""
        try:
            # Get current mode
            current_mode = "vibe_coder"
            if self.gui:
                current_mode = self.gui.get_current_mode()
            
            # Wait for all in-flight chunk transcriptions to complete
            max_wait = 30  # Maximum 30 seconds wait
            wait_start = time.time()
            last_count = -1
            
            while True:
                with self.thread_lock:
                    active_count = len(self.active_chunk_threads)
                
                # All chunks completed
                if active_count == 0:
                    break
                
                # Show progress when count changes
                if active_count != last_count:
                    print(f"{Fore.YELLOW}⏳ Waiting for {active_count} chunk(s) to complete...{Style.RESET_ALL}")
                    last_count = active_count
                
                # Timeout protection
                elapsed = time.time() - wait_start
                if elapsed > max_wait:
                    print(f"{Fore.RED}⚠️  Timeout: {active_count} chunk(s) still processing after {max_wait}s{Style.RESET_ALL}")
                    break
                
                # Poll every 100ms
                time.sleep(0.1)
            
            # Step 1: Transcribe only remaining audio (after last chunk)
            final_transcription = ""
            
            if audio_data is not None and len(audio_data) > 0:
                # Only transcribe if there's significant remaining audio (> 0.5 second)
                remaining_duration = len(audio_data) / config.AUDIO_SAMPLE_RATE
                
                if remaining_duration > 0.5:
                    print(f"{Fore.CYAN}[1/4] 🎯 Transcribing final {remaining_duration:.1f}s...{Style.RESET_ALL}")
                    final_transcription = self.speech_to_text.transcribe_audio(audio_data)
                else:
                    print(f"{Fore.CYAN}[1/4] ⏭ Skipping final transcription (only {remaining_duration:.1f}s remaining){Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}[1/4] ⏭ No remaining audio to transcribe{Style.RESET_ALL}")
            
            # Step 2: Combine all chunks with final transcription
            with self.chunk_lock:
                all_chunks = self.transcribed_chunks.copy()
            
            # Add final transcription if it has new content
            if final_transcription and final_transcription.strip():
                # Check for duplicates before adding
                if not all_chunks or final_transcription.strip() != all_chunks[-1]:
                    all_chunks.append(final_transcription.strip())
            
            # Step 2.5: Remove duplicate sentences
            transcribed_text = self._remove_duplicate_sentences(all_chunks)
            
            if transcribed_text:
                print(f"{Fore.GREEN}✓ Combined {len(all_chunks)} segments (duplicates removed){Style.RESET_ALL}")
            else:
                transcribed_text = ""
            
            if not transcribed_text or transcribed_text.strip() == "":
                print(f"{Fore.RED}✗ No speech detected{Style.RESET_ALL}")
                self.is_processing = False
                if self.gui:
                    self.gui.hide()
                return
            
            print(f"{Fore.GREEN}✓ Complete transcription: {Fore.WHITE}{transcribed_text[:100]}...{Style.RESET_ALL}")
            
            # Step 3: AI Refinement (if enabled)
            if self.use_ai_refinement:
                print(f"{Fore.CYAN}[2/4] ✨ Refining with {self.ai_manager.get_provider_name()}...{Style.RESET_ALL}")
                
                prompt_template = config.WRITING_MODES.get(current_mode, config.WRITING_MODES["vibe_coder"])["prompt"]
                refined_text = self.ai_manager.refine_text(transcribed_text, prompt_template)
                
                # Apply post-processing for vibe_coder mode (backup layer)
                if current_mode == "vibe_coder":
                    refined_text = config.post_process_coding_text(refined_text)
                
                print(f"{Fore.GREEN}✓ Refined: {Fore.WHITE}{refined_text[:100]}...{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}[2/4] ⏭ Skipping AI refinement (raw mode){Style.RESET_ALL}")
                refined_text = transcribed_text
            
            # Step 3: Save to storage
            print(f"{Fore.CYAN}[3/4] 💾 Saving to storage...{Style.RESET_ALL}")
            self.data_storage.save_transcription(
                mode=current_mode,
                raw_text=transcribed_text,
                refined_text=refined_text,
                paste_success=False
            )
            
            # Step 4: Paste
            print(f"{Fore.CYAN}[4/4] 📋 Pasting text...{Style.RESET_ALL}")
            success = self.paste_manager.paste_text(refined_text)
            
            if success:
                print(f"{Fore.GREEN}✓ Text pasted successfully!{Style.RESET_ALL}")
                self.data_storage.save_transcription(
                    mode=current_mode,
                    raw_text=transcribed_text,
                    refined_text=refined_text,
                    paste_success=True
                )
            else:
                print(f"{Fore.YELLOW}⚠ Paste failed, copied to clipboard{Style.RESET_ALL}")
            
            # Calculate and display total time
            from datetime import datetime
            end_timestamp = datetime.now().strftime("%H:%M:%S")
            total_time = time.time() - self.recording_start_time
            processing_time = time.time() - processing_start
            
            print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⏱️  [{end_timestamp}] Processing completed{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⏱️  Total: {total_time:.1f}s (Recording: {total_time - processing_time:.1f}s | Processing: {processing_time:.1f}s){Style.RESET_ALL}")
            print(f"{Fore.GREEN}✓ Ready for next dictation{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{Style.BRIGHT}✓ Ready for next dictation{Style.RESET_ALL}\n")
            
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        
        finally:
            # Hide GUI and reset state
            if self.gui:
                self.gui.show_recording()
                self.gui.hide()
            
            self.is_processing = False
    
    def _update_visualizer_loop(self):
        """Update visualizer with audio levels"""
        while True:
            try:
                level = self.audio_recorder.get_audio_level()
                if self.gui and self.is_recording:
                    self.gui.update_visualizer(level)
                    time.sleep(0.03)  # ~33 FPS when recording
                else:
                    time.sleep(0.1)  # Longer sleep when idle to save CPU
            except:
                break
    
    def _setup_hotkeys(self):
        """Setup global hotkeys using pynput"""
        print(f"\n{Fore.YELLOW}🔧 Setting up global hotkeys...{Style.RESET_ALL}")
        
        def on_press(key):
            """Handle key press events"""
            try:
                # Track modifier keys
                if key in (pynput_keyboard.Key.cmd, pynput_keyboard.Key.cmd_l, pynput_keyboard.Key.cmd_r):
                    self.current_modifiers.add('win')
                elif key in (pynput_keyboard.Key.ctrl, pynput_keyboard.Key.ctrl_l, pynput_keyboard.Key.ctrl_r):
                    self.current_modifiers.add('ctrl')
                elif key in (pynput_keyboard.Key.shift, pynput_keyboard.Key.shift_l, pynput_keyboard.Key.shift_r):
                    self.current_modifiers.add('shift')
                
                # Check for Win+Ctrl+Shift (toggle mode)
                if {'win', 'ctrl', 'shift'} == self.current_modifiers:
                    if not self.push_to_talk_pressed:
                        self._on_toggle_mode()
                    return
                
                # Check for Win+Shift (push-to-talk)
                if {'win', 'shift'} == self.current_modifiers and 'ctrl' not in self.current_modifiers:
                    if not self.push_to_talk_pressed and not self.toggle_mode_active:
                        self.push_to_talk_pressed = True
                        self._on_push_to_talk_start()
                    return
                    
            except Exception as e:
                print(f"{Fore.RED}Error in key press: {e}{Style.RESET_ALL}")
        
        def on_release(key):
            """Handle key release events"""
            try:
                # Track modifier keys
                if key in (pynput_keyboard.Key.cmd, pynput_keyboard.Key.cmd_l, pynput_keyboard.Key.cmd_r):
                    self.current_modifiers.discard('win')
                elif key in (pynput_keyboard.Key.ctrl, pynput_keyboard.Key.ctrl_l, pynput_keyboard.Key.ctrl_r):
                    self.current_modifiers.discard('ctrl')
                elif key in (pynput_keyboard.Key.shift, pynput_keyboard.Key.shift_l, pynput_keyboard.Key.shift_r):
                    self.current_modifiers.discard('shift')
                
                # Check if push-to-talk was released
                if self.push_to_talk_pressed:
                    if 'win' not in self.current_modifiers or 'shift' not in self.current_modifiers:
                        self.push_to_talk_pressed = False
                        self._on_push_to_talk_release()
                        
            except Exception as e:
                print(f"{Fore.RED}Error in key release: {e}{Style.RESET_ALL}")
        
        # Start listener in background thread
        self.hotkey_listener = pynput_keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )
        self.hotkey_listener.start()
        
        print(f"{Fore.GREEN}✓ Hotkeys registered:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  • Win+Shift (Hold) - Push-to-talk mode{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  • Win+Ctrl+Shift (Press) - Toggle recording mode{Style.RESET_ALL}")
    
    def _on_push_to_talk_start(self):
        """Handle Win+Shift press (start recording)"""
        if not self.toggle_mode_active and not self.is_processing:
            print(f"{Fore.MAGENTA}🔘 Push-to-talk: Starting...{Style.RESET_ALL}")
            self.start_recording()
    
    def _on_push_to_talk_release(self):
        """Handle Win+Shift release (stop recording)"""
        if self.is_recording and not self.toggle_mode_active:
            print(f"{Fore.MAGENTA}🔘 Push-to-talk: Released, stopping...{Style.RESET_ALL}")
            self.stop_recording_and_process()
    
    def _on_toggle_mode(self):
        """Handle Win+Ctrl+Shift toggle"""
        if self.is_processing:
            print(f"{Fore.YELLOW}⏳ Already processing, please wait...{Style.RESET_ALL}")
            return
            
        if self.toggle_mode_active:
            # Stop recording
            print(f"{Fore.BLUE}🔄 Toggle mode: Stopping...{Style.RESET_ALL}")
            self.toggle_mode_active = False
            self.stop_recording_and_process()
        else:
            # Start recording
            print(f"{Fore.BLUE}🔄 Toggle mode: Starting...{Style.RESET_ALL}")
            self.toggle_mode_active = True
            self.start_recording()

    def run(self):
        """Main application loop"""
        # No AI test needed - already done in provider selection
        
        print(f"{Fore.YELLOW}⏳ Initializing GUI...{Style.RESET_ALL}")
        
        # Create GUI (must be in main thread)
        self.gui = WidgetGUI(
            on_cancel_callback=self.on_cancel,
            on_stop_callback=self.on_stop
        )
        
        # Hide GUI initially (will show on hotkey press)
        self.gui.hide()
        print(f"{Fore.GREEN}✓ GUI ready (hidden){Style.RESET_ALL}")
        
        # Start visualizer update thread
        visualizer_thread = threading.Thread(target=self._update_visualizer_loop, daemon=True)
        visualizer_thread.start()
        
        # Setup global hotkeys
        self._setup_hotkeys()
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*70}")
        print(f"{Fore.GREEN}{Style.BRIGHT}{'✓ WriteForMe is ready!':^70}")
        print(f"{Fore.GREEN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  🎤 Press Win+Shift (hold) for quick dictation{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  🔄 Press Win+Ctrl+Shift (toggle) for longer sessions{Style.RESET_ALL}")
        if self.use_ai_refinement:
            print(f"{Fore.CYAN}  💻 Using: {self.ai_manager.get_provider_name()}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}  ✏️  Mode: Raw transcription (no AI){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  ⚠ Close this window to exit{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")
        
        # Start GUI event loop (keeps app running)
        try:
            self.gui.start()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print(f"\n{Fore.YELLOW}🧹 Cleaning up...{Style.RESET_ALL}")
        
        # Stop hotkey listener
        if self.hotkey_listener:
            try:
                self.hotkey_listener.stop()
                print(f"{Fore.GREEN}✓ Hotkeys unregistered{Style.RESET_ALL}")
            except:
                pass
        
        self.audio_recorder.cleanup()
        if self.gui:
            self.gui.destroy()
        print(f"{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")


def main(silent_mode=False):
    """Entry point"""
    app = WisprFlowLocal(silent_mode=silent_mode)
    app.run()


if __name__ == "__main__":
    main(silent_mode=False)
