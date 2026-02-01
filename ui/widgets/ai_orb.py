from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QPen, QColor, QConicalGradient
from ui.widgets.ai_panel import AIPanel

class AIOrb(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(50, 50)
        self.setCursor(Qt.PointingHandCursor)

        self.angle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(16)

    def _animate(self):
        self.angle = (self.angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(6, 6, self.width() - 12, self.height() - 12)

        # 🌈 Dairesel (conical) gradient
        gradient = QConicalGradient(rect.center(), self.angle)

        # YUMUŞAK RENK GEÇİŞLERİ
        gradient.setColorAt(0.00, QColor(255, 105, 180))  # pink
        gradient.setColorAt(0.25, QColor(138, 43, 226))   # purple
        gradient.setColorAt(0.50, QColor(0, 191, 255))    # blue
        gradient.setColorAt(0.75, QColor(255, 215, 0))    # yellow ✨
        gradient.setColorAt(1.00, QColor(255, 105, 180))  # back to pink

        pen = QPen()
        pen.setBrush(gradient)
        pen.setWidth(10)
        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)
        painter.drawArc(rect, 0, 360 * 16)

    def mousePressEvent(self, event):
     self.parent().toggle_ai_panel(self)