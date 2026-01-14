"""
Wispr Flow Local - Main Application
A local Python clone of Wispr Flow using speech recognition and AI
Now with global hotkey support and multiple AI providers

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
    def __init__(self):
        # Initialize AI Provider Manager with selection UI
        self.ai_manager = AIProviderManager()
        if not self.ai_manager.select_provider():
            print(f"{Fore.RED}Failed to initialize AI provider!{Style.RESET_ALL}")
            raise Exception("No AI provider available")
        
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"{Fore.GREEN}✓ Using: {self.ai_manager.get_provider_name()}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")
        
        # Initialize other components
        print(f"{Fore.YELLOW}⏳ Initializing components...{Style.RESET_ALL}")
        self.audio_recorder = AudioRecorder()
        self.speech_to_text = SpeechToText()
        self.paste_manager = PasteManager()
        self.data_storage = DataStorage()
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
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}▶ Starting recording...{Style.RESET_ALL}")
        self.is_recording = True
        
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
        
        print(f"\n{Fore.YELLOW}⏹ Stopping recording - Processing...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        
        # Switch UI to processing mode immediately
        if self.gui:
            self.gui.show_processing()
        
        # Stop recording and get audio data
        audio_data = self.audio_recorder.stop_recording()
        
        if audio_data is None or len(audio_data) == 0:
            print(f"{Fore.RED}✗ No audio recorded{Style.RESET_ALL}")
            self.is_processing = False
            if self.gui:
                self.gui.hide()
            return
        
        # Process in separate thread to avoid blocking
        threading.Thread(target=self._process_audio, args=(audio_data,), daemon=True).start()
    
    def on_stop(self, mode="ai"):
        """Handle stop button press from GUI"""
        self.stop_recording_and_process()
    
    def _process_audio(self, audio_data):
        """Process audio in background thread"""
        try:
            # Get current mode
            current_mode = "default"
            if self.gui:
                current_mode = self.gui.get_current_mode()
            
            # Step 1: Speech to Text
            print(f"{Fore.CYAN}[1/4] 🎯 Transcribing speech...{Style.RESET_ALL}")
            transcribed_text = self.speech_to_text.transcribe_audio(audio_data)
            
            if not transcribed_text or transcribed_text.strip() == "":
                print(f"{Fore.RED}✗ No speech detected{Style.RESET_ALL}")
                self.is_processing = False
                if self.gui:
                    self.gui.hide()
                return
            
            print(f"{Fore.GREEN}✓ Transcribed: {Fore.WHITE}{transcribed_text}{Style.RESET_ALL}")
            
            # Step 2: AI Refinement
            print(f"{Fore.CYAN}[2/4] ✨ Refining with {self.ai_manager.get_provider_name()}...{Style.RESET_ALL}")
            
            prompt_template = config.WRITING_MODES.get(current_mode, config.WRITING_MODES["default"])["prompt"]
            refined_text = self.ai_manager.refine_text(transcribed_text, prompt_template)
            
            print(f"{Fore.GREEN}✓ Refined: {Fore.WHITE}{refined_text}{Style.RESET_ALL}")
            
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
            
            print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
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
                time.sleep(0.03)  # ~33 FPS for smoother response
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
        print(f"{Fore.CYAN}  💻 Using: {self.ai_manager.get_provider_name()}{Style.RESET_ALL}")
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


def main():
    """Entry point"""
    app = WisprFlowLocal()
    app.run()


if __name__ == "__main__":
    main()
