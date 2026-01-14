"""
Glass Card Component - Reusable frosted glass card with hover effects
"""
import customtkinter as ctk
from assets.styles import *


class GlassCard(ctk.CTkFrame):
    """Beautiful glassmorphic card with smooth hover animations"""
    
    def __init__(self, parent, **kwargs):
        # Extract custom parameters
        self.hover_enabled = kwargs.pop("hover_enabled", True)
        self.click_enabled = kwargs.pop("click_enabled", False)
        self.on_click = kwargs.pop("on_click", None)
        
        # Glass styling
        super().__init__(
            parent,
            fg_color=BG_GLASS,
            border_color=BORDER_GLASS,
            border_width=1,
            corner_radius=RADIUS_LG,
            **kwargs
        )
        
        # State tracking
        self.is_hovered = False
        
        # Bind hover events if enabled
        if self.hover_enabled:
            self.bind("<Enter>", self._on_enter)
            self.bind("<Leave>", self._on_leave)
        
        # Bind click events if enabled
        if self.click_enabled and self.on_click:
            self.bind("<Button-1>", lambda e: self.on_click())
            self.configure(cursor="hand2")
    
    def _on_enter(self, event):
        """Hover effect - lighten and glow"""
        self.is_hovered = True
        self.configure(
            fg_color=BG_GLASS_HOVER,
            border_color=BORDER_HOVER
        )
    
    def _on_leave(self, event):
        """Remove hover effect"""
        self.is_hovered = False
        self.configure(
            fg_color=BG_GLASS,
            border_color=BORDER_GLASS
        )
    
    def set_active(self, active=True):
        """Set card to active state (for selection)"""
        if active:
            self.configure(
                fg_color=BG_GLASS_ACTIVE,
                border_color=BORDER_GLOW
            )
        else:
            self.configure(
                fg_color=BG_GLASS,
                border_color=BORDER_GLASS
            )


class TranscriptionCard(GlassCard):
    """Specialized card for displaying transcription history"""
    
    def __init__(self, parent, data, on_reinject=None, on_delete=None, **kwargs):
        super().__init__(parent, hover_enabled=True, **kwargs)
        
        self.data = data
        self.on_reinject = on_reinject
        self.on_delete = on_delete
        
        self._build_ui()
    
    def _build_ui(self):
        """Build transcription card layout"""
        # Main container with padding
        self.configure(width=700, height=140)
        self.grid_propagate(False)
        
        # Header section (timestamp + mode)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=PADDING_MD, pady=(PADDING_MD, PADDING_XS))
        
        # Timestamp
        timestamp = self.data.get("timestamp", "")[:19].replace("T", " ")
        timestamp_label = ctk.CTkLabel(
            header_frame,
            text=timestamp,
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_TERTIARY
        )
        timestamp_label.pack(side="left")
        
        # Mode badge
        mode = self.data.get("mode", "unknown")
        mode_badge = ctk.CTkLabel(
            header_frame,
            text=mode.replace("_", " ").title(),
            font=(FONT_FAMILY, FONT_SIZE_SM, FONT_WEIGHT_MEDIUM),
            text_color=ACCENT_PRIMARY,
            fg_color=BG_DARKER,
            corner_radius=RADIUS_SM,
            padx=PADDING_SM,
            pady=4
        )
        mode_badge.pack(side="left", padx=PADDING_SM)
        
        # Paste success indicator
        if self.data.get("paste_success"):
            success_label = ctk.CTkLabel(
                header_frame,
                text="✓ Pasted",
                font=(FONT_FAMILY, FONT_SIZE_SM),
                text_color=ACCENT_SUCCESS
            )
            success_label.pack(side="left", padx=PADDING_XS)
        
        # Text preview section
        text_frame = ctk.CTkFrame(self, fg_color="transparent")
        text_frame.grid(row=1, column=0, sticky="ew", padx=PADDING_MD, pady=PADDING_XS)
        
        # Refined text (main content)
        refined_text = self.data.get("refined_text", "")
        preview = refined_text[:120] + ("..." if len(refined_text) > 120 else "")
        
        text_label = ctk.CTkLabel(
            text_frame,
            text=preview,
            font=(FONT_FAMILY, FONT_SIZE_MD),
            text_color=TEXT_PRIMARY,
            anchor="w",
            justify="left",
            wraplength=600
        )
        text_label.pack(fill="x")
        
        # Action buttons section
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="e", padx=PADDING_MD, pady=(PADDING_XS, PADDING_MD))
        
        # Re-inject button
        if self.on_reinject:
            reinject_btn = ctk.CTkButton(
                actions_frame,
                text="⟲ Re-inject",
                font=(FONT_FAMILY, FONT_SIZE_SM),
                width=100,
                height=30,
                corner_radius=RADIUS_SM,
                fg_color=ACCENT_PRIMARY,
                hover_color=ACCENT_PRIMARY_GLOW,
                command=lambda: self.on_reinject(self.data)
            )
            reinject_btn.pack(side="right", padx=PADDING_XS)
        
        # Delete button
        if self.on_delete:
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="🗑",
                font=(FONT_FAMILY, FONT_SIZE_SM),
                width=30,
                height=30,
                corner_radius=RADIUS_SM,
                fg_color=BG_GLASS,
                hover_color=ACCENT_DANGER,
                border_color=BORDER_GLASS,
                border_width=1,
                command=lambda: self.on_delete(self.data)
            )
            delete_btn.pack(side="right", padx=PADDING_XS)
        
        # Word count
        word_count = len(refined_text.split())
        count_label = ctk.CTkLabel(
            actions_frame,
            text=f"{word_count} words",
            font=(FONT_FAMILY, FONT_SIZE_SM),
            text_color=TEXT_TERTIARY
        )
        count_label.pack(side="right", padx=PADDING_MD)
