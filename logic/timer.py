# Pomodoro zamanlayıcısının sadece iş mantığını tutan sınıf

class PomodoroTimer:
    
    WORK_TIME = 25 * 60
    BREAK_TIME = 5 * 60
    SOFT_BREAK_EXTRA = 5 * 60
    LONG_BREAK_TIME = 15 * 60

    def __init__(self):
        # Şu an hangi modda olduğumuzu tutar
        self.mode = "WORK"
        self.soft_break_used = False
        # Başlangıçta çalışma süresiyle başlar
        self.remaining = self.WORK_TIME
        self.session_count = 0
        self.total_focus_seconds = 0
        self.running = False
        self.work_extend_count = 0
        self.break_extend_count = 0
    

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.mode = "WORK"
        self.remaining = self.WORK_TIME
        self.session_count = 0
        self.total_focus_seconds = 0
        self.running = False

    # Her 1 saniyede bir çağrılması gereken fonksiyon
    def tick(self):

        # Eğer zamanlayıcı çalışmıyorsa
        if not self.running:
            return None

        if self.remaining <= 0:
            return "PHASE_FINISHED"

        self.remaining -= 1

        # WORK modunda odak süresini artır
        if self.mode == "WORK":
            self.total_focus_seconds += 1

        # Süre azaldıktan sonra tekrar kontrol
        if self.remaining <= 0:
            return "PHASE_FINISHED"

        return None
    
    # Uzatma izni
    def can_extend(self):
        if self.mode == "WORK":
            return self.work_extend_count < 2
        elif self.mode == "BREAK" or self.mode == "LONG_BREAK":
            return self.break_extend_count < 1
        return False
    
    def use_extend(self):
        if not self.can_extend():
            return False
        
        if self.mode == "WORK":
            self.work_extend_count += 1
        elif self.mode == "BREAK" or self.mode == "LONG_BREAK":
            self.break_extend_count += 1
        self.remaining += self.SOFT_BREAK_EXTRA