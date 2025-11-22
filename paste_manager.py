"""
Clipboard and auto-paste manager
"""
import pyperclip
import pyautogui
import time


class PasteManager:
    def __init__(self):
        # Small delay for safety
        pyautogui.PAUSE = 0.1
        
    def paste_text(self, text):
        """
        Copy text to clipboard and paste it
        
        Args:
            text: Text to paste
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not text or text.strip() == "":
            print("[PasteManager] No text to paste")
            return False
        
        try:
            # Save current clipboard
            original_clipboard = pyperclip.paste()
            
            # Copy new text to clipboard
            pyperclip.copy(text)
            print(f"[PasteManager] Copied to clipboard: {text[:50]}...")
            
            # Small delay to ensure clipboard is updated
            time.sleep(0.1)
            
            # Simulate Ctrl+V to paste
            pyautogui.hotkey('ctrl', 'v')
            print("[PasteManager] Pasted text")
            
            # Optional: Restore original clipboard after a delay
            # Commented out to keep the refined text in clipboard
            # time.sleep(0.5)
            # pyperclip.copy(original_clipboard)
            
            return True
            
        except Exception as e:
            print(f"[PasteManager] Error pasting text: {e}")
            return False
    
    def copy_to_clipboard(self, text):
        """
        Copy text to clipboard without pasting
        
        Args:
            text: Text to copy
        """
        try:
            pyperclip.copy(text)
            print(f"[PasteManager] Copied to clipboard: {text[:50]}...")
            return True
        except Exception as e:
            print(f"[PasteManager] Error copying to clipboard: {e}")
            return False
