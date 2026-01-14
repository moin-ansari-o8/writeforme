"""
Glass Button Component - Beautiful buttons with glow effects
"""
import customtkinter as ctk
from assets.styles import *


class GlassButton(ctk.CTkButton):
    """Glassmorphic button with smooth animations"""
    
    def __init__(self, parent, variant="primary", icon=None, **kwargs):
        # Get style based on variant
        style = get_button_style(variant)
        
        # Apply glass styling
        super().__init__(
            parent,
            fg_color=style["fg_color"],
            hover_color=style["hover_color"],
            border_color=style.get("border_color", BORDER_GLASS),
            border_width=1,
            corner_radius=RADIUS_MD,
            text_color=style["text_color"],
            font=(FONT_FAMILY, FONT_SIZE_MD, FONT_WEIGHT_MEDIUM),
            height=BUTTON_HEIGHT,
            cursor="hand2",
            **kwargs
        )


class IconButton(ctk.CTkButton):
    """Small icon-only button for compact actions"""
    
    def __init__(self, parent, icon_text, tooltip=None, variant="secondary", **kwargs):
        style = get_button_style(variant)
        
        super().__init__(
            parent,
            text=icon_text,
            width=36,
            height=36,
            corner_radius=RADIUS_SM,
            fg_color=style["fg_color"],
            hover_color=style["hover_color"],
            border_color=style.get("border_color", BORDER_GLASS),
            border_width=1,
            text_color=style["text_color"],
            font=(FONT_FAMILY, FONT_SIZE_LG),
            cursor="hand2",
            **kwargs
        )
        
        # Tooltip support (placeholder - would need tkinter tooltip library)
        self.tooltip = tooltip


class ToggleButton(ctk.CTkButton):
    """Toggle button with on/off states"""
    
    def __init__(self, parent, text_on="ON", text_off="OFF", default_state=False, on_toggle=None, **kwargs):
        self.text_on = text_on
        self.text_off = text_off
        self.is_on = default_state
        self.on_toggle = on_toggle
        
        super().__init__(
            parent,
            text=self.text_on if self.is_on else self.text_off,
            corner_radius=RADIUS_MD,
            height=BUTTON_HEIGHT,
            font=(FONT_FAMILY, FONT_SIZE_MD, FONT_WEIGHT_MEDIUM),
            cursor="hand2",
            command=self._toggle,
            **kwargs
        )
        
        self._update_style()
    
    def _toggle(self):
        """Toggle state and update styling"""
        self.is_on = not self.is_on
        self.configure(text=self.text_on if self.is_on else self.text_off)
        self._update_style()
        
        if self.on_toggle:
            self.on_toggle(self.is_on)
    
    def _update_style(self):
        """Update button colors based on state"""
        if self.is_on:
            self.configure(
                fg_color=ACCENT_SUCCESS,
                hover_color="#059669",
                border_color=ACCENT_SUCCESS,
                text_color=TEXT_PRIMARY
            )
        else:
            self.configure(
                fg_color=BG_GLASS,
                hover_color=BG_GLASS_HOVER,
                border_color=BORDER_GLASS,
                text_color=TEXT_SECONDARY
            )
    
    def set_state(self, state):
        """Programmatically set toggle state"""
        if self.is_on != state:
            self._toggle()


class GlowButton(GlassButton):
    """Button with animated glow effect on hover"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, variant="primary", **kwargs)
        
        # Enhance with glow effect
        self.configure(
            border_width=2,
            border_color=BORDER_GLOW
        )
        
        # Bind for additional effects
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
    
    def _on_hover(self, event):
        """Intensify glow on hover"""
        self.configure(border_width=2)
    
    def _on_leave(self, event):
        """Reset glow"""
        self.configure(border_width=1)
