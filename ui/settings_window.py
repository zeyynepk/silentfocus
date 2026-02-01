from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox
from PySide6.QtCore import Qt

class SettingsDialog (QDialog):
    def __init__(self, work, break_, long_break, parent = None):
        super().__init__(parent)
        self.work_minutes = work
        self.break_minutes = break_
        self.long_break_minutes = long_break

        self.setWindowTitle("Ayarlar")
        self.setFixedSize(300,250)
        self._create_widgets()
        self._create_layouts()

    def _create_widgets(self):

        self.title_label = QLabel("⏰ Süre Ayarları")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.work_label = QLabel("Çalışma süresi (dk)")
        self.work_spin = QSpinBox()
        self.work_spin.setRange(1, 120)
        self.work_spin.setValue(self.work_minutes)

        self.break_label = QLabel("Mola süresi (dk)")
        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 60)
        self.break_spin.setValue(self.break_minutes)

        self.long_break_label = QLabel("Uzun mola süresi (dk)")
        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(5, 120)
        self.long_break_spin.setValue(self.long_break_minutes)

        self.btn_save = QPushButton("Kaydet 📌")
        self.btn_save.setMinimumHeight(48)
        self.btn_save.clicked.connect(self.accept)

    def _create_layouts(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.work_label)
        main_layout.addWidget(self.work_spin)
        main_layout.addWidget(self.break_label)
        main_layout.addWidget(self.break_spin)
        main_layout.addWidget(self.long_break_label)
        main_layout.addWidget(self.long_break_spin)
        main_layout.addStretch()
        main_layout.addWidget(self.btn_save)
        self.setLayout(main_layout)
    
    def get_values(self):
        return{
            "work": self.work_spin.value(),
            "break": self.break_spin.value(),
            "long_break" : self.long_break_spin.value()

        }