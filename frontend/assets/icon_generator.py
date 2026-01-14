"""
PNG Icon Generator - Creates visible icons using QPainter
No SVG dependencies - pure raster graphics
"""
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon, QPainterPath
from PyQt6.QtCore import Qt, QPointF, QRectF


def create_home_icon(size=20, color="white"):
    """House icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    
    # Roof
    points = [
        QPointF(size * 0.5, size * 0.2),
        QPointF(size * 0.15, size * 0.5),
        QPointF(size * 0.85, size * 0.5)
    ]
    painter.drawPolyline(points)
    
    # House body
    painter.drawRect(int(size * 0.25), int(size * 0.5), int(size * 0.5), int(size * 0.4))
    
    # Door
    painter.drawRect(int(size * 0.4), int(size * 0.65), int(size * 0.2), int(size * 0.25))
    
    painter.end()
    return QIcon(pixmap)


def create_history_icon(size=20, color="white"):
    """Circular arrow icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    
    # Circle
    rect = QRectF(size * 0.15, size * 0.15, size * 0.7, size * 0.7)
    painter.drawArc(rect, 45 * 16, 270 * 16)
    
    # Arrow
    painter.drawLine(int(size * 0.3), int(size * 0.25), int(size * 0.3), int(size * 0.1))
    painter.drawLine(int(size * 0.3), int(size * 0.1), int(size * 0.45), int(size * 0.15))
    
    painter.end()
    return QIcon(pixmap)


def create_settings_icon(size=20, color="white"):
    """Gear icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    
    # Center circle
    center = size * 0.5
    painter.drawEllipse(QPointF(center, center), size * 0.2, size * 0.2)
    
    # Gear teeth (6 lines)
    for i in range(6):
        angle = i * 60
        rad = angle * 3.14159 / 180
        x1 = center + (size * 0.25) * (angle % 120 == 0)
        painter.drawLine(int(center), int(center - size * 0.35), int(center), int(center - size * 0.45))
        painter.translate(center, center)
        painter.rotate(60)
        painter.translate(-center, -center)
    
    painter.end()
    return QIcon(pixmap)


def create_mic_icon(size=20, color="white"):
    """Microphone icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    
    # Mic capsule
    rect = QRectF(size * 0.35, size * 0.15, size * 0.3, size * 0.4)
    painter.drawRoundedRect(rect, 8, 8)
    
    # Stand
    painter.drawLine(int(size * 0.5), int(size * 0.55), int(size * 0.5), int(size * 0.8))
    painter.drawLine(int(size * 0.3), int(size * 0.8), int(size * 0.7), int(size * 0.8))
    
    # Arc
    arc_rect = QRectF(size * 0.25, size * 0.4, size * 0.5, size * 0.35)
    painter.drawArc(arc_rect, 0, 180 * 16)
    
    painter.end()
    return QIcon(pixmap)


def create_send_icon(size=20, color="white"):
    """Paper plane / arrow icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    
    # Paper plane shape
    path = QPainterPath()
    path.moveTo(size * 0.15, size * 0.85)  # Bottom left
    path.lineTo(size * 0.85, size * 0.15)  # Top right
    path.lineTo(size * 0.5, size * 0.5)    # Middle
    path.lineTo(size * 0.15, size * 0.85)  # Back to start
    
    painter.drawPath(path)
    
    # Diagonal line
    painter.drawLine(int(size * 0.5), int(size * 0.5), int(size * 0.85), int(size * 0.85))
    
    painter.end()
    return QIcon(pixmap)


def create_close_icon(size=20, color="white"):
    """X icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    
    # X shape
    margin = size * 0.25
    painter.drawLine(int(margin), int(margin), int(size - margin), int(size - margin))
    painter.drawLine(int(size - margin), int(margin), int(margin), int(size - margin))
    
    painter.end()
    return QIcon(pixmap)


def create_minimize_icon(size=20, color="white"):
    """Horizontal line"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    
    painter.drawLine(int(size * 0.25), int(size * 0.5), int(size * 0.75), int(size * 0.5))
    
    painter.end()
    return QIcon(pixmap)


def create_maximize_icon(size=20, color="white"):
    """Square icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    
    margin = size * 0.25
    painter.drawRect(int(margin), int(margin), int(size - 2 * margin), int(size - 2 * margin))
    
    painter.end()
    return QIcon(pixmap)


def create_trash_icon(size=20, color="white"):
    """Trash bin icon"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    
    # Top line
    painter.drawLine(int(size * 0.2), int(size * 0.3), int(size * 0.8), int(size * 0.3))
    
    # Bin body
    painter.drawLine(int(size * 0.3), int(size * 0.3), int(size * 0.25), int(size * 0.8))
    painter.drawLine(int(size * 0.7), int(size * 0.3), int(size * 0.75), int(size * 0.8))
    painter.drawLine(int(size * 0.25), int(size * 0.8), int(size * 0.75), int(size * 0.8))
    
    # Handle
    painter.drawLine(int(size * 0.4), int(size * 0.3), int(size * 0.4), int(size * 0.2))
    painter.drawLine(int(size * 0.6), int(size * 0.3), int(size * 0.6), int(size * 0.2))
    painter.drawLine(int(size * 0.4), int(size * 0.2), int(size * 0.6), int(size * 0.2))
    
    painter.end()
    return QIcon(pixmap)


def create_search_icon(size=20, color="white"):
    """Magnifying glass"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    
    # Circle
    painter.drawEllipse(QPointF(size * 0.4, size * 0.4), size * 0.25, size * 0.25)
    
    # Handle
    painter.drawLine(int(size * 0.57), int(size * 0.57), int(size * 0.8), int(size * 0.8))
    
    painter.end()
    return QIcon(pixmap)


def create_download_icon(size=20, color="white"):
    """Download arrow"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    pen = QPen(QColor(color))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    
    # Vertical line
    painter.drawLine(int(size * 0.5), int(size * 0.2), int(size * 0.5), int(size * 0.65))
    
    # Arrow head
    painter.drawLine(int(size * 0.5), int(size * 0.65), int(size * 0.35), int(size * 0.5))
    painter.drawLine(int(size * 0.5), int(size * 0.65), int(size * 0.65), int(size * 0.5))
    
    # Bottom line
    painter.drawLine(int(size * 0.25), int(size * 0.8), int(size * 0.75), int(size * 0.8))
    
    painter.end()
    return QIcon(pixmap)


# Icon registry
ICON_REGISTRY = {
    "home": create_home_icon,
    "history": create_history_icon,
    "settings": create_settings_icon,
    "mic": create_mic_icon,
    "send": create_send_icon,
    "close": create_close_icon,
    "minimize": create_minimize_icon,
    "maximize": create_maximize_icon,
    "trash": create_trash_icon,
    "search": create_search_icon,
    "download": create_download_icon,
}


def get_icon(name, size=20, color="white"):
    """Get icon by name"""
    creator = ICON_REGISTRY.get(name.lower())
    if creator:
        return creator(size, color)
    # Default icon - circle
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidth(2)
    painter.setPen(pen)
    painter.drawEllipse(int(size * 0.25), int(size * 0.25), int(size * 0.5), int(size * 0.5))
    painter.end()
    return QIcon(pixmap)
