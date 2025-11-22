"""
Data Storage Manager - Persistent storage for all transcriptions
Stores all processed voice transcriptions with metadata
"""
import json
import os
from datetime import datetime
import threading


class DataStorage:
    def __init__(self, storage_file="transcriptions_history.json"):
        """
        Initialize data storage manager
        
        Args:
            storage_file: Path to JSON storage file
        """
        self.storage_file = storage_file
        self.lock = threading.Lock()
        
        # Create storage file if it doesn't exist
        if not os.path.exists(self.storage_file):
            self._initialize_storage()
            print(f"[DataStorage] Created new storage file: {self.storage_file}")
        else:
            print(f"[DataStorage] Using existing storage file: {self.storage_file}")
    
    def _initialize_storage(self):
        """Create new storage file with empty structure"""
        initial_data = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "transcriptions": []
        }
        
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2, ensure_ascii=False)
    
    def save_transcription(self, mode, raw_text, refined_text, paste_success=False):
        """
        Save a new transcription entry
        
        Args:
            mode: Writing mode used (e.g., 'default', 'email_professional')
            raw_text: Original transcribed text
            refined_text: AI-refined text
            paste_success: Whether paste operation succeeded
            
        Returns:
            bool: True if saved successfully
        """
        try:
            with self.lock:
                # Read existing data
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Create new entry
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "mode": mode,
                    "raw_text": raw_text,
                    "refined_text": refined_text,
                    "paste_success": paste_success,
                    "text_length": len(refined_text)
                }
                
                # Append to transcriptions list
                data["transcriptions"].append(entry)
                
                # Write back to file
                with open(self.storage_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"[DataStorage] Saved transcription #{len(data['transcriptions'])} (paste_success={paste_success})")
                return True
                
        except Exception as e:
            print(f"[DataStorage] Error saving transcription: {e}")
            return False
    
    def get_history(self, limit=None):
        """
        Get transcription history
        
        Args:
            limit: Maximum number of entries to return (None for all)
            
        Returns:
            list: List of transcription entries
        """
        try:
            with self.lock:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                transcriptions = data.get("transcriptions", [])
                
                if limit:
                    return transcriptions[-limit:]
                return transcriptions
                
        except Exception as e:
            print(f"[DataStorage] Error reading history: {e}")
            return []
    
    def get_total_count(self):
        """Get total number of transcriptions stored"""
        try:
            with self.lock:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return len(data.get("transcriptions", []))
        except:
            return 0
    
    def export_to_text(self, output_path="transcriptions_export.txt"):
        """
        Export all refined text to a plain text file
        
        Args:
            output_path: Path to output text file
            
        Returns:
            bool: True if exported successfully
        """
        try:
            transcriptions = self.get_history()
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("TRANSCRIPTIONS EXPORT\n")
                f.write(f"Total entries: {len(transcriptions)}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, entry in enumerate(transcriptions, 1):
                    f.write(f"Entry #{i}\n")
                    f.write(f"Timestamp: {entry['timestamp']}\n")
                    f.write(f"Mode: {entry['mode']}\n")
                    f.write(f"Paste Success: {entry['paste_success']}\n")
                    f.write("-" * 60 + "\n")
                    f.write(f"{entry['refined_text']}\n")
                    f.write("\n" + "=" * 60 + "\n\n")
            
            print(f"[DataStorage] Exported {len(transcriptions)} entries to {output_path}")
            return True
            
        except Exception as e:
            print(f"[DataStorage] Error exporting to text: {e}")
            return False
    
    def clear_history(self):
        """Clear all transcription history (use with caution!)"""
        try:
            with self.lock:
                self._initialize_storage()
            print("[DataStorage] History cleared")
            return True
        except Exception as e:
            print(f"[DataStorage] Error clearing history: {e}")
            return False
