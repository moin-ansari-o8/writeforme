"""
WriteForMe Dashboard - Professional UI with Glassmorphism
Icons: PNG rasterized (no SVG), Typography: Inter/Segoe UI
"""
import sys
from datetime import datetime, timedelta
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

# Import PNG icon system
from assets.icons import IconButton


class GradientLabel(QLabel):
    """Label with gradient text effect"""
    
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.gradient_colors = [
            QColor(99, 102, 241),   # Blue
            QColor(139, 192, 241),  # Light blue
            QColor(99, 102, 241)    # Blue
        ]
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, self.gradient_colors[0])
        gradient.setColorAt(0.5, self.gradient_colors[1])
        gradient.setColorAt(1, self.gradient_colors[2])
        
        # Draw text with gradient
        painter.setPen(QPen(QBrush(gradient), 1))
        painter.setFont(self.font())
        painter.drawText(self.rect(), int(self.alignment()), self.text())
        painter.end()


class GlassFrame(QFrame):
    """Beautiful glass panel with blur and transparency"""
    
    def __init__(self, parent=None, blur_radius=20, opacity=0.3):
        super().__init__(parent)
        self.blur_radius = blur_radius
        self.glass_opacity = opacity
        
        # Enable transparency
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        
        # Apply blur effect
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(blur_radius)
        self.setGraphicsEffect(blur)
    
    def paintEvent(self, event):
        """Custom paint for glass effect"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Glass background with transparency
        path = QPainterPath()
        rect_f = QRectF(self.rect())
        path.addRoundedRect(rect_f, 16, 16)
        
        # Fill with semi-transparent white
        glass_color = QColor(255, 255, 255, int(self.glass_opacity * 255))
        painter.fillPath(path, glass_color)
        
        # Add subtle border
        border_color = QColor(255, 255, 255, 80)
        pen = QPen(border_color, 1)
        painter.setPen(pen)
        painter.drawPath(path)
        
        painter.end()


class ModernButton(QPushButton):
    """Beautiful button with hover effects"""
    
    def __init__(self, text, icon=None, parent=None):
        super().__init__(text, parent)
        self.default_color = QColor(60, 60, 65, 200)   # Professional gray
        self.hover_color = QColor(80, 80, 85, 230)     # Lighter gray on hover
        self.current_color = self.default_color
        
        self.setFont(QFont("Inter", 14, QFont.Weight.Medium))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(44)
        
        # Animation for smooth color transition
        self.anim = QPropertyAnimation(self, b"color")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    @pyqtProperty(QColor)
    def color(self):
        return self.current_color
    
    @color.setter
    def color(self, color):
        self.current_color = color
        self.update()
    
    def enterEvent(self, event):
        self.anim.setStartValue(self.current_color)
        self.anim.setEndValue(self.hover_color)
        self.anim.start()
    
    def leaveEvent(self, event):
        self.anim.setStartValue(self.current_color)
        self.anim.setEndValue(self.default_color)
        self.anim.start()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Rounded rectangle
        path = QPainterPath()
        rect_f = QRectF(self.rect())
        path.addRoundedRect(rect_f, 12, 12)
        painter.fillPath(path, self.current_color)
        
        # Text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        
        painter.end()


class TranscriptionDetailDialog(QDialog):
    """Dialog to show full transcription details"""
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Transcription Details")
        self.setModal(True)
        self.setFixedSize(780, 680)
        
        # Remove default window frame for custom styling
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main container with glass effect
        container = QWidget(self)
        container.setStyleSheet("""
            QWidget {
                background: rgba(35, 35, 38, 0.98);
                border-radius: 20px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # Title bar with close button
        title_bar = QHBoxLayout()
        title = QLabel("Transcription Details")
        title.setFont(QFont("Inter", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: rgb(240, 240, 240); background: transparent; letter-spacing: -0.5px;")
        title_bar.addWidget(title)
        title_bar.addStretch()
        
        close_btn = IconButton.create("close", size=32, tooltip="Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(60, 60, 65, 0.9);
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(180, 50, 50, 1);
            }
        """)
        close_btn.clicked.connect(self.accept)
        title_bar.addWidget(close_btn)
        layout.addLayout(title_bar)
        
        # Timestamp and mode
        info_layout = QHBoxLayout()
        timestamp_text = self.data.get("timestamp", "")[:19].replace("T", " ")
        timestamp_label = QLabel(timestamp_text)
        timestamp_label.setFont(QFont("Inter", 13))
        timestamp_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); background: transparent;")
        info_layout.addWidget(timestamp_label)
        
        mode_text = self.data.get("mode", "default").replace("_", " ").title()
        mode_label = QLabel(f"Mode: {mode_text}")
        mode_label.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        mode_label.setStyleSheet("""
            color: rgb(210, 210, 210);
            background: rgba(60, 60, 65, 0.95);
            border-radius: 8px;
            padding: 6px 16px;
        """)
        info_layout.addWidget(mode_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Raw transcription section
        raw_label = QLabel("Raw Transcription")
        raw_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        raw_label.setStyleSheet("color: rgba(255, 255, 255, 0.85); background: transparent; margin-top: 8px;")
        layout.addWidget(raw_label)
        
        raw_text = QTextEdit()
        raw_text.setPlainText(self.data.get("raw_text", "N/A"))
        raw_text.setReadOnly(True)
        raw_text.setMinimumHeight(140)
        raw_text.setFont(QFont("Inter", 14))
        raw_text.setStyleSheet("""
            QTextEdit {
                background: rgba(45, 45, 50, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 12px;
                color: rgb(200, 200, 200);
                padding: 18px;
                line-height: 1.6;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(80, 80, 85, 0.7);
                border-radius: 4px;
            }
        """)
        layout.addWidget(raw_text)
        
        # Refined text section
        refined_label = QLabel("Refined Text")
        refined_label.setFont(QFont("Inter", 17, QFont.Weight.Bold))
        refined_label.setStyleSheet("color: rgb(99, 102, 241); background: transparent; margin-top: 12px;")
        layout.addWidget(refined_label)
        
        refined_text = QTextEdit()
        refined_text.setPlainText(self.data.get("refined_text", "N/A"))
        refined_text.setReadOnly(True)
        refined_text.setMinimumHeight(160)
        refined_text.setFont(QFont("Inter", 14))
        refined_text.setStyleSheet("""
            QTextEdit {
                background: rgba(55, 55, 62, 0.95);
                border: 1px solid rgba(99, 102, 241, 0.2);
                border-radius: 12px;
                color: rgb(230, 230, 230);
                padding: 20px;
                line-height: 1.6;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: rgba(99, 102, 241, 0.5);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(99, 102, 241, 0.7);
            }
        """)
        layout.addWidget(refined_text)
        
        # Stats
        stats_layout = QHBoxLayout()
        word_count = len(self.data.get("refined_text", "").split())
        stats_layout.addWidget(QLabel(f"Words: {word_count}"))
        stats_layout.addStretch()
        stats_label = QLabel(f"Words: {word_count}")
        stats_label.setFont(QFont("Inter", 12))
        stats_label.setStyleSheet("color: rgba(255, 255, 255, 0.5); background: transparent;")
        layout.addWidget(stats_label)
        
        # Position container in dialog
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(container)


class TranscriptionCard(QFrame):
    """Glass card for displaying transcriptions"""
    
    delete_clicked = pyqtSignal(object)
    reinject_clicked = pyqtSignal(object)
    card_clicked = pyqtSignal(object)
    
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setMinimumHeight(160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.card_clicked.emit(self.data)
        super().mousePressEvent(event)
    
    def setup_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Header (timestamp + mode)
        header = QHBoxLayout()
        
        timestamp_text = self.data.get("timestamp", "")[:19].replace("T", " ")
        timestamp = QLabel(timestamp_text)
        timestamp.setFont(QFont("Inter", 12))
        timestamp.setStyleSheet("color: rgba(255, 255, 255, 0.5); background: transparent; border: none; outline: none;")
        header.addWidget(timestamp)
        
        mode_badge = QLabel(self.data.get("mode", "").replace("_", " ").title())
        mode_badge.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        mode_badge.setStyleSheet("""
            color: rgb(200, 200, 200);
            background: rgba(60, 60, 65, 0.95);
            border: none;
            border-radius: 6px;
            padding: 4px 12px;
        """)
        header.addWidget(mode_badge)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Text preview
        refined_text = self.data.get("refined_text", "")
        preview = refined_text[:180] + ("..." if len(refined_text) > 180 else "")
        
        text_label = QLabel(preview)
        text_label.setWordWrap(True)
        text_label.setFont(QFont("Inter", 14))
        text_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent; line-height: 1.5; border: none; outline: none;")
        layout.addWidget(text_label)
        
        layout.addStretch()
        
        # Action buttons
        actions = QHBoxLayout()
        actions.addStretch()
        
        word_count = len(refined_text.split())
        count_label = QLabel(f"{word_count} words")
        count_label.setFont(QFont("Inter", 12))
        count_label.setStyleSheet("color: rgba(255, 255, 255, 0.4); background: transparent;")
        actions.addWidget(count_label)
        
        reinject_btn = QPushButton("Re-inject")
        reinject_btn.setFont(QFont("Inter", 12, QFont.Weight.Medium))
        reinject_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reinject_btn.setStyleSheet("""
            QPushButton {
                background: rgba(220, 220, 220, 0.9);
                color: rgb(30, 30, 30);
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background: rgba(240, 240, 240, 1);
            }
        """)
        reinject_btn.clicked.connect(lambda: self.reinject_clicked.emit(self.data))
        actions.addWidget(reinject_btn)
        
        delete_btn = IconButton.create("trash", size=32, tooltip="Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background: rgba(60, 60, 65, 0.9);
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(180, 50, 50, 1);
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.data))
        actions.addWidget(delete_btn)
        
        layout.addLayout(actions)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Glassmorphism background
        path = QPainterPath()
        rect_f = QRectF(self.rect())
        path.addRoundedRect(rect_f, 12, 12)
        
        # Opaque frosted glass
        glass_color = QColor(45, 45, 48, 245)
        painter.fillPath(path, glass_color)
        
        # Thin subtle border
        border_color = QColor(255, 255, 255, 15)  # Very subtle white
        pen = QPen(border_color, 1)
        painter.setPen(pen)
        painter.drawPath(path)
        
        painter.end()


class GlassDashboard(QMainWindow):
    """Main frameless window with true glassmorphism"""
    
    def __init__(self):
        super().__init__()
        self.dragging = False
        self.drag_position = QPoint()
        self.current_tab = "home"
        self.is_maximized = False
        
        self.setup_window()
        self.setup_ui()
        self.load_mock_data()
    
    def setup_window(self):
        """Configure frameless transparent window"""
        self.setWindowTitle("WriteForMe")
        self.setGeometry(100, 100, 1100, 750)
        
        # Frameless with transparency
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Center on screen
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
    
    def setup_ui(self):
        """Build main UI layout"""
        # Central widget
        central = QWidget()
        central.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(16)
        
        # Right content area - CREATE FIRST before sidebar
        self.content_stack = QStackedWidget()
        self.content_stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create all tabs at startup (no lazy loading!)
        self.home_tab = self.create_home_tab()
        self.history_tab = self.create_history_tab()
        self.settings_tab = self.create_settings_tab()
        self.stats_tab = self.create_stats_tab()
        
        self.content_stack.addWidget(self.home_tab)
        self.content_stack.addWidget(self.history_tab)
        self.content_stack.addWidget(self.settings_tab)
        self.content_stack.addWidget(self.stats_tab)
        
        # Left sidebar - CREATE AFTER content_stack
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Wrap in solid glass frame
        content_glass = QFrame()
        content_glass.setStyleSheet("""
            QFrame {
                background: rgba(35, 35, 38, 0.98);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_glass)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Title bar at top right
        titlebar_container = QWidget()
        titlebar_container.setFixedHeight(50)
        titlebar_container.setStyleSheet("background: transparent;")
        titlebar_layout = QHBoxLayout(titlebar_container)
        titlebar_layout.setContentsMargins(10, 10, 10, 0)
        titlebar_layout.setSpacing(0)
        
        # Drag area
        drag_area = QLabel()
        drag_area.setStyleSheet("background: transparent; border: none; outline: none;")
        drag_area.mousePressEvent = self.mousePressEvent
        drag_area.mouseMoveEvent = self.mouseMoveEvent
        titlebar_layout.addWidget(drag_area, 1)
        
        # Window controls - RIGHT ALIGNED with Lucide icons
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        
        # Minimize button
        minimize_btn = IconButton.create("minimize", size=35, tooltip="Minimize")
        minimize_btn.setStyleSheet("""
            QPushButton {
                background: rgba(50, 50, 55, 0.9);
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(70, 70, 75, 1);
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        controls_layout.addWidget(minimize_btn)
        
        # Maximize button
        maximize_btn = IconButton.create("maximize", size=35, tooltip="Maximize")
        maximize_btn.setStyleSheet("""
            QPushButton {
                background: rgba(50, 50, 55, 0.9);
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(70, 70, 75, 1);
            }
        """)
        maximize_btn.clicked.connect(self.toggle_maximize)
        controls_layout.addWidget(maximize_btn)
        
        # Close button
        close_btn = IconButton.create("close", size=35, tooltip="Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(50, 50, 55, 0.9);
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: rgba(180, 50, 50, 1);
            }
        """)
        close_btn.clicked.connect(self.close)
        controls_layout.addWidget(close_btn)
        
        titlebar_layout.addLayout(controls_layout)
        content_layout.addWidget(titlebar_container)
        
        # Add content stack
        content_layout.addWidget(self.content_stack)
        
        main_layout.addWidget(content_glass, 1)
    
    def create_sidebar(self):
        """Create glass sidebar with navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            QFrame {
                background: rgba(35, 35, 38, 0.98);
                border: 1px solid rgba(255, 255, 255, 0.04);
                border-radius: 20px;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # App header with gradient
        app_name = GradientLabel("WriteForMe")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setFont(QFont("Inter", 26, QFont.Weight.DemiBold))
        app_name.setStyleSheet("background: transparent; border: none; outline: none; letter-spacing: -0.5px;")
        layout.addWidget(app_name)
        
        layout.addSpacing(20)
        
        # Navigation buttons with icons
        self.nav_buttons = {}
        nav_items = [
            ("home", "Home", "home"),
            ("history", "History", "history"),
            ("settings", "Settings", "settings"),
        ]
        
        for tab_id, label, icon_svg in nav_items:
            btn = QPushButton(f"  {label}")  # Spacing for icon
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(48)
            btn.setFont(QFont("Inter", 14, QFont.Weight.Medium))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: rgba(255, 255, 255, 0.6);
                    border: none;
                    border-radius: 12px;
                    text-align: left;
                    padding-left: 48px;
                }
                QPushButton:hover {
                    background: rgba(50, 50, 55, 0.6);
                    color: rgba(255, 255, 255, 0.9);
                }
            """)
            btn.clicked.connect(lambda checked, tid=tab_id: self.switch_tab(tid))
            layout.addWidget(btn)
            self.nav_buttons[tab_id] = btn
        
        layout.addStretch()
        
        # Status indicator
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background: rgba(40, 40, 45, 0.95);
                border: none;
                border-radius: 12px;
                padding: 12px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        status_layout.setSpacing(4)
        
        status_indicator = QLabel()
        status_indicator.setFixedSize(8, 8)
        status_indicator.setStyleSheet("background: rgb(100, 200, 100); border-radius: 4px; border: none;")
        status_text_layout = QHBoxLayout()
        status_text_layout.setSpacing(8)
        status_text_layout.addWidget(status_indicator)
        status_label = QLabel("Active")
        status_label.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        status_label.setStyleSheet("color: rgb(100, 200, 100); background: transparent; border: none; outline: none;")
        status_text_layout.addWidget(status_label)
        status_text_layout.addStretch()
        status_layout.addLayout(status_text_layout)
        
        layout.addWidget(status_frame)
        
        # Version at bottom left
        version = QLabel("v1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignLeft)
        version.setFont(QFont("Inter", 10))
        version.setStyleSheet("color: rgba(255, 255, 255, 0.3); background: transparent; border: none; outline: none; padding-top: 8px;")
        layout.addWidget(version)
        
        # Highlight first tab
        self.switch_tab("home")
        
        return sidebar
    
    def create_home_tab(self):
        """Create home tab with chat-style interface like GPT/Gemini"""
        tab = QWidget()
        tab.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Scrollable chat area
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chat_scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.15);
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.25);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Chat container
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(40, 40, 40, 20)
        self.chat_layout.setSpacing(12)
        self.chat_layout.addStretch()
        
        # Welcome message (centered overlay when no messages)
        self.welcome_widget = self.create_welcome_message()
        self.welcome_widget.setParent(self.chat_scroll)
        
        self.chat_scroll.setWidget(self.chat_container)
        layout.addWidget(self.chat_scroll, 1)
        
        # Sticky input bar at bottom
        input_wrapper = QWidget()
        input_wrapper.setStyleSheet("background: transparent;")
        input_wrapper_layout = QVBoxLayout(input_wrapper)
        input_wrapper_layout.setContentsMargins(40, 12, 40, 24)
        input_wrapper_layout.setSpacing(0)
        
        input_container = QFrame()
        input_container.setStyleSheet("""
            QFrame {
                background: rgba(45, 45, 50, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 24px;
            }
        """)
        
        # Main vertical layout for input container
        input_main_layout = QVBoxLayout(input_container)
        input_main_layout.setContentsMargins(18, 12, 18, 12)
        input_main_layout.setSpacing(10)
        
        # Text input area (compact chat-style)
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Message WriteForMe...")
        self.prompt_input.setMaximumHeight(120)
        self.prompt_input.setFixedHeight(32)  # Start compact
        self.prompt_input.setFont(QFont("Inter", 14))
        self.prompt_input.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.prompt_input.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                color: rgb(220, 220, 220);
                padding: 0;
            }
        """)
        # Auto-expand on text change
        self.prompt_input.textChanged.connect(self.adjust_input_height)
        input_main_layout.addWidget(self.prompt_input)
        
        # Bottom control bar with model selector and action buttons
        control_bar = QHBoxLayout()
        control_bar.setSpacing(6)
        
        # Model selector as pill-style dropdown (left side of control bar)
        self.model_selector = QComboBox()
        self.model_selector.addItems([
            "Cohere Command R7B",
            "Vibe Coder",
            "Casual Chat"
        ])
        self.model_selector.setFont(QFont("Inter", 13))
        self.model_selector.setFixedHeight(36)
        self.model_selector.setMinimumWidth(160)
        self.model_selector.setCursor(Qt.CursorShape.PointingHandCursor)
        self.model_selector.setStyleSheet("""
            QComboBox {
                background: rgba(60, 60, 65, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 18px;
                color: rgba(255, 255, 255, 0.85);
                padding: 6px 16px 6px 12px;
                font-size: 13px;
            }
            QComboBox:hover {
                background: rgba(70, 70, 75, 0.9);
                border-color: rgba(99, 102, 241, 0.5);
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                width: 0;
                height: 0;
            }
            QComboBox QAbstractItemView {
                background: rgba(40, 40, 45, 0.98);
                color: rgb(220, 220, 220);
                selection-background-color: rgba(99, 102, 241, 0.8);
                selection-color: white;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 6px;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 10px 14px;
                border-radius: 8px;
                margin: 2px;
            }
            QComboBox QAbstractItemView::item:hover {
                background: rgba(60, 60, 65, 0.8);
            }
        """)
        control_bar.addWidget(self.model_selector)
        
        control_bar.addStretch()
        
        # Mic button
        self.mic_button = IconButton.create("mic", size=40, tooltip="Record voice")
        self.mic_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.08);
            }
            QPushButton:pressed {
                background: rgba(99, 102, 241, 0.6);
            }
        """)
        self.mic_button.clicked.connect(self.toggle_recording)
        control_bar.addWidget(self.mic_button)
        
        # Send button
        self.submit_button = IconButton.create("send", size=40, tooltip="Send message")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background: rgba(99, 102, 241, 0.9);
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background: rgba(99, 102, 241, 1);
            }
            QPushButton:disabled {
                background: rgba(60, 60, 65, 0.5);
            }
        """)
        self.submit_button.clicked.connect(self.submit_prompt)
        control_bar.addWidget(self.submit_button)
        
        input_main_layout.addLayout(control_bar)
        
        input_wrapper_layout.addWidget(input_container)
        layout.addWidget(input_wrapper)
        
        # Store message list
        self.messages = []
        
        # Initialize recording state
        self.is_recording_home = False
        
        # Center welcome message after layout is ready
        QTimer.singleShot(100, self.center_welcome_message)
        
        return tab
    
    def create_welcome_message(self):
        """Create centered welcome message widget"""
        welcome_frame = QFrame()
        welcome_frame.setStyleSheet("background: transparent; border: none; outline: none;")
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setSpacing(12)
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Welcome to WriteForMe")
        title.setFont(QFont("Inter", 26, QFont.Weight.DemiBold))
        title.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent; border: none; outline: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(title)
        
        desc = QLabel("Speech-to-text assistant with AI refinement")
        desc.setFont(QFont("Inter", 15))
        desc.setStyleSheet("color: rgba(255, 255, 255, 0.5); background: transparent; border: none; outline: none;")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(desc)
        
        return welcome_frame
    
    def adjust_input_height(self):
        """Auto-adjust input height based on content"""
        doc_height = self.prompt_input.document().size().height()
        new_height = min(max(32, int(doc_height) + 8), 120)
        self.prompt_input.setFixedHeight(new_height)
    
    def center_welcome_message(self):
        """Center welcome message in scroll area"""
        if hasattr(self, 'welcome_widget') and self.welcome_widget.isVisible():
            scroll_width = self.chat_scroll.viewport().width()
            scroll_height = self.chat_scroll.viewport().height()
            welcome_width = self.welcome_widget.sizeHint().width()
            welcome_height = self.welcome_widget.sizeHint().height()
            
            x = (scroll_width - welcome_width) // 2
            y = (scroll_height - welcome_height) // 2
            
            self.welcome_widget.move(x, y)
    
    def add_message_bubble(self, text, is_user=False, is_thinking=False):
        """Add a chat message bubble"""
        # Hide welcome message on first message
        if hasattr(self, 'welcome_widget') and self.welcome_widget.isVisible():
            self.welcome_widget.setVisible(False)
        
        # Create bubble
        bubble = QFrame()
        bubble.setStyleSheet(f"""
            QFrame {{
                background: {'rgba(99, 102, 241, 0.9)' if is_user else 'rgba(45, 45, 50, 0.95)'};
                border: none;
                border-radius: 16px;
            }}
        """)
        
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(16, 12, 16, 12)
        bubble_layout.setSpacing(6)
        
        # Label header
        if not is_user:
            header = QLabel("Assistant" if not is_thinking else "Thinking...")
            header.setFont(QFont("Inter", 11, QFont.Weight.Medium))
            header.setStyleSheet("color: rgba(255, 255, 255, 0.5); background: transparent; border: none; outline: none;")
            bubble_layout.addWidget(header)
        
        # Message text
        message_label = QLabel(text if not is_thinking else "Refining your text...")
        message_label.setFont(QFont("Inter", 14))
        message_label.setStyleSheet("color: rgb(220, 220, 220); background: transparent; border: none; outline: none;")
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        bubble_layout.addWidget(message_label)
        
        # Alignment wrapper
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent; border: none;")
        wrapper_layout = QHBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        
        # Calculate responsive width (65-70% of chat area)
        chat_width = self.chat_scroll.viewport().width() - 80
        max_bubble_width = int(chat_width * 0.68)
        
        bubble.setMinimumWidth(200)
        bubble.setMaximumWidth(max_bubble_width)
        
        if is_user:
            wrapper_layout.addStretch()
            wrapper_layout.addWidget(bubble)
        else:
            wrapper_layout.addWidget(bubble)
            wrapper_layout.addStretch()
        
        # Insert before stretch
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, wrapper)
        
        # Scroll to bottom
        QTimer.singleShot(50, self.scroll_to_bottom)
        
        return bubble
    
    def resizeEvent(self, event):
        """Handle window resize to re-center welcome message"""
        super().resizeEvent(event)
        if hasattr(self, 'welcome_widget'):
            QTimer.singleShot(10, self.center_welcome_message)
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        scrollbar = self.chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def create_history_tab(self):
        """Create history tab with transcriptions"""
        tab = QWidget()
        tab.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("Transcription History")
        title.setFont(QFont("Inter", 28, QFont.Weight.DemiBold))
        title.setStyleSheet("color: rgb(230, 230, 230); letter-spacing: -0.5px; border: none; outline: none;")
        header.addWidget(title)
        
        self.stats_badge = QLabel("0 entries")
        self.stats_badge.setFont(QFont("Inter", 13))
        self.stats_badge.setStyleSheet("""
            background: rgba(50, 50, 55, 0.8);
            color: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
            padding: 6px 16px;
        """)
        header.addWidget(self.stats_badge)
        header.addStretch()
        
        # Sort dropdown
        sort_label = QLabel("Sort:")
        sort_label.setFont(QFont("Inter", 13))
        sort_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); border: none; outline: none;")
        header.addWidget(sort_label)
        
        self.sort_selector = QComboBox()
        self.sort_selector.addItems(["Latest to Old", "Old to Latest"])
        self.sort_selector.setFont(QFont("Inter", 13))
        self.sort_selector.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sort_selector.setStyleSheet("""
            QComboBox {
                background: rgba(50, 50, 55, 0.9);
                border: 1px solid rgba(70, 70, 75, 0.5);
                border-radius: 8px;
                color: rgb(210, 210, 210);
                padding: 8px 16px;
            }
            QComboBox:hover {
                border-color: rgba(99, 102, 241, 0.5);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: rgba(40, 40, 45, 0.98);
                color: rgb(220, 220, 220);
                selection-background-color: rgba(99, 102, 241, 0.8);
                border: 1px solid rgba(70, 70, 75, 0.5);
                border-radius: 8px;
                padding: 4px;
            }
        """)
        self.sort_selector.currentIndexChanged.connect(self.on_sort_changed)
        header.addWidget(self.sort_selector)
        
        export_btn = QPushButton("Export")
        export_btn.setFont(QFont("Inter", 13, QFont.Weight.Medium))
        export_btn.setMinimumHeight(40)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setStyleSheet("""
            QPushButton {
                background: rgba(99, 102, 241, 0.9);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background: rgba(99, 102, 241, 1);
            }
        """)
        header.addWidget(export_btn)
        
        layout.addLayout(header)
        
        # Search bar with icon
        search_container = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search transcriptions...")
        self.search_input.setMinimumHeight(48)
        self.search_input.setFont(QFont("Inter", 14))
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(45, 45, 50, 0.9);
                border: 1px solid rgba(70, 70, 75, 0.5);
                border-radius: 12px;
                color: rgb(220, 220, 220);
                padding: 0 48px 0 20px;
            }
            QLineEdit:focus {
                background: rgba(50, 50, 55, 0.95);
                border-color: rgba(99, 102, 241, 0.6);
            }
        """)
        self.search_input.textChanged.connect(self.on_search)
        layout.addWidget(self.search_input)
        
        # Scroll area for cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: rgba(35, 35, 38, 0.95);
                border-radius: 12px;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(80, 80, 85, 0.7);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        """)
        
        self.cards_container = QWidget()
        self.cards_container.setStyleSheet("background: rgba(35, 35, 38, 0.95); border-radius: 12px;")
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(28, 28, 28, 28)
        self.cards_layout.setSpacing(20)
        self.cards_layout.addStretch()
        
        scroll.setWidget(self.cards_container)
        layout.addWidget(scroll)
        
        return tab
    
    def create_settings_tab(self):
        """Create settings tab"""
        tab = QWidget()
        tab.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        
        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: rgb(230, 230, 230);")
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # AI Provider section
        section1 = self.create_settings_section("🤖 AI Provider")
        layout.addWidget(section1)
        
        # Writing Mode section  
        section2 = self.create_settings_section("✍️ Writing Mode")
        layout.addWidget(section2)
        
        layout.addStretch()
        
        return tab
    
    def create_settings_section(self, title):
        """Create a settings section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: rgba(42, 42, 45, 0.95);
                border: none;
                border-radius: 16px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: rgb(220, 220, 220);")
        layout.addWidget(title_label)
        
        desc = QLabel("Configure your preferences")
        desc.setStyleSheet("color: rgb(140, 140, 145); font-size: 13px;")
        layout.addWidget(desc)
        
        return frame
    
    def create_stats_tab(self):
        """Create statistics tab"""
        tab = QWidget()
        tab.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        
        title = QLabel("Statistics")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: rgb(230, 230, 230);")
        layout.addWidget(title)
        
        layout.addStretch()
        
        return tab
    
    def button_style(self):
        return """
            QPushButton {
                background: rgba(60, 60, 65, 0.95);
                border: none;
                border-radius: 10px;
                color: rgb(210, 210, 210);
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(75, 75, 80, 1);
            }
        """
    
    def load_mock_data(self):
        """Load real transcription data from JSON file"""
        import json
        import os
        
        # Path to transcriptions_history.json
        self.history_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "transcriptions_history.json")
        
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    transcriptions = data.get("transcriptions", [])
                    self.all_transcriptions = transcriptions
                    self.filtered_transcriptions = transcriptions.copy()
                    self.json_data = data  # Store full JSON structure
            else:
                self.all_transcriptions = []
                self.filtered_transcriptions = []
                self.json_data = {"version": "1.0", "transcriptions": []}
        except Exception as e:
            print(f"Error loading transcriptions: {e}")
            self.all_transcriptions = []
            self.filtered_transcriptions = []
            self.json_data = {"version": "1.0", "transcriptions": []}
        
        self.render_cards()
    
    def save_to_json(self):
        """Save transcriptions back to JSON file"""
        import json
        from datetime import datetime
        
        try:
            # Update the transcriptions in json_data
            self.json_data["transcriptions"] = self.all_transcriptions
            
            # Write back to file
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.json_data, f, indent=2, ensure_ascii=False)
            
            print(f"[Dashboard] Saved {len(self.all_transcriptions)} transcriptions to JSON")
        except Exception as e:
            print(f"Error saving transcriptions: {e}")
    
    def render_cards(self):
        """Render transcription cards"""
        # Clear existing cards
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Update stats
        self.stats_badge.setText(f"{len(self.filtered_transcriptions)} entries")
        
        # Apply sorting
        sorted_data = self.filtered_transcriptions.copy()
        if hasattr(self, 'sort_selector'):
            if self.sort_selector.currentIndex() == 0:  # Latest to Old
                sorted_data = sorted(sorted_data, key=lambda x: x.get('timestamp', ''), reverse=True)
            else:  # Old to Latest
                sorted_data = sorted(sorted_data, key=lambda x: x.get('timestamp', ''))
        
        # Add cards
        for data in sorted_data:
            card = TranscriptionCard(data)
            card.delete_clicked.connect(self.on_delete)
            card.reinject_clicked.connect(self.on_reinject)
            card.card_clicked.connect(self.on_card_clicked)
            self.cards_layout.insertWidget(0, card)
    
    def on_search(self, query):
        """Filter transcriptions by search"""
        if not query:
            self.filtered_transcriptions = self.all_transcriptions.copy()
        else:
            query_lower = query.lower()
            self.filtered_transcriptions = [
                t for t in self.all_transcriptions
                if query_lower in t.get("refined_text", "").lower()
            ]
        self.render_cards()
    
    def on_sort_changed(self, index):
        """Handle sort order change"""
        # 0 = Latest to Old, 1 = Old to Latest
        self.render_cards()
    
    def on_delete(self, data):
        """Delete transcription and persist to JSON"""
        if data in self.all_transcriptions:
            self.all_transcriptions.remove(data)
        if data in self.filtered_transcriptions:
            self.filtered_transcriptions.remove(data)
        
        # Persist to JSON file
        self.save_to_json()
        self.render_cards()
    
    def on_reinject(self, data):
        """Re-inject text"""
        print(f"[Re-inject] {data.get('refined_text', '')[:50]}...")
    
    def on_card_clicked(self, data):
        """Show detail dialog when card is clicked"""
        dialog = TranscriptionDetailDialog(data, self)
        dialog.exec()
    
    def submit_prompt(self):
        """Submit text prompt for processing"""
        text = self.prompt_input.toPlainText().strip()
        if not text:
            return
        
        # Add user message bubble
        self.add_message_bubble(text, is_user=True)
        
        # Clear input and reset height
        self.prompt_input.clear()
        self.prompt_input.setFixedHeight(32)
        
        # Add thinking bubble
        thinking_bubble = self.add_message_bubble("", is_user=False, is_thinking=True)
        QApplication.processEvents()
        
        try:
            # Get selected mode
            mode_text = self.model_selector.currentText()
            if "Vibe Coder" in mode_text:
                mode = "vibe_coder"
            elif "Casual Chat" in mode_text:
                mode = "casual_chatter"
            else:
                mode = "vibe_coder"
            
            # Import AI refiner
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from ai_refiner import AIRefiner
            
            if not hasattr(self, 'refiner'):
                self.refiner = AIRefiner(mode)
            else:
                self.refiner.set_mode(mode)
            
            refined_text = self.refiner.refine_text(text)
            
            # Remove thinking bubble
            thinking_bubble.deleteLater()
            
            # Add assistant response
            self.add_message_bubble(refined_text, is_user=False)
            
        except Exception as e:
            print(f"Error processing prompt: {e}")
            thinking_bubble.deleteLater()
            self.add_message_bubble(f"Error: {str(e)}", is_user=False)
    
    def toggle_recording(self):
        """Toggle recording state in home tab"""
        if not self.is_recording_home:
            # Start recording
            self.is_recording_home = True
            self.mic_button.setText("⏹")
            self.mic_button.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 80, 80, 0.9);
                    border: none;
                    border-radius: 24px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background: rgba(255, 100, 100, 1);
                }
            """)
            self.status_label.setText("🎤 Recording...")
            self.status_label.setVisible(True)
            self.result_container.setVisible(False)
            
            # Start actual recording
            self.start_home_recording()
        else:
            # Stop recording
            self.is_recording_home = False
            self.mic_button.setText("🎤")
            self.mic_button.setStyleSheet("""
                QPushButton {
                    background: rgba(60, 60, 65, 0.9);
                    border: none;
                    border-radius: 24px;
                    font-size: 20px;
                }
                QPushButton:hover {
                    background: rgba(80, 80, 85, 1);
                }
            """)
            self.status_label.setText("⏳ Processing...")
            
            # Stop recording and process
            self.stop_home_recording()
    
    def start_home_recording(self):
        """Start recording audio"""
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from audio_recorder import AudioRecorder
            
            if not hasattr(self, 'recorder'):
                self.recorder = AudioRecorder()
            
            self.recorder.start_recording()
        except Exception as e:
            print(f"Error starting recording: {e}")
            self.status_label.setText(f"Error: {e}")
    
    def stop_home_recording(self):
        """Stop recording and process"""
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from speech_to_text import SpeechToText
            from ai_refiner import AIRefiner
            import numpy as np
            
            if hasattr(self, 'recorder'):
                audio_data = self.recorder.stop_recording()
                
                # Transcribe
                self.status_label.setText("🔄 Transcribing...")
                QApplication.processEvents()
                
                if not hasattr(self, 'stt'):
                    self.stt = SpeechToText()
                
                raw_text = self.stt.transcribe_audio(audio_data)
                
                if raw_text:
                    # Show in input
                    self.prompt_input.setPlainText(raw_text)
                    
                    # Refine
                    self.status_label.setText("✨ Refining with AI...")
                    QApplication.processEvents()
                    
                    # Get selected mode
                    mode_text = self.model_selector.currentText()
                    if "Vibe Coder" in mode_text:
                        mode = "vibe_coder"
                    elif "Casual Chatter" in mode_text:
                        mode = "casual_chatter"
                    else:
                        mode = "vibe_coder"
                    
                    if not hasattr(self, 'refiner'):
                        self.refiner = AIRefiner(mode)
                    else:
                        self.refiner.set_mode(mode)
                    
                    refined_text = self.refiner.refine_text(raw_text)
                    
                    # Show result
                    self.result_text.setPlainText(refined_text)
                    self.result_container.setVisible(True)
                    self.status_label.setText("✅ Done!")
                    
                    # Hide status after 2 seconds
                    QTimer.singleShot(2000, lambda: self.status_label.setVisible(False))
                else:
                    self.status_label.setText("No speech detected")
                    QTimer.singleShot(2000, lambda: self.status_label.setVisible(False))
        except Exception as e:
            print(f"Error processing recording: {e}")
            self.status_label.setText(f"Error: {e}")
            QTimer.singleShot(3000, lambda: self.status_label.setVisible(False))
    
    def switch_tab(self, tab_id):
        """Switch between tabs"""
        self.current_tab = tab_id
        
        # Update button styles
        for tid, btn in self.nav_buttons.items():
            if tid == tab_id:
                btn.setStyleSheet("""
                    QPushButton {
                        background: rgba(70, 70, 75, 0.8);
                        color: rgb(240, 240, 240);
                        border: none;
                        border-radius: 12px;
                        text-align: left;
                        padding-left: 20px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        color: rgb(160, 160, 165);
                        border: none;
                        border-radius: 12px;
                        text-align: left;
                        padding-left: 20px;
                    }
                    QPushButton:hover {
                        background: rgba(50, 50, 55, 0.5);
                        color: rgb(220, 220, 220);
                    }
                """)
        
        # Switch content
        tab_index = {"home": 0, "history": 1, "settings": 2, "stats": 3}
        self.content_stack.setCurrentIndex(tab_index[tab_id])
    
    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.is_maximized:
            self.setGeometry(100, 100, 1100, 750)
            self.is_maximized = False
        else:
            screen = QApplication.primaryScreen().availableGeometry()
            self.setGeometry(screen)
            self.is_maximized = True
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
    
    def mouseReleaseEvent(self, event):
        self.dragging = False
    
    def paintEvent(self, event):
        """Paint professional dark background with rounded corners"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Professional dark gray gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(18, 18, 18))      # Very dark gray
        gradient.setColorAt(0.5, QColor(24, 24, 24))    # Dark gray
        gradient.setColorAt(1, QColor(18, 18, 18))      # Very dark gray
        
        # Draw rounded rectangle background
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)  # 20px border radius
        painter.fillPath(path, QBrush(gradient))
        painter.end()


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    
    print("🚀 Launching TRUE Glassmorphism Dashboard")
    print("✨ PyQt6 with real blur effects")
    print("🎨 Frameless window with smooth animations\n")
    
    window = GlassDashboard()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
