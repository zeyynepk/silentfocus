# logic/ai_worker.py
from PySide6.QtCore import QObject, Signal
import traceback
from logic.ai_service import get_ai_comment

class AIWorker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, stats: dict, context: str):
        super().__init__()
        self.stats = stats
        self.context = context

    def run(self):
        try:
            print("🤖 AI Worker: İstek gönderiliyor...")
            text = get_ai_comment(self.stats, self.context)
            
            # Eğer text None dönerse veya içinde 'Error' varsa hata sinyali çak
            if text is None:
                raise Exception("API yanıt vermedi (None).")
            
            # OpenAI hata mesajı bazen metin olarak dönebilir, kontrol edelim:
            if "insufficient_quota" in str(text) or "error" in str(text).lower() and len(str(text)) < 200:
                 # Basit bir kontrol, hata mesajını yakalamak için
                 raise Exception("OpenAI Kotası Yetersiz (429). Lütfen bakiyenizi kontrol edin.")

            print("✅ AI Worker: Cevap başarılı.")
            self.finished.emit(text)

        except Exception as e:
            print(f"❌ AI WORKER ERROR: {e}")
            # traceback.print_exc()
            
            # Hatayı kullanıcıya gösterilecek şekilde sadeleştir
            error_msg = str(e)
            if "quota" in error_msg.lower():
                error_msg = "OpenAI kotası dolmuş. Lütfen API hesabınıza bakiye yükleyin."
            
            self.error.emit(error_msg)