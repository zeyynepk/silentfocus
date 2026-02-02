class FocusAnalyzer:
    def __init__(self):
        pass

    def analyze(self, stats: dict, context:str) -> str:
        """
        stats örneği:
        {
            "total_focus_minutes" : 90,
            "sessions" : 3,
            "work_extends" : 2,
            "break_extends" : 1
        }
        """

    
        total = stats["total_focus_minutes"]
        sessions = stats["sessions"]
        work_extends = stats["work_extends"]
        break_extends = stats["break_extends"]

    
        if context == "WORK_END":
            if work_extends >= 2:
                return "Kendini zorluyorsun 🔥 Molayı ihmal etme."
            if total < 5:
                return "Güzel bir başlangıç 🌱 Devamı gelir."
            if sessions >= 4:
                return "Bugün istikrarlısın 🧠 Güzel gidiyor."
            return "Odak iyiydi ✨"

    #  Uzun mola
        if context == "LONG_BREAK":
            return "Uzun molayı hak ettin 🧘‍♀️ Biraz nefes."

    #  Süreyi fazla uzatma
        if context == "OVER_EXTEND":
            return "Bugün sınırları zorluyorsun ⚠️ Dinlenmeye dikkat."

    #  Manuel sorgulama (orb tıklaması)
        if context == "MANUAL":
            if break_extends > 0:
                return "Molaları biraz uzatıyorsun ☕ Dengeyi koru."
            if total < 1:
                return "Henüz yeni başladık 🌱"
            if total < 10:
                return "Odak yeni yeni ısınıyor 🔥"
            if total < 15:
                return "Odak netleşmeye başladı ✨"
            if total < 20:
                return "Güzel bir akış yakalamışsın 💫"
            return "Bugün ciddi odaklanıyorsun ⚡️"