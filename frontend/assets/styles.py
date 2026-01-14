"""
Glassmorphism Theme - Color Palette & Design System
Beautiful dark mode with acrylic effects
"""

# ==================== COLOR PALETTE ====================

# Background Colors
BG_DARK = "#0a0a0a"              # Deep black background
BG_DARKER = "#050505"            # Even darker for depth
BG_GLASS = "#1a1a1a"             # Glass panel base
BG_GLASS_HOVER = "#222222"       # Glass hover state
BG_GLASS_ACTIVE = "#2a2a2a"      # Glass active state

# Accent Colors
ACCENT_PRIMARY = "#6366f1"       # Indigo - primary actions
ACCENT_PRIMARY_GLOW = "#818cf8"  # Lighter indigo for glow
ACCENT_SECONDARY = "#8b5cf6"     # Purple - secondary actions
ACCENT_SUCCESS = "#10b981"       # Green - success states
ACCENT_DANGER = "#ef4444"        # Red - delete/danger
ACCENT_WARNING = "#f59e0b"       # Amber - warnings

# Text Colors
TEXT_PRIMARY = "#e0e0e0"         # Main text - bright
TEXT_SECONDARY = "#9ca3af"       # Secondary text - muted
TEXT_TERTIARY = "#6b7280"        # Tertiary text - subtle
TEXT_DISABLED = "#4b5563"        # Disabled text

# Border Colors
BORDER_GLASS = "#2d2d2d"         # Subtle glass border
BORDER_GLOW = "#6366f1"          # Accent border with glow
BORDER_HOVER = "#3d3d3d"         # Border on hover

# Special Effects
GLASS_OPACITY = 0.7              # Glass transparency (70%)
GLOW_INTENSITY = 0.4             # Glow effect intensity
SHADOW_LIGHT = "rgba(99, 102, 241, 0.1)"   # Subtle accent shadow
SHADOW_STRONG = "rgba(0, 0, 0, 0.3)"       # Strong depth shadow

# ==================== DIMENSIONS ====================

# Spacing
PADDING_XS = 8
PADDING_SM = 12
PADDING_MD = 16
PADDING_LG = 24
PADDING_XL = 32

# Border Radius
RADIUS_SM = 8
RADIUS_MD = 12
RADIUS_LG = 16
RADIUS_XL = 20
RADIUS_FULL = 999

# Sizes
BUTTON_HEIGHT = 40
INPUT_HEIGHT = 44
CARD_HEIGHT_SM = 80
CARD_HEIGHT_MD = 120

# ==================== FONTS ====================

FONT_FAMILY = "Segoe UI"         # Windows native font
FONT_FAMILY_MONO = "Consolas"    # Monospace for code

FONT_SIZE_XS = 11
FONT_SIZE_SM = 12
FONT_SIZE_MD = 14
FONT_SIZE_LG = 16
FONT_SIZE_XL = 20
FONT_SIZE_2XL = 24
FONT_SIZE_3XL = 32

FONT_WEIGHT_NORMAL = "normal"
FONT_WEIGHT_MEDIUM = "bold"      # CTk doesn't support medium, use bold
FONT_WEIGHT_BOLD = "bold"

# ==================== ANIMATION ====================

ANIMATION_FAST = 150      # ms - quick interactions
ANIMATION_NORMAL = 250    # ms - standard transitions
ANIMATION_SLOW = 400      # ms - smooth, elegant

# ==================== CUSTOM THEME DICT ====================

GLASS_THEME = {
    "CTk": {
        "fg_color": [BG_DARK, BG_DARK]
    },
    "CTkFrame": {
        "fg_color": [BG_GLASS, BG_GLASS],
        "border_color": [BORDER_GLASS, BORDER_GLASS],
        "border_width": 1
    },
    "CTkButton": {
        "fg_color": [ACCENT_PRIMARY, ACCENT_PRIMARY],
        "hover_color": [ACCENT_PRIMARY_GLOW, ACCENT_PRIMARY_GLOW],
        "border_color": [BORDER_GLOW, BORDER_GLOW],
        "border_width": 1,
        "corner_radius": RADIUS_MD,
        "text_color": [TEXT_PRIMARY, TEXT_PRIMARY]
    },
    "CTkEntry": {
        "fg_color": [BG_GLASS, BG_GLASS],
        "border_color": [BORDER_GLASS, BORDER_GLASS],
        "border_width": 1,
        "corner_radius": RADIUS_SM,
        "text_color": [TEXT_PRIMARY, TEXT_PRIMARY],
        "placeholder_text_color": [TEXT_TERTIARY, TEXT_TERTIARY]
    },
    "CTkLabel": {
        "text_color": [TEXT_PRIMARY, TEXT_PRIMARY]
    }
}

# ==================== HELPER FUNCTIONS ====================

def get_glass_style():
    """Returns base glass panel styling"""
    return {
        "fg_color": BG_GLASS,
        "border_color": BORDER_GLASS,
        "border_width": 1,
        "corner_radius": RADIUS_LG
    }

def get_button_style(variant="primary"):
    """Returns button styling based on variant"""
    styles = {
        "primary": {
            "fg_color": ACCENT_PRIMARY,
            "hover_color": ACCENT_PRIMARY_GLOW,
            "border_color": BORDER_GLOW,
            "text_color": TEXT_PRIMARY
        },
        "secondary": {
            "fg_color": BG_GLASS,
            "hover_color": BG_GLASS_HOVER,
            "border_color": BORDER_GLASS,
            "text_color": TEXT_PRIMARY
        },
        "danger": {
            "fg_color": ACCENT_DANGER,
            "hover_color": "#dc2626",
            "border_color": ACCENT_DANGER,
            "text_color": TEXT_PRIMARY
        },
        "success": {
            "fg_color": ACCENT_SUCCESS,
            "hover_color": "#059669",
            "border_color": ACCENT_SUCCESS,
            "text_color": TEXT_PRIMARY
        }
    }
    return styles.get(variant, styles["primary"])

def get_input_style():
    """Returns input field styling"""
    return {
        "fg_color": BG_GLASS,
        "border_color": BORDER_GLASS,
        "border_width": 1,
        "corner_radius": RADIUS_SM,
        "text_color": TEXT_PRIMARY
    }
