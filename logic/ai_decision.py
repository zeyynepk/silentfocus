def should_ai_speak(stats: dict, context:str) -> bool:
    """
    AI şuanda konuşmalı mı ?
    sadece true/false döner
    """

    total = stats["total_focus_minutes"]
    sessions = stats["sessions"]
    work_extends = stats["work_extends"]
    break_extends = stats["break_extends"]

    if total < 1 :
        return False
    if work_extends >= 2 :
        return True
    if break_extends >=2 :
        return True
    if sessions > 4 :
        return True
    if context == "LONG_BREAK":
        return True
    if context == "WORK_END":
        return True
    return False 