"""
Glass Input Component - Acrylic search bars and input fields
"""
import customtkinter as ctk
from assets.styles import *


class GlassEntry(ctk.CTkEntry):
    """Glassmorphic text input with smooth focus effects"""
    
    def __init__(self, parent, placeholder="", **kwargs):
        super().__init__(
            parent,
            placeholder_text=placeholder,
            fg_color=BG_GLASS,
            border_color=BORDER_GLASS,
            border_width=1,
            corner_radius=RADIUS_SM,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_TERTIARY,
            font=(FONT_FAMILY, FONT_SIZE_MD),
            height=INPUT_HEIGHT,
            **kwargs
        )
        
        # Focus effects
        self.bind("<FocusIn>", self._on_focus)
        self.bind("<FocusOut>", self._on_blur)
    
    def _on_focus(self, event):
        """Highlight border on focus"""
        self.configure(border_color=BORDER_GLOW)
    
    def _on_blur(self, event):
        """Reset border on blur"""
        self.configure(border_color=BORDER_GLASS)


class SearchBar(ctk.CTkFrame):
    """Beautiful search bar with icon and clear button"""
    
    def __init__(self, parent, placeholder="Search...", on_search=None, **kwargs):
        super().__init__(
            parent,
            fg_color=BG_GLASS,
            border_color=BORDER_GLASS,
            border_width=1,
            corner_radius=RADIUS_MD,
            **kwargs
        )
        
        self.on_search = on_search
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        
        # Search icon
        icon_label = ctk.CTkLabel(
            self,
            text="🔍",
            font=(FONT_FAMILY, FONT_SIZE_LG),
            text_color=TEXT_TERTIARY
        )
        icon_label.grid(row=0, column=0, padx=(PADDING_MD, PADDING_XS), pady=PADDING_XS)
        
        # Search input
        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            fg_color="transparent",
            border_width=0,
            text_color=TEXT_PRIMARY,
            placeholder_text_color=TEXT_TERTIARY,
            font=(FONT_FAMILY, FONT_SIZE_MD),
            height=INPUT_HEIGHT
        )
        self.entry.grid(row=0, column=1, sticky="ew", pady=PADDING_XS)
        
        # Bind search event
        self.entry.bind("<KeyRelease>", self._on_key_release)
        
        # Clear button (hidden by default)
        self.clear_btn = ctk.CTkButton(
            self,
            text="✕",
            width=30,
            height=30,
            corner_radius=RADIUS_SM,
            fg_color="transparent",
            hover_color=BG_GLASS_HOVER,
            text_color=TEXT_TERTIARY,
            font=(FONT_FAMILY, FONT_SIZE_MD),
            command=self._clear_search
        )
        self.clear_btn.grid(row=0, column=2, padx=(PADDING_XS, PADDING_MD), pady=PADDING_XS)
        self.clear_btn.grid_remove()  # Hide initially
        
        # Focus border effect
        self.entry.bind("<FocusIn>", lambda e: self.configure(border_color=BORDER_GLOW))
        self.entry.bind("<FocusOut>", lambda e: self.configure(border_color=BORDER_GLASS))
    
    def _on_key_release(self, event):
        """Handle search input changes"""
        query = self.entry.get()
        
        # Show/hide clear button
        if query:
            self.clear_btn.grid()
        else:
            self.clear_btn.grid_remove()
        
        # Trigger search callback
        if self.on_search:
            self.on_search(query)
    
    def _clear_search(self):
        """Clear search input"""
        self.entry.delete(0, "end")
        self.clear_btn.grid_remove()
        
        if self.on_search:
            self.on_search("")
    
    def get(self):
        """Get current search query"""
        return self.entry.get()
    
    def focus(self):
        """Focus the search input"""
        self.entry.focus()


class GlassDropdown(ctk.CTkOptionMenu):
    """Glassmorphic dropdown menu"""
    
    def __init__(self, parent, values, default_value=None, on_change=None, **kwargs):
        super().__init__(
            parent,
            values=values,
            fg_color=BG_GLASS,
            button_color=BG_GLASS,
            button_hover_color=BG_GLASS_HOVER,
            dropdown_fg_color=BG_GLASS,
            dropdown_hover_color=BG_GLASS_HOVER,
            text_color=TEXT_PRIMARY,
            dropdown_text_color=TEXT_PRIMARY,
            font=(FONT_FAMILY, FONT_SIZE_MD),
            dropdown_font=(FONT_FAMILY, FONT_SIZE_MD),
            corner_radius=RADIUS_SM,
            height=INPUT_HEIGHT,
            command=on_change,
            **kwargs
        )
        
        if default_value:
            self.set(default_value)


class GlassTextBox(ctk.CTkTextbox):
    """Glassmorphic multi-line text area"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=BG_GLASS,
            border_color=BORDER_GLASS,
            border_width=1,
            corner_radius=RADIUS_SM,
            text_color=TEXT_PRIMARY,
            font=(FONT_FAMILY, FONT_SIZE_MD),
            **kwargs
        )
        
        # Focus effects
        self.bind("<FocusIn>", self._on_focus)
        self.bind("<FocusOut>", self._on_blur)
    
    def _on_focus(self, event):
        """Highlight border on focus"""
        self.configure(border_color=BORDER_GLOW)
    
    def _on_blur(self, event):
        """Reset border on blur"""
        self.configure(border_color=BORDER_GLASS)
