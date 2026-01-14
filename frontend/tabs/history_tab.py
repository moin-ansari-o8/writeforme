"""
History Tab - View all transcriptions with search and management
"""
import customtkinter as ctk
from components.glass_card import TranscriptionCard
from components.glass_input import SearchBar
from components.glass_button import GlassButton
from assets.styles import *
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


class HistoryTab(ctk.CTkFrame):
    """History tab showing all transcription records"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        # Data
        self.all_transcriptions = []
        self.filtered_transcriptions = []
        
        self._build_ui()
        self._load_mock_data()  # Use mock data for testing
    
    def _build_ui(self):
        """Build history tab layout"""
        # Header section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=PADDING_LG, pady=(PADDING_LG, PADDING_MD))
        
        # Title
        title_label = ctk.CTkLabel(
            header,
            text="Transcription History",
            font=(FONT_FAMILY, FONT_SIZE_3XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(side="left")
        
        # Stats badge
        self.stats_label = ctk.CTkLabel(
            header,
            text="0 entries",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_SECONDARY,
            fg_color=BG_GLASS,
            corner_radius=RADIUS_SM,
            padx=PADDING_MD,
            pady=PADDING_XS
        )
        self.stats_label.pack(side="left", padx=PADDING_MD)
        
        # Export button
        export_btn = GlassButton(
            header,
            text="📤 Export",
            variant="secondary",
            width=120,
            command=self._export_history
        )
        export_btn.pack(side="right", padx=PADDING_XS)
        
        # Clear all button
        clear_btn = GlassButton(
            header,
            text="🗑 Clear All",
            variant="danger",
            width=120,
            command=self._clear_history
        )
        clear_btn.pack(side="right", padx=PADDING_XS)
        
        # Search bar
        self.search_bar = SearchBar(
            self,
            placeholder="Search transcriptions...",
            on_search=self._on_search
        )
        self.search_bar.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_MD))
        
        # Scrollable content area
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=BG_GLASS,
            scrollbar_button_hover_color=BG_GLASS_HOVER
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=PADDING_LG, pady=(0, PADDING_LG))
        
        # Empty state message
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="No transcriptions yet\nStart dictating with Win+Shift!",
            font=(FONT_FAMILY, FONT_SIZE_LG),
            text_color=TEXT_TERTIARY,
            justify="center"
        )
        self.empty_label.pack(pady=100)
    
    def _load_mock_data(self):
        """Load mock transcription data for testing"""
        from datetime import datetime, timedelta
        
        mock_data = [
            {
                "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "mode": "vibe_coder",
                "raw_text": "hello hello so I'm testing the deep-sea coder model",
                "refined_text": "Hello, I'm testing the deepseek coder model and checking if the transcription works properly with voice commands.",
                "paste_success": True,
                "text_length": 120
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
                "mode": "casual_chatter",
                "raw_text": "um so like I was thinking about the new feature",
                "refined_text": "So I was thinking about the new feature we discussed earlier. It should be pretty straightforward to implement.",
                "paste_success": True,
                "text_length": 115
            },
            {
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "mode": "vibe_coder",
                "raw_text": "main road 55 web underscore filter function",
                "refined_text": "Open main.py and check the web_filter function to see if the energy_threshold was properly adjusted.",
                "paste_success": True,
                "text_length": 95
            },
            {
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "mode": "vibe_coder",
                "raw_text": "let's see if to work or not",
                "refined_text": "Let's see if it works or not. The new configuration should improve accuracy significantly.",
                "paste_success": False,
                "text_length": 89
            },
            {
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
                "mode": "casual_chatter",
                "raw_text": "I guess we should start working on the dashboard",
                "refined_text": "We should start working on the dashboard soon. The glassmorphism design looks amazing!",
                "paste_success": True,
                "text_length": 95
            }
        ]
        
        self.all_transcriptions = mock_data
        self.filtered_transcriptions = mock_data.copy()
        self._render_transcriptions()
    
    def _render_transcriptions(self):
        """Render transcription cards"""
        # Clear existing cards
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        # Update stats
        total = len(self.all_transcriptions)
        filtered = len(self.filtered_transcriptions)
        stats_text = f"{filtered} of {total} entries" if filtered < total else f"{total} entries"
        self.stats_label.configure(text=stats_text)
        
        # Show empty state if no data
        if not self.filtered_transcriptions:
            self.empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="No matching transcriptions found",
                font=(FONT_FAMILY, FONT_SIZE_LG),
                text_color=TEXT_TERTIARY
            )
            self.empty_label.pack(pady=100)
            return
        
        # Render cards (newest first)
        for data in reversed(self.filtered_transcriptions):
            card = TranscriptionCard(
                self.scroll_frame,
                data=data,
                on_reinject=self._on_reinject,
                on_delete=self._on_delete
            )
            card.pack(fill="x", pady=PADDING_SM)
    
    def _on_search(self, query):
        """Filter transcriptions by search query"""
        if not query:
            self.filtered_transcriptions = self.all_transcriptions.copy()
        else:
            query_lower = query.lower()
            self.filtered_transcriptions = [
                t for t in self.all_transcriptions
                if query_lower in t.get("refined_text", "").lower()
                or query_lower in t.get("raw_text", "").lower()
                or query_lower in t.get("mode", "").lower()
            ]
        
        self._render_transcriptions()
    
    def _on_reinject(self, data):
        """Re-inject transcription text"""
        text = data.get("refined_text", "")
        print(f"[History] Re-injecting: {text[:50]}...")
        
        # TODO: Integrate with paste_manager.py
        # from paste_manager import paste_text
        # paste_text(text)
        
        # Show feedback (mock for now)
        self._show_notification("Text re-injected!")
    
    def _on_delete(self, data):
        """Delete transcription entry"""
        print(f"[History] Deleting entry: {data.get('timestamp')}")
        
        # Remove from lists
        if data in self.all_transcriptions:
            self.all_transcriptions.remove(data)
        if data in self.filtered_transcriptions:
            self.filtered_transcriptions.remove(data)
        
        # Re-render
        self._render_transcriptions()
        self._show_notification("Entry deleted")
    
    def _export_history(self):
        """Export history to text file"""
        print("[History] Exporting history...")
        
        # TODO: Integrate with data_storage.py export_to_text()
        self._show_notification("History exported!")
    
    def _clear_history(self):
        """Clear all history (with confirmation)"""
        # TODO: Add confirmation dialog
        print("[History] Clearing all history...")
        self.all_transcriptions = []
        self.filtered_transcriptions = []
        self._render_transcriptions()
        self._show_notification("History cleared")
    
    def _show_notification(self, message):
        """Show temporary notification (placeholder)"""
        # TODO: Add toast notification system
        print(f"[Notification] {message}")
    
    def refresh_data(self):
        """Refresh data from storage (for future integration)"""
        # TODO: Load from data_storage.py
        # from data_storage import DataStorage
        # storage = DataStorage()
        # self.all_transcriptions = storage.get_history()
        # self.filtered_transcriptions = self.all_transcriptions.copy()
        # self._render_transcriptions()
        pass
