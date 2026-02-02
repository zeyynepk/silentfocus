import subprocess
# QWidget → pencere / container, QVBoxLayout → dikey yerleşim, QHBoxLayout → yatay yerleşim
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsOpacityEffect
# Qt → hizalama vb. sabitler
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer
from styles.themes import WORK_THEME , BREAK_THEME, LONG_BREAK_THEME
from logic.timer import PomodoroTimer
from ui.settings_window import SettingsDialog
from ui.widgets.ai_orb import AIOrb
from ui.widgets.ai_panel import AIPanel
from logic.focus_analyzer import FocusAnalyzer

# Ana pencere sınıfı
# QWidget’ten kalıtım alır
class MainWindow(QWidget):
   
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Silent Focus")
        self.resize(600, 400)
        self._create_widgets()
        self._create_layouts()
        self.opacity_effect = QGraphicsOpacityEffect(self.hero_card)
        self.hero_card.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        # Animasyon süresi (milisaniye)
        self.fade_anim.setDuration(220)
        self.setStyleSheet(WORK_THEME)
        self.timer_logic = PomodoroTimer()
        # UI tarafında saniye saymak için
        self.qt_timer = QTimer(self)
        # Her saniye _on_tick fonksiyonunu çağır
        self.qt_timer.timeout.connect(self._on_tick)

        #soft break(10 sn) için durum
        self.offer_active =False
        self.offer_seconds = 10

        #soft break için ayrı bir timer
        self.offer_timer = QTimer(self)
        self.offer_timer.timeout.connect(self._on_offer_tick)

        self.ai_panel = None
        self.last_ai_context = "MANUAL"

    def _create_widgets(self):

        # Sayaç alanını tutan ana kart (container)
        self.hero_card = QWidget()
        # CSS için isim 
        self.hero_card.setObjectName("hero_card")
        self.hero_icon = QLabel("🚀")
        
        self.hero_icon.setAlignment(Qt.AlignCenter)
        # CSS için isim
        self.hero_icon.setObjectName("hero_icon")
        self.label_time = QLabel("00:00")
        self.label_time.setAlignment(Qt.AlignCenter)
        self.label_time.setObjectName("label_time")

        self.session_label = QLabel("Seans: 0 | Toplam Odak: 0 dk")
        self.session_label.setAlignment(Qt.AlignCenter)
        self.session_label.setObjectName("session_label")

        self.btn_start = QPushButton("Start")
        self.btn_pause = QPushButton("Pause")
        self.btn_reset = QPushButton("Reset")
        self.btn_settings = QPushButton("⚙️")
        
        #soft break uzatma butonu(+5dk)
        self.btn_extend = QPushButton("+5 dk uzat")
        self.btn_extend.clicked.connect(self._accept_soft_break)
        self.btn_extend.setEnabled(False) #başta hep pasif

        # Butonlara tıklanınca hangi fonksiyon çalışacak
        self.btn_start.clicked.connect(self._start_timer)
        self.btn_pause.clicked.connect(self._pause_timer)
        self.btn_reset.clicked.connect(self._reset_timer)
        self.btn_settings.clicked.connect(self._open_settings)

        self.ai_orb = AIOrb(self)

    def _create_layouts(self):
        # LAYOUT :
        # Sağ üst  = Üst layout + YATAY + önce addStretch(), sonra buton
        # Sol üst  = Üst layout + YATAY + önce buton, sonra addStretch()
        # Ortalamak = Dikey layout'ta üstte ve altta addStretch() kullanmak

        hero_layout = QVBoxLayout()
        hero_layout.setSpacing(12) # Elemanlar arası boşluk
        hero_layout.setContentsMargins(32, 32, 32, 32) # İç boşluklar (padding)

        hero_layout.addWidget(self.hero_icon)
        hero_layout.addWidget(self.label_time)
        hero_layout.addWidget(self.session_label)
        self.hero_card.setLayout(hero_layout) # Hero kartın layout’unu ayarla

        
        main_layout = QVBoxLayout() # Ana pencerenin layout’u

        settings_layout = QHBoxLayout()
        settings_layout.addWidget(self.btn_settings)
        settings_layout.addStretch()
        main_layout.addLayout(settings_layout)
        
        # +5 dk uzat butonu hero kartın sağ üstüne
        extend_layout = QHBoxLayout()
        extend_layout.addStretch()
        extend_layout.addWidget(self.btn_extend)
        hero_layout.insertLayout(0, extend_layout)

        main_layout.setSpacing(24)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Ortalamak için üst boşluk
        main_layout.addStretch()
        main_layout.addWidget(self.hero_card)
        main_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(16)

        # Sol boşluk
        button_layout.addStretch()

        # Butonları ekle
        button_layout.addWidget(self.btn_start)
        button_layout.addWidget(self.btn_pause)
        button_layout.addWidget(self.btn_reset)
        
        # Sağ boşluk
        button_layout.addStretch()
        # Buton alanını ana layout’a ekle
        main_layout.addLayout(button_layout)

        orb_layout = QHBoxLayout()
        orb_layout.addStretch()
        orb_layout.addWidget(self.ai_orb)

        self.ai_panel_container = QVBoxLayout()
        self.ai_panel_container.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        # Panel alanı layout akışını bozmasın
        self.ai_panel_container.setContentsMargins(0, 0, 0, 0)
        self.ai_panel_container.addStretch()
        main_layout.addLayout(self.ai_panel_container)

        main_layout.addLayout(orb_layout)

        # Ana layout’u pencereye uygula
        self.setLayout(main_layout)

    # Çalışma / mola moduna göre UI güncelleme
    def set_mode(self, mode: str):
       
        # Önce fade-out (kaybolma)
        self.fade_anim.stop()
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.start()

        # Mod kontrolü
        if mode == "WORK":
            self.setStyleSheet(WORK_THEME)
            self.hero_icon.setText("🚀")

        elif mode == "BREAK":
            self.setStyleSheet(BREAK_THEME)
            self.hero_icon.setText("🌿")

        elif mode == "LONG_BREAK":
            self.setStyleSheet(LONG_BREAK_THEME)
            self.hero_icon.setText("🌸")

        # Fade-in (geri gelme)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.start()

    # Her saniye çalışan fonksiyon
    def _on_tick(self):

        # Mantık sınıfından 1 saniyelik ilerleme al
        result = self.timer_logic.tick()

        # Kalan süreyi dakika ve saniyeye çevir
        minutes = self.timer_logic.remaining // 60
        seconds = self.timer_logic.remaining % 60

        # Ekrana yaz
        self.label_time.setText(f"{minutes:02d}:{seconds:02d}")

        #seans ve toplam odak süresi
        total_minutes = self.timer_logic.total_focus_seconds // 60
        total_seconds= self.timer_logic.total_focus_seconds % 60

        self.session_label.setText(f"Seans: {self.timer_logic.session_count} | " f"Toplam odak: {total_minutes} dk {total_seconds:02d} sn")

        # Mod değiştiyse UI güncelle
        #offer_active == True : “+5 dk uzat” teklifi ekranda ve 10 saniyelik geri sayım devam ediyor
        if result == "PHASE_FINISHED" and not self.offer_active:
            self.qt_timer.stop()

            if self.timer_logic.can_extend():
                self._start_soft_break_offer()
            else:
                self._force_phase_change()

      

    # Start butonu
    def _start_timer(self):
        self.timer_logic.start()
        self.qt_timer.start(1000)

        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)

    # Pause butonu
    def _pause_timer(self):
        self.timer_logic.pause()
        self.qt_timer.stop()
        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)

    # Reset butonu
    def _reset_timer(self):
        self.timer_logic.reset()
        self.qt_timer.stop()
        self.label_time.setText("25:00")
        self.set_mode("WORK")
        self.btn_start.setEnabled(True)
        self.btn_pause.setEnabled(False)
    
    def _start_soft_break_offer(self):
        """
        WORK bitince 10 saniyelik +5 uzatma teklifi
        """
        self.qt_timer.stop()
        self.offer_mode = self.timer_logic.mode
        self.offer_active = True
        self.offer_seconds = 10
        self.btn_extend.setEnabled(True)
        self.btn_extend.setText(f"+5 dk uzat ({self.offer_seconds})")
        self.offer_timer.start(1000)
                
    def _force_phase_change(self):
        if self.timer_logic.mode == "WORK":
            self.last_ai_context = "WORK_END"
            self.timer_logic.session_count += 1

            if self.timer_logic.session_count %4 == 0:
                self.last_ai_context = "LONG_BREAK"
                self._notify("4 seans tamamlandı! Uzun mola zamanı 🛌")
                self.timer_logic.mode = "LONG_BREAK"
                self.timer_logic.remaining = self.timer_logic.LONG_BREAK_TIME
                self.set_mode("LONG_BREAK")
            else :
                self._notify("Çalışma bitti! Mola zamanı ☕️")
                self.timer_logic.mode = "BREAK"
                self.timer_logic.remaining = self.timer_logic.BREAK_TIME
                self.set_mode("BREAK")
            self.timer_logic.break_extend_count = 0
        else:
            self._notify("Mola bitti! Çalışmaya dön 💪")
            self.timer_logic.mode = "WORK"
            self.last_ai_context = "MANUAL"
            self.timer_logic.remaining = self.timer_logic.WORK_TIME
            self.timer_logic.work_extend_count = 0
            self.set_mode("WORK")

        # Ana timer'ı tekrar başlat
        self.qt_timer.start(1000)      

        # AI panel açıksa context değiştiğini bildir
        if self.ai_panel and self.ai_panel.isVisible():
            data = self.get_focus_data()
            context = self.get_ai_context()
            self.ai_panel.refresh(data, context)

    def _on_offer_tick(self):

        if not self.offer_active:
            return

        self.offer_seconds -= 1

        if self.offer_seconds <= 0:
            self.offer_timer.stop()
            self.offer_active = False

            self.btn_extend.setEnabled(False)
            self.btn_extend.setText("+5 dk uzat")

            self._force_phase_change()
            return

        self.btn_extend.setText(f"+5 dk uzat ({self.offer_seconds})")

    def _accept_soft_break(self):
        """
        kullanıcı 5 dk uzata bastı
       
    - Mod DEĞİŞMEZ
    - Sadece süre uzatılır
    - Hangi moddaysak (WORK / BREAK) orada devam edilir

        - mode = offer_mode yapılır
        - BREAK <-> WORK geçişi YAPILMAZ
    """
        
        if not self.offer_active:
            return
        
        if not self.timer_logic.can_extend():
            self.offer_timer.stop()
            self.offer_active = False
            self.btn_extend.setEnabled(False)
            self.btn_extend.setText("+5 dk uzat")
            self._force_phase_change()
            return
        
        self.timer_logic.use_extend()
        self.offer_timer.stop()
        self.offer_active = False
        self.btn_extend.setEnabled(False)
        self.btn_extend.setText("+5 dk uzat")

        self.qt_timer.start(1000)

    def _notify(self, message: str):
        subprocess.run(["osascript","-e", f'display notification "{message}" with title "Silent Focus"'])
    
    def _open_settings(self):

        dialog = SettingsDialog(
        work=self.timer_logic.WORK_TIME // 60, 
        break_=self.timer_logic.BREAK_TIME // 60,
        long_break=self.timer_logic.LONG_BREAK_TIME // 60,
        parent=self
        )
        
        if dialog.exec():
            values = dialog.get_values()
            self.timer_logic.WORK_TIME = values["work"] * 60
            self.timer_logic.BREAK_TIME = values["break"] * 60
            self.timer_logic.LONG_BREAK_TIME = values["long_break"] * 60

            if not self.timer_logic.running:
                self.timer_logic.remaining = self.timer_logic.WORK_TIME
                self.label_time.setText(f'{values["work"]:02d}:00')
    

    def toggle_ai_panel(self, orb):
        if self.ai_panel:
            if self.ai_panel.isVisible():
                self.ai_panel.hide()
            else:
                data = self.get_focus_data()
                context = self.get_ai_context()   
                self.ai_panel.refresh(data, context)
                self.ai_panel.show()
            return

        data = self.get_focus_data()
        context = self.get_ai_context()

        self.ai_panel = AIPanel(data, context, self)
        self.ai_panel.setFixedWidth(280)

        self.ai_panel_container.addWidget(self.ai_panel)
        self.ai_panel.show()

    def get_focus_data(self):
        return {
            "sessions": self.timer_logic.session_count,
            "total_focus_minutes": self.timer_logic.total_focus_seconds // 60 ,
            "work_extends": self.timer_logic.work_extend_count,
            "break_extends": self.timer_logic.break_extend_count,
            "current_mode": self.timer_logic.mode
        }


    def get_ai_context(self):
        
        if self.last_ai_context != "MANUAL":
            ctx = self.last_ai_context
            self.last_ai_context = "MANUAL"   
            return ctx

        if self.timer_logic.mode == "WORK" and self.timer_logic.work_extend_count >= 2:
            return "OVER_EXTEND"

        return "MANUAL"

    