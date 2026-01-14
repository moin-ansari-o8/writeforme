"""
WriteForMe Dashboard - TRUE Glassmorphism UI with PyQt6
Real blur effects, frameless window, smooth animations
"""
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QPushButton, QScrollArea,
                              QFrame, QGraphicsBlurEffect, QGraphicsOpacityEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QPoint
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QBrush, QPen, QLinearGradient


class GlassWidget(QFrame):
    """Main dashboard window with glassmorphic design"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("WriteForMe - Dashboard")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Apply custom colors
        self.configure(fg_color=BG_DARK)
        
        # Track current tab
        self.current_tab = None
        self.tab_buttons = {}
        
        self._build_ui()
        
        # Show history tab by default
        self._switch_tab("history")
        
        # Center window on screen
        self._center_window()
    
    def _center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _build_ui(self):
        """Build main dashboard layout"""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=PADDING_LG, pady=PADDING_LG)
        
        # Left sidebar (navigation)
        self._build_sidebar(main_frame)
        
        # Right content area
        self._build_content_area(main_frame)
    
    def _build_sidebar(self, parent):
        """Build left sidebar with navigation"""
        sidebar = ctk.CTkFrame(
            parent,
            fg_color=BG_GLASS,
            border_color=BORDER_GLASS,
            border_width=1,
            corner_radius=RADIUS_LG,
            width=240
        )
        sidebar.pack(side="left", fill="y", padx=(0, PADDING_MD))
        sidebar.pack_propagate(False)
        
        # App header
        header_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        header_frame.pack(fill="x", padx=PADDING_LG, pady=(PADDING_LG, PADDING_XL))
        
        # App icon/logo (placeholder)
        logo_label = ctk.CTkLabel(
            header_frame,
            text="✨",
            font=(FONT_FAMILY, 32),
            text_color=ACCENT_PRIMARY
        )
        logo_label.pack(pady=(0, PADDING_XS))
        
        # App name
        app_name = ctk.CTkLabel(
            header_frame,
            text="WriteForMe",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        app_name.pack()
        
        # Version
        version_label = ctk.CTkLabel(
            header_frame,
            text="v1.0.0",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_TERTIARY
        )
        version_label.pack()
        
        # Navigation buttons
        nav_items = [
            ("history", "📜", "History", "View all transcriptions"),
            ("settings", "⚙️", "Settings", "Configure preferences"),
            ("stats", "📊", "Statistics", "Usage analytics")
        ]
        
        for tab_id, icon, label, tooltip in nav_items:
            btn = self._create_nav_button(sidebar, tab_id, icon, label)
            btn.pack(fill="x", padx=PADDING_MD, pady=(0, PADDING_XS))
            self.tab_buttons[tab_id] = btn
        
        # Spacer
        spacer = ctk.CTkFrame(sidebar, fg_color="transparent")
        spacer.pack(fill="both", expand=True)
        
        # Status section at bottom
        status_frame = ctk.CTkFrame(
            sidebar,
            fg_color=BG_DARKER,
            corner_radius=RADIUS_MD
        )
        status_frame.pack(fill="x", padx=PADDING_MD, pady=PADDING_MD)
        
        # Status indicator
        status_header = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_header.pack(fill="x", padx=PADDING_MD, pady=(PADDING_MD, PADDING_XS))
        
        status_dot = ctk.CTkFrame(
            status_header,
            fg_color=ACCENT_SUCCESS,
            corner_radius=RADIUS_FULL,
            width=8,
            height=8
        )
        status_dot.pack(side="left", padx=(0, PADDING_XS))
        
        status_label = ctk.CTkLabel(
            status_header,
            text="Capsule Active",
            font=(FONT_FAMILY, FONT_SIZE_SM, FONT_WEIGHT_MEDIUM),
            text_color=TEXT_PRIMARY
        )
        status_label.pack(side="left")
        
        # Hotkey hint
        hotkey_label = ctk.CTkLabel(
            status_frame,
            text="Win+Shift to record",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_TERTIARY
        )
        hotkey_label.pack(padx=PADDING_MD, pady=(0, PADDING_MD))
        
        # Footer buttons
        footer_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer_frame.pack(fill="x", padx=PADDING_MD, pady=(0, PADDING_MD))
        
        # About button
        about_btn = ctk.CTkButton(
            footer_frame,
            text="ℹ️ About",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            fg_color="transparent",
            hover_color=BG_GLASS_HOVER,
            text_color=TEXT_SECONDARY,
            height=32,
            corner_radius=RADIUS_SM,
            command=self._show_about
        )
        about_btn.pack(side="left", fill="x", expand=True, padx=(0, PADDING_XS))
        
        # Exit button
        exit_btn = ctk.CTkButton(
            footer_frame,
            text="✕",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            fg_color="transparent",
            hover_color=ACCENT_DANGER,
            text_color=TEXT_SECONDARY,
            width=32,
            height=32,
            corner_radius=RADIUS_SM,
            command=self._exit_app
        )
        exit_btn.pack(side="right")
    
    def _create_nav_button(self, parent, tab_id, icon, label):
        """Create a navigation button"""
        btn = ctk.CTkButton(
            parent,
            text=f"{icon}  {label}",
            font=(FONT_FAMILY, FONT_SIZE_MD, FONT_WEIGHT_MEDIUM),
            fg_color="transparent",
            hover_color=BG_GLASS_HOVER,
            text_color=TEXT_SECONDARY,
            anchor="w",
            height=44,
            corner_radius=RADIUS_MD,
            command=lambda: self._switch_tab(tab_id)
        )
        return btn
    
    def _build_content_area(self, parent):
        """Build main content area"""
        self.content_frame = ctk.CTkFrame(
            parent,
            fg_color=BG_GLASS,
            border_color=BORDER_GLASS,
            border_width=1,
            corner_radius=RADIUS_LG
        )
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        # Create tab instances (hidden initially)
        self.tabs = {
            "history": HistoryTab(self.content_frame),
            "settings": SettingsTab(self.content_frame),
            "stats": StatsTab(self.content_frame)
        }
    
    def _switch_tab(self, tab_id):
        """Switch to a different tab"""
        # Hide current tab
        if self.current_tab:
            self.tabs[self.current_tab].pack_forget()
            # Reset button style
            self.tab_buttons[self.current_tab].configure(
                fg_color="transparent",
                text_color=TEXT_SECONDARY
            )
        
        # Show new tab
        self.tabs[tab_id].pack(fill="both", expand=True)
        self.current_tab = tab_id
        
        # Highlight active button
        self.tab_buttons[tab_id].configure(
            fg_color=ACCENT_PRIMARY,
            text_color=TEXT_PRIMARY
        )
        
        # Refresh data if needed
        if tab_id == "history" and hasattr(self.tabs[tab_id], 'refresh_data'):
            self.tabs[tab_id].refresh_data()
        elif tab_id == "stats" and hasattr(self.tabs[tab_id], 'refresh_stats'):
            self.tabs[tab_id].refresh_stats()
    
    def _show_about(self):
        """Show about dialog"""
        # Create modal dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("About WriteForMe")
        dialog.geometry("500x400")
        dialog.resizable(False, False)
        dialog.configure(fg_color=BG_DARK)
        
        # Center dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 250
        y = self.winfo_y() + (self.winfo_height() // 2) - 200
        dialog.geometry(f"+{x}+{y}")
        
        # Content
        content = ctk.CTkFrame(
            dialog,
            fg_color=BG_GLASS,
            border_color=BORDER_GLASS,
            border_width=1,
            corner_radius=RADIUS_LG
        )
        content.pack(fill="both", expand=True, padx=PADDING_LG, pady=PADDING_LG)
        
        # Icon
        icon_label = ctk.CTkLabel(
            content,
            text="✨",
            font=(FONT_FAMILY, 64),
            text_color=ACCENT_PRIMARY
        )
        icon_label.pack(pady=(PADDING_XL, PADDING_MD))
        
        # Title
        title_label = ctk.CTkLabel(
            content,
            text="WriteForMe",
            font=(FONT_FAMILY, FONT_SIZE_3XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title_label.pack()
        
        # Version
        version_label = ctk.CTkLabel(
            content,
            text="Version 1.0.0",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_SECONDARY
        )
        version_label.pack(pady=PADDING_XS)
        
        # Description
        desc_label = ctk.CTkLabel(
            content,
            text="Local-first desktop dictation assistant\nwith AI-powered text refinement",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_SECONDARY,
            justify="center"
        )
        desc_label.pack(pady=PADDING_LG)
        
        # Features
        features = "✓ Voice transcription with real-time visualizer\n✓ AI refinement (Cohere, Gemini, Groq, Ollama)\n✓ Global hotkeys (Win+Shift, Win+Ctrl+Shift)\n✓ Beautiful glassmorphism UI"
        features_label = ctk.CTkLabel(
            content,
            text=features,
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_TERTIARY,
            justify="left"
        )
        features_label.pack(pady=PADDING_MD)
        
        # Close button
        close_btn = ctk.CTkButton(
            content,
            text="Close",
            font=(FONT_FAMILY, FONT_SIZE_MD, FONT_WEIGHT_MEDIUM),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_PRIMARY_GLOW,
            height=BUTTON_HEIGHT,
            corner_radius=RADIUS_MD,
            command=dialog.destroy
        )
        close_btn.pack(pady=(PADDING_LG, PADDING_XL))
        
        # Make modal
        dialog.transient(self)
        dialog.grab_set()
    
    def _exit_app(self):
        """Exit the application"""
        self.quit()
        self.destroy()


def main():
    """Main entry point"""
    print("🚀 Launching WriteForMe Dashboard...")
    print("📊 Glassmorphism UI with mock data")
    print("✨ Test the interface before integration\n")
    
    app = GlassDashboard()
    app.mainloop()


if __name__ == "__main__":
    main()
