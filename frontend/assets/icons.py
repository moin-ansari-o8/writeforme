"""
PNG Icon System - Rasterized icons using QPainter
No SVG dependencies - pure QPixmap icons
"""
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


class IconButton:
    """Helper to create icon buttons with PNG icons"""
    
    @staticmethod
    def create(icon_name, size=40, on_click=None, tooltip="", color="white"):
        """
        Create a modern icon button with PNG icon
        
        Args:
            icon_name: Icon name (e.g., "home", "send", "mic")
            size: Button size (square)
            on_click: Click callback
            tooltip: Tooltip text
            color: Icon color
        
        Returns:
            QPushButton with visible icon
        """
        from PyQt6.QtWidgets import QPushButton
        from PyQt6.QtCore import Qt
        from .icon_generator import get_icon
        
        btn = QPushButton()
        btn.setFixedSize(size, size)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        if tooltip:
            btn.setToolTip(tooltip)
        
        if on_click:
            btn.clicked.connect(on_click)
        
        # Get PNG icon
        icon_size = int(size * 0.5)
        icon = get_icon(icon_name, icon_size, color)
        btn.setIcon(icon)
        btn.setIconSize(QSize(icon_size, icon_size))
        
        # Default styling
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: {size // 2}px;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 0.08);
            }}
            QPushButton:pressed {{
                background: rgba(255, 255, 255, 0.12);
            }}
        """)
        
        return btn
