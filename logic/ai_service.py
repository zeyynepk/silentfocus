def get_ai_comment(stats:dict, context:str) -> str:
    """
    Gerçek ai buraya bağlanacak
    """

    total = stats["total_focus_minutes"]
    sessions = stats["sessions"]
    work_extends = stats["work_extends"]
    current_mode = stats.get("current_mode", "WORK")

    if context == "LONG_BREAK":
        return "Harika iş! 4 seansı devirdin, şimdi uzun bir dinlenmeyi hak ettin 🌸"

    if context == "WORK_END":
        if work_extends >= 2:
            return "Çok yoğun çalıştın ama başardın. Şimdi mola zamanı! 🔥"
        return "Seans bitti! Kısa bir mola ile zihnini tazeleyelim ☕️"
    
    if work_extends >= 2:
        return (
            "Çalışma süreni oldukça zorlamışsın. "
            "Bu tempoyu sürdürmeden önce kısa bir mola "
            "vermen odak kaliteni korumana yardımcı olur."
        )
    
    if sessions > 0 and sessions % 4 == 0 and current_mode != "WORK":
        return("4 verimli seans tamamladın! Uzun mola yapabiliriz, tebrikler.")

    if context == "WORK_END":
        return (
            "Bu seansı istikrarlı bir şekilde tamamlamışsın. "
            "Kısa bir mola sonrası aynı ritmi koruyabilirsin."
        )

    if total >= 2:
        return (
            "Bugün odak süren güzel ilerliyor. "
            "Bu düzeni bozmadığın sürece verimli bir gün olacak."
        )

    return "Odak alışkanlığın şekilleniyor. Küçük adımlar doğru yönde."