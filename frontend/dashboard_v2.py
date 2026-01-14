"""
WriteForMe Dashboard - TRUE Glassmorphism with PyQt6
Real backdrop blur, frameless window, smooth animations
"""
import sys
from datetime import datetime, timedelta
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


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
        
        self.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
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
        self.setFixedSize(700, 600)
        
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
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title bar with close button
        title_bar = QHBoxLayout()
        title = QLabel("Transcription Details")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: rgb(230, 230, 230); background: transparent;")
        title_bar.addWidget(title)
        title_bar.addStretch()
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(32, 32)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(60, 60, 65, 0.9);
                border: none;
                border-radius: 8px;
                color: rgb(200, 200, 200);
                font-size: 16px;
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
        timestamp_label = QLabel(f"📅 {timestamp_text}")
        timestamp_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px; background: transparent;")
        info_layout.addWidget(timestamp_label)
        
        mode_text = self.data.get("mode", "default").replace("_", " ").title()
        mode_label = QLabel(f"Mode: {mode_text}")
        mode_label.setStyleSheet("""
            color: rgb(200, 200, 200);
            background: rgba(60, 60, 65, 0.95);
            border-radius: 6px;
            padding: 4px 12px;
            font-size: 12px;
        """)
        info_layout.addWidget(mode_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Raw transcription section
        raw_label = QLabel("Raw Transcription:")
        raw_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        raw_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent;")
        layout.addWidget(raw_label)
        
        raw_text = QTextEdit()
        raw_text.setPlainText(self.data.get("raw_text", "N/A"))
        raw_text.setReadOnly(True)
        raw_text.setMaximumHeight(120)
        raw_text.setStyleSheet("""
            QTextEdit {
                background: rgba(45, 45, 50, 0.9);
                border: none;
                border-radius: 8px;
                color: rgb(200, 200, 200);
                padding: 12px;
                font-size: 13px;
            }
        """)
        layout.addWidget(raw_text)
        
        # Refined text section
        refined_label = QLabel("Refined Text:")
        refined_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        refined_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent;")
        layout.addWidget(refined_label)
        
        refined_text = QTextEdit()
        refined_text.setPlainText(self.data.get("refined_text", "N/A"))
        refined_text.setReadOnly(True)
        refined_text.setMaximumHeight(120)
        refined_text.setStyleSheet("""
            QTextEdit {
                background: rgba(45, 45, 50, 0.9);
                border: none;
                border-radius: 8px;
                color: rgb(220, 220, 220);
                padding: 12px;
                font-size: 13px;
            }
        """)
        layout.addWidget(refined_text)
        
        # Stats
        stats_layout = QHBoxLayout()
        word_count = len(self.data.get("refined_text", "").split())
        stats_layout.addWidget(QLabel(f"Words: {word_count}"))
        stats_layout.addStretch()
        stats_label = QLabel(f"Words: {word_count}")
        stats_label.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 12px; background: transparent;")
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
        self.setFixedHeight(140)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.card_clicked.emit(self.data)
        super().mousePressEvent(event)
    
    def setup_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        # Header (timestamp + mode)
        header = QHBoxLayout()
        
        timestamp_text = self.data.get("timestamp", "")[:19].replace("T", " ")
        timestamp = QLabel(timestamp_text)
        timestamp.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 12px; background: transparent;")
        header.addWidget(timestamp)
        
        mode_badge = QLabel(self.data.get("mode", "").replace("_", " ").title())
        mode_badge.setStyleSheet("""
            color: rgb(200, 200, 200);
            background: rgba(60, 60, 65, 0.95);
            border: none;
            border-radius: 6px;
            padding: 4px 12px;
            font-size: 12px;
            font-weight: 600;
        """)
        header.addWidget(mode_badge)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Text preview
        refined_text = self.data.get("refined_text", "")
        preview = refined_text[:120] + ("..." if len(refined_text) > 120 else "")
        
        text_label = QLabel(preview)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 14px; background: transparent;")
        layout.addWidget(text_label)
        
        layout.addStretch()
        
        # Action buttons
        actions = QHBoxLayout()
        actions.addStretch()
        
        word_count = len(refined_text.split())
        count_label = QLabel(f"{word_count} words")
        count_label.setStyleSheet("color: rgba(255, 255, 255, 0.4); font-size: 12px; background: transparent;")
        actions.addWidget(count_label)
        
        reinject_btn = QPushButton("⟲ Re-inject")
        reinject_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reinject_btn.setStyleSheet("""
            QPushButton {
                background: rgba(220, 220, 220, 0.9);
                color: rgb(30, 30, 30);
                border: none;
                border-radius: 8px;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(240, 240, 240, 1);
            }
        """)
        reinject_btn.clicked.connect(lambda: self.reinject_clicked.emit(self.data))
        actions.addWidget(reinject_btn)
        
        delete_btn = QPushButton("×")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setFixedSize(32, 32)
        delete_btn.setStyleSheet("""
            QPushButton {
                background: rgba(60, 60, 65, 0.9);
                border: none;
                border-radius: 8px;
                font-size: 14px;
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
        
        # Proper glassmorphism background - opaque with blur
        path = QPainterPath()
        rect_f = QRectF(self.rect())
        path.addRoundedRect(rect_f, 12, 12)  # Rounded corners
        
        # Opaque frosted glass - NOT transparent
        glass_color = QColor(45, 45, 48, 245)  # Almost fully opaque
        painter.fillPath(path, glass_color)
        
        # Subtle highlight border for glass effect
        border_color = QColor(70, 70, 75, 150)
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
        main_layout.setContentsMargins(20, 20, 20, 20)
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
                border: none;
                border-radius: 20px;
            }
        """)
        content_layout = QVBoxLayout(content_glass)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.content_stack)
        
        main_layout.addWidget(content_glass, 1)
    
    def create_sidebar(self):
        """Create glass sidebar with navigation"""
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            QFrame {
                background: rgba(35, 35, 38, 0.98);
                border: none;
                border-radius: 20px;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Custom title bar
        titlebar = QHBoxLayout()
        titlebar.setSpacing(8)
        titlebar.setContentsMargins(10, 0, 0, 0)  # Left margin
        
        # Window controls - LEFT ALIGNED
        for icon, func in [("—", self.showMinimized), ("□", self.toggle_maximize), ("✕", self.close)]:
            btn = QPushButton(icon)
            btn.setFixedSize(30, 30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(50, 50, 55, 0.9);
                    border: none;
                    border-radius: 6px;
                    color: rgb(200, 200, 200);
                    font-size: 16px;
                }
                QPushButton:hover {
                    background: rgba(70, 70, 75, 1);
                }
            """)
            btn.clicked.connect(func)
            titlebar.addWidget(btn)
        
        # Drag area (takes remaining space)
        drag_label = QLabel()
        drag_label.setFixedHeight(30)
        drag_label.mousePressEvent = self.mousePressEvent
        drag_label.mouseMoveEvent = self.mouseMoveEvent
        titlebar.addWidget(drag_label, 1)
        
        layout.addLayout(titlebar)
        
        # App header
        app_name = QLabel("WriteForMe")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        app_name.setStyleSheet("color: rgb(230, 230, 230);")
        layout.addWidget(app_name)
        
        version = QLabel("v1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("color: rgb(120, 120, 125); font-size: 12px;")
        layout.addWidget(version)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        self.nav_buttons = {}
        for tab_id, label in [
            ("home", "Home"),
            ("history", "History"),
            ("settings", "Settings"),
            ("stats", "Statistics")
        ]:
            btn = QPushButton(label)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(48)
            btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
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
        
        status_label = QLabel("● Capsule Active")
        status_label.setStyleSheet("color: rgb(100, 200, 100); font-size: 13px; font-weight: 600;")
        status_layout.addWidget(status_label)
        
        hotkey_label = QLabel("Win+Shift to record")
        hotkey_label.setStyleSheet("color: rgb(140, 140, 145); font-size: 11px;")
        status_layout.addWidget(hotkey_label)
        hotkey_label.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 11px;")
        status_layout.addWidget(hotkey_label)
        
        layout.addWidget(status_frame)
        
        # Highlight first tab
        self.switch_tab("home")
        
        return sidebar
    
    def create_home_tab(self):
        """Create home tab with ChatGPT-like interface"""
        tab = QWidget()
        tab.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)
        
        # Welcome header
        welcome = QLabel("Welcome to WriteForMe")
        welcome.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        welcome.setStyleSheet("color: rgb(230, 230, 230); background: transparent;")
        layout.addWidget(welcome)
        
        # Description
        desc = QLabel("Speech-to-text assistant with AI refinement")
        desc.setWordWrap(True)
        desc.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 15px; background: transparent;")
        layout.addWidget(desc)
        
        layout.addSpacing(20)
        
        # Model selector
        model_layout = QHBoxLayout()
        model_label = QLabel("AI Model:")
        model_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 13px; background: transparent;")
        model_layout.addWidget(model_label)
        
        self.model_selector = QComboBox()
        self.model_selector.addItems(["Vibe Coder", "Casual Chatter"])
        self.model_selector.setStyleSheet("""
            QComboBox {
                background: rgba(45, 45, 50, 0.9);
                border: none;
                border-radius: 8px;
                color: rgb(220, 220, 220);
                padding: 8px 16px;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: rgba(45, 45, 50, 0.98);
                color: rgb(220, 220, 220);
                selection-background-color: rgba(70, 70, 75, 0.9);
                border: none;
            }
        """)
        model_layout.addWidget(self.model_selector)
        model_layout.addStretch()
        layout.addLayout(model_layout)
        
        layout.addSpacing(10)
        
        # Input area with mic button (ChatGPT-like)
        input_container = QFrame()
        input_container.setStyleSheet("""
            QFrame {
                background: rgba(45, 45, 50, 0.95);
                border-radius: 16px;
            }
        """)
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(12, 12, 12, 12)
        input_layout.setSpacing(12)
        
        # Mic button on left
        self.mic_button = QPushButton("🎤")
        self.mic_button.setFixedSize(48, 48)
        self.mic_button.setCursor(Qt.CursorShape.PointingHandCursor)
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
            QPushButton:pressed {
                background: rgba(100, 100, 255, 0.8);
            }
        """)
        self.mic_button.clicked.connect(self.toggle_recording)
        input_layout.addWidget(self.mic_button)
        
        # Text input
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText("Type your prompt or click the mic to speak...")
        self.prompt_input.setMaximumHeight(120)
        self.prompt_input.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                color: rgb(220, 220, 220);
                padding: 8px;
                font-size: 14px;
            }
        """)
        input_layout.addWidget(self.prompt_input)
        
        layout.addWidget(input_container)
        
        # Processing status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 13px; background: transparent;")
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)
        
        # Result area
        self.result_container = QFrame()
        self.result_container.setStyleSheet("""
            QFrame {
                background: rgba(45, 45, 50, 0.95);
                border-radius: 12px;
            }
        """)
        result_layout = QVBoxLayout(self.result_container)
        result_layout.setContentsMargins(20, 20, 20, 20)
        
        result_title = QLabel("Refined Text:")
        result_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        result_title.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent;")
        result_layout.addWidget(result_title)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Refined text will appear here...")
        self.result_text.setStyleSheet("""
            QTextEdit {
                background: rgba(40, 40, 45, 0.9);
                border: none;
                border-radius: 8px;
                color: rgb(220, 220, 220);
                padding: 12px;
                font-size: 14px;
            }
        """)
        result_layout.addWidget(self.result_text)
        
        self.result_container.setVisible(False)
        layout.addWidget(self.result_container)
        
        layout.addStretch()
        
        # Initialize recording state
        self.is_recording_home = False
        
        return tab
    
    def create_history_tab(self):
        """Create history tab with transcriptions"""
        tab = QWidget()
        tab.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("Transcription History")
        title.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: rgb(230, 230, 230);")
        header.addWidget(title)
        
        self.stats_badge = QLabel("0 entries")
        self.stats_badge.setStyleSheet("""
            background: rgba(50, 50, 55, 0.8);
            color: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
            padding: 6px 16px;
            font-size: 13px;
        """)
        header.addWidget(self.stats_badge)
        header.addStretch()
        
        # Sort dropdown
        sort_label = QLabel("Sort:")
        sort_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 13px;")
        header.addWidget(sort_label)
        
        self.sort_selector = QComboBox()
        self.sort_selector.addItems(["Latest to Old", "Old to Latest"])
        self.sort_selector.setStyleSheet("""
            QComboBox {
                background: rgba(50, 50, 55, 0.9);
                border: none;
                border-radius: 8px;
                color: rgb(210, 210, 210);
                padding: 6px 16px;
                font-size: 13px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: rgba(50, 50, 55, 0.98);
                color: rgb(210, 210, 210);
                selection-background-color: rgba(70, 70, 75, 0.9);
                border: none;
            }
        """)
        self.sort_selector.currentIndexChanged.connect(self.on_sort_changed)
        header.addWidget(self.sort_selector)
        
        export_btn = QPushButton("Export")
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setStyleSheet(self.button_style())
        header.addWidget(export_btn)
        
        layout.addLayout(header)
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search transcriptions...")
        self.search_input.setMinimumHeight(48)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(45, 45, 50, 0.9);
                border: none;
                border-radius: 12px;
                color: rgb(220, 220, 220);
                padding: 0 20px;
                font-size: 14px;
            }
            QLineEdit:focus {
                background: rgba(255, 255, 255, 0.12);
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
        self.cards_layout.setSpacing(12)
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
        history_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "transcriptions_history.json")
        
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    transcriptions = data.get("transcriptions", [])
                    self.all_transcriptions = transcriptions
                    self.filtered_transcriptions = transcriptions.copy()
            else:
                self.all_transcriptions = []
                self.filtered_transcriptions = []
        except Exception as e:
            print(f"Error loading transcriptions: {e}")
            self.all_transcriptions = []
            self.filtered_transcriptions = []
        
        self.render_cards()
    
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
        """Delete transcription"""
        if data in self.all_transcriptions:
            self.all_transcriptions.remove(data)
        if data in self.filtered_transcriptions:
            self.filtered_transcriptions.remove(data)
        self.render_cards()
    
    def on_reinject(self, data):
        """Re-inject text"""
        print(f"[Re-inject] {data.get('refined_text', '')[:50]}...")
    
    def on_card_clicked(self, data):
        """Show detail dialog when card is clicked"""
        dialog = TranscriptionDetailDialog(data, self)
        dialog.exec()
    
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
                    mode_map = {"Vibe Coder": "vibe_coder", "Casual Chatter": "casual_chatter"}
                    mode = mode_map.get(self.model_selector.currentText(), "vibe_coder")
                    
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
        """Paint professional dark background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Professional dark gray gradient
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(18, 18, 18))      # Very dark gray
        gradient.setColorAt(0.5, QColor(24, 24, 24))    # Dark gray
        gradient.setColorAt(1, QColor(18, 18, 18))      # Very dark gray
        
        painter.fillRect(self.rect(), gradient)
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
