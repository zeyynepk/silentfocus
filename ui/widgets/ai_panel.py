from PySide6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer
from logic.focus_analyzer import FocusAnalyzer
from logic.ai_service import get_ai_comment

class AIPanel(QWidget):
    def __init__(self, data: dict, context:str, parent=None):
        super().__init__(parent)

        self.analyzer = FocusAnalyzer()
        self.message = self.analyzer.analyze(data,context)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self._create_ui()
        self.btn_real_ai.clicked.connect(self._on_real_ai_clicked)
        self.adjustSize()          #  içerik kadar büyü
        self._animate_open()

        self.loading_style = """
        QLabel {
            background-color: rgba(30, 41, 59, 0.6);
            border-radius: 12px;
            color: #cbd5e1;
            font-size: 12px;
            padding: 8px 12px;
        }
        """

        self.answer_style = """
        QLabel {
            background-color: rgba(30, 41, 59, 0.95);
            border-radius: 16px;
            border: 1px solid rgba(59, 130, 246, 0.45);
            color: #e5e7eb;
            font-size: 13px;
            padding: 12px 14px;
        }
        """
    def _create_ui(self):
        self.container = QLabel(self.message)
        self.container.setWordWrap(True)
        self.container.setAlignment(Qt.AlignCenter)

        self.container.setStyleSheet("""
            QLabel {
                background-color: rgba(20, 30, 50, 180);
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 30);
                color: rgba(255, 255, 255, 220);
                font-size: 14px;
                padding: 14px;
            }
        """)
        #AI butonu

        self.btn_real_ai = QPushButton("🤖 AI'dan yorum/öneri al")
        self.btn_real_ai.setCursor(Qt.PointingHandCursor)

        # AI cevabının gösterileceği alan

        self.real_ai_label = QLabel("")
        from PySide6.QtWidgets import QSizePolicy
        self.real_ai_label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
        self.real_ai_label.setWordWrap(True)
        self.real_ai_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.real_ai_label.setMinimumHeight(0)
        self.real_ai_label.setVisible(False)
        self.real_ai_label.setStyleSheet("""
            QLabel {
                background-color: rgba(30, 41, 59, 0.95);   /* theme uyumlu koyu mavi */
                border-radius: 16px;
                border: 1px solid rgba(59, 130, 246, 0.45);
                color: #e5e7eb;
                font-size: 13px;
                padding: 12px 14px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.container)
        layout.addWidget(self.btn_real_ai)
        layout.addWidget(self.real_ai_label)
        self.setLayout(layout)

    def _animate_open(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(250)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()
    
    def refresh(self, data, context):
    # üst AI mesajını güncelle
        self.context = context
        self.message = self.analyzer.analyze(data, context)
        self.container.setText(self.message)

        # AI alanı açıksa kapat
        self.real_ai_label.hide()
        self.btn_real_ai.setText("🤖 AI'dan yorum/öneri al")

        # panel boyutunu yeniden hesapla
        self.adjustSize()
    
    def _on_real_ai_clicked(self):
        if self.real_ai_label.isVisible():
            self.real_ai_label.hide()
            self.btn_real_ai.setText("🤖 AI'dan yorum/öneri al")
            return

        self.real_ai_label.setStyleSheet(self.loading_style)
        self.real_ai_label.setText("🤖 AI düşünüyor…")
        self.real_ai_label.show()

        QTimer.singleShot(1000, self._show_mock_ai_response)
        
    def _show_mock_ai_response(self):
        if not self.real_ai_label.isVisible():
            return

        response = get_ai_comment(stats=self.parent().get_focus_data(),context=self.context)

        self.real_ai_label.setStyleSheet(self.answer_style)
        self.real_ai_label.setText(response)


        self.real_ai_label.setFixedWidth(self.width())
        self.real_ai_label.setFixedHeight(
            self.real_ai_label.sizeHint().height()
        )

        self.adjustSize()