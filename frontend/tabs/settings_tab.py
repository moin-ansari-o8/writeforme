"""
Settings Tab - Configure AI providers, modes, and preferences
"""
import customtkinter as ctk
from components.glass_card import GlassCard
from components.glass_button import GlassButton, ToggleButton
from components.glass_input import GlassDropdown, GlassEntry
from assets.styles import *


class SettingsTab(ctk.CTkFrame):
    """Settings tab for configuring application preferences"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self._build_ui()
    
    def _build_ui(self):
        """Build settings tab layout"""
        # Scrollable container
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=BG_GLASS,
            scrollbar_button_hover_color=BG_GLASS_HOVER
        )
        scroll.pack(fill="both", expand=True, padx=PADDING_LG, pady=PADDING_LG)
        
        # Title
        title_label = ctk.CTkLabel(
            scroll,
            text="Settings",
            font=(FONT_FAMILY, FONT_SIZE_3XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title_label.pack(anchor="w", pady=(0, PADDING_LG))
        
        # AI Provider Section
        self._build_ai_provider_section(scroll)
        
        # Writing Mode Section
        self._build_writing_mode_section(scroll)
        
        # Hotkeys Section
        self._build_hotkeys_section(scroll)
        
        # Audio Settings Section
        self._build_audio_section(scroll)
        
        # Appearance Section
        self._build_appearance_section(scroll)
        
        # Save button
        save_btn = GlassButton(
            scroll,
            text="💾 Save Settings",
            variant="primary",
            width=200,
            command=self._save_settings
        )
        save_btn.pack(pady=PADDING_XL)
    
    def _build_ai_provider_section(self, parent):
        """AI Provider selection section"""
        section = GlassCard(parent, hover_enabled=False)
        section.pack(fill="x", pady=(0, PADDING_MD))
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="🤖 AI Provider",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=PADDING_LG, pady=(PADDING_LG, PADDING_SM))
        
        # Description
        desc = ctk.CTkLabel(
            section,
            text="Select which AI service to use for text refinement",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_SECONDARY,
            anchor="w"
        )
        desc.pack(anchor="w", padx=PADDING_LG, pady=(0, PADDING_MD))
        
        # Provider dropdown
        provider_frame = ctk.CTkFrame(section, fg_color="transparent")
        provider_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_MD))
        
        provider_label = ctk.CTkLabel(
            provider_frame,
            text="Provider:",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_PRIMARY,
            width=120,
            anchor="w"
        )
        provider_label.pack(side="left", padx=(0, PADDING_MD))
        
        self.provider_dropdown = GlassDropdown(
            provider_frame,
            values=["Cohere (Online)", "Gemini (Online)", "Groq (Online)", "Ollama (Local)"],
            default_value="Cohere (Online)",
            on_change=self._on_provider_change
        )
        self.provider_dropdown.pack(side="left", fill="x", expand=True)
        
        # Status indicator
        self.provider_status = ctk.CTkLabel(
            provider_frame,
            text="✓ Available",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=ACCENT_SUCCESS
        )
        self.provider_status.pack(side="left", padx=PADDING_MD)
        
        # Enable AI refinement toggle
        toggle_frame = ctk.CTkFrame(section, fg_color="transparent")
        toggle_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_LG))
        
        toggle_label = ctk.CTkLabel(
            toggle_frame,
            text="Enable AI Refinement:",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_PRIMARY,
            width=180,
            anchor="w"
        )
        toggle_label.pack(side="left", padx=(0, PADDING_MD))
        
        self.ai_toggle = ToggleButton(
            toggle_frame,
            text_on="✓ Enabled",
            text_off="✕ Disabled",
            default_state=True,
            width=120
        )
        self.ai_toggle.pack(side="left")
    
    def _build_writing_mode_section(self, parent):
        """Writing mode selection section"""
        section = GlassCard(parent, hover_enabled=False)
        section.pack(fill="x", pady=(0, PADDING_MD))
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="✍️ Writing Mode",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=PADDING_LG, pady=(PADDING_LG, PADDING_SM))
        
        # Description
        desc = ctk.CTkLabel(
            section,
            text="Choose how your dictation should be processed",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_SECONDARY,
            anchor="w"
        )
        desc.pack(anchor="w", padx=PADDING_LG, pady=(0, PADDING_MD))
        
        # Mode dropdown
        mode_frame = ctk.CTkFrame(section, fg_color="transparent")
        mode_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_MD))
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="Default Mode:",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_PRIMARY,
            width=120,
            anchor="w"
        )
        mode_label.pack(side="left", padx=(0, PADDING_MD))
        
        self.mode_dropdown = GlassDropdown(
            mode_frame,
            values=["Vibe Coder", "Casual Chatter"],
            default_value="Vibe Coder",
            on_change=self._on_mode_change
        )
        self.mode_dropdown.pack(side="left", fill="x", expand=True)
        
        # Mode description
        self.mode_desc = ctk.CTkLabel(
            section,
            text="Code-specialized mode with aggressive cleanup and symbol conversion",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_TERTIARY,
            anchor="w",
            wraplength=600,
            justify="left"
        )
        self.mode_desc.pack(anchor="w", padx=PADDING_LG, pady=(0, PADDING_LG))
    
    def _build_hotkeys_section(self, parent):
        """Hotkeys configuration section"""
        section = GlassCard(parent, hover_enabled=False)
        section.pack(fill="x", pady=(0, PADDING_MD))
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="⌨️ Hotkeys",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=PADDING_LG, pady=(PADDING_LG, PADDING_SM))
        
        # Description
        desc = ctk.CTkLabel(
            section,
            text="Global keyboard shortcuts (customization coming soon)",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_SECONDARY,
            anchor="w"
        )
        desc.pack(anchor="w", padx=PADDING_LG, pady=(0, PADDING_MD))
        
        # Hotkey displays
        hotkeys = [
            ("Push-to-Talk", "Win + Shift (Hold)", "Press and hold to record, release to process"),
            ("Toggle Mode", "Win + Ctrl + Shift", "Press once to start, press again to stop"),
            ("Open Dashboard", "Win + D (Planned)", "Show/hide this dashboard window")
        ]
        
        for name, keys, description in hotkeys:
            hk_frame = ctk.CTkFrame(section, fg_color="transparent")
            hk_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_SM))
            
            name_label = ctk.CTkLabel(
                hk_frame,
                text=name,
                font=(FONT_FAMILY, FONT_SIZE_MD),
                text_color=TEXT_PRIMARY,
                width=140,
                anchor="w"
            )
            name_label.pack(side="left", padx=(0, PADDING_SM))
            
            keys_badge = ctk.CTkLabel(
                hk_frame,
                text=keys,
                font=(FONT_FAMILY_MONO, FONT_SIZE_SM, FONT_WEIGHT_MEDIUM),
                text_color=ACCENT_PRIMARY,
                fg_color=BG_DARKER,
                corner_radius=RADIUS_SM,
                padx=PADDING_MD,
                pady=6,
                width=200
            )
            keys_badge.pack(side="left", padx=(0, PADDING_SM))
            
            desc_label = ctk.CTkLabel(
                hk_frame,
                text=description,
                font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=TEXT_TERTIARY,
                anchor="w"
            )
            desc_label.pack(side="left", fill="x", expand=True)
        
        # Spacer
        ctk.CTkLabel(section, text="").pack(pady=PADDING_SM)
    
    def _build_audio_section(self, parent):
        """Audio device settings section"""
        section = GlassCard(parent, hover_enabled=False)
        section.pack(fill="x", pady=(0, PADDING_MD))
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="🎤 Audio Settings",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=PADDING_LG, pady=(PADDING_LG, PADDING_SM))
        
        # Microphone selection
        mic_frame = ctk.CTkFrame(section, fg_color="transparent")
        mic_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_MD))
        
        mic_label = ctk.CTkLabel(
            mic_frame,
            text="Microphone:",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_PRIMARY,
            width=120,
            anchor="w"
        )
        mic_label.pack(side="left", padx=(0, PADDING_MD))
        
        self.mic_dropdown = GlassDropdown(
            mic_frame,
            values=["Default Microphone", "Built-in Microphone", "USB Microphone"],
            default_value="Default Microphone"
        )
        self.mic_dropdown.pack(side="left", fill="x", expand=True)
        
        # VAD sensitivity
        vad_frame = ctk.CTkFrame(section, fg_color="transparent")
        vad_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_LG))
        
        vad_label = ctk.CTkLabel(
            vad_frame,
            text="Voice Detection:",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_PRIMARY,
            width=120,
            anchor="w"
        )
        vad_label.pack(side="left", padx=(0, PADDING_MD))
        
        self.vad_dropdown = GlassDropdown(
            vad_frame,
            values=["Very Aggressive", "Aggressive", "Normal", "Relaxed"],
            default_value="Very Aggressive"
        )
        self.vad_dropdown.pack(side="left", fill="x", expand=True)
    
    def _build_appearance_section(self, parent):
        """Appearance settings section"""
        section = GlassCard(parent, hover_enabled=False)
        section.pack(fill="x", pady=(0, PADDING_MD))
        
        # Section title
        title = ctk.CTkLabel(
            section,
            text="🎨 Appearance",
            font=(FONT_FAMILY, FONT_SIZE_XL, FONT_WEIGHT_BOLD),
            text_color=TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=PADDING_LG, pady=(PADDING_LG, PADDING_SM))
        
        # Show visualizer toggle
        toggle_frame = ctk.CTkFrame(section, fg_color="transparent")
        toggle_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_MD))
        
        viz_label = ctk.CTkLabel(
            toggle_frame,
            text="Show Capsule Visualizer:",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_PRIMARY,
            width=180,
            anchor="w"
        )
        viz_label.pack(side="left", padx=(0, PADDING_MD))
        
        self.viz_toggle = ToggleButton(
            toggle_frame,
            text_on="✓ Enabled",
            text_off="✕ Disabled",
            default_state=True,
            width=120
        )
        self.viz_toggle.pack(side="left")
        
        # System tray toggle
        tray_frame = ctk.CTkFrame(section, fg_color="transparent")
        tray_frame.pack(fill="x", padx=PADDING_LG, pady=(0, PADDING_LG))
        
        tray_label = ctk.CTkLabel(
            tray_frame,
            text="Run in System Tray:",
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_PRIMARY,
            width=180,
            anchor="w"
        )
        tray_label.pack(side="left", padx=(0, PADDING_MD))
        
        self.tray_toggle = ToggleButton(
            tray_frame,
            text_on="✓ Enabled",
            text_off="✕ Disabled",
            default_state=False,
            width=120
        )
        self.tray_toggle.pack(side="left")
    
    def _on_provider_change(self, value):
        """Handle AI provider selection change"""
        print(f"[Settings] Provider changed to: {value}")
        # TODO: Check provider availability and update status
        self.provider_status.configure(text="✓ Available", text_color=ACCENT_SUCCESS)
    
    def _on_mode_change(self, value):
        """Handle writing mode change"""
        print(f"[Settings] Mode changed to: {value}")
        
        # Update description based on mode
        descriptions = {
            "Vibe Coder": "Code-specialized mode with aggressive cleanup and symbol conversion",
            "Casual Chatter": "Minimal refinement - removes filler words while preserving conversational tone"
        }
        self.mode_desc.configure(text=descriptions.get(value, ""))
    
    def _save_settings(self):
        """Save all settings"""
        print("[Settings] Saving settings...")
        
        settings = {
            "ai_provider": self.provider_dropdown.get(),
            "ai_enabled": self.ai_toggle.is_on,
            "writing_mode": self.mode_dropdown.get(),
            "microphone": self.mic_dropdown.get(),
            "vad_mode": self.vad_dropdown.get(),
            "show_visualizer": self.viz_toggle.is_on,
            "system_tray": self.tray_toggle.is_on
        }
        
        print(f"[Settings] New settings: {settings}")
        
        # TODO: Save to settings.json or config file
        # TODO: Apply settings to running application
        
        # Show feedback
        print("[Settings] Settings saved successfully!")
