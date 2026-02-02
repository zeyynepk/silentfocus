import sys
# QApplication, masaüstü uygulamasının çalışması için 
from PySide6.QtWidgets import QApplication
# Bu sınıf, uygulamamızın ana pencere tasarımını ve mantığı
from ui.main_window import MainWindow

def main():
    # sys.argv, program çalıştırılırken komut satırından gelen parametreleri tutar
    app = QApplication(sys.argv)
    # MainWindow sınıfından bir nesne 
    window = MainWindow()
    window.show()

    # event loop başlatıyoruz 
    # Kullanıcı tıklamaları, klavye girişleri vb. 
    sys.exit(app.exec())

# bu dosya başka bir dosya tarafından import edilirse main() çalışmaz

if __name__ == "__main__":
    # main fonksiyonunu çağırarak uygulamayı başlatıyoruz
    main()