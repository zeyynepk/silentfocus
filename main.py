# Python'un sistemle (işletim sistemiyle) ilgili fonksiyonlarını kullanabilmek için sys modülünü içe aktarıyoruz
# Örneğin: programdan düzgün çıkış yapmak için sys.exit kullanacağız
import sys
# QApplication, masaüstü uygulamasının çalışması için ZORUNLU olan ana uygulama nesnesidir
from PySide6.QtWidgets import QApplication
# Bu sınıf, uygulamamızın ana pencere tasarımını ve mantığını içerir
from ui.main_window import MainWindow

# Programın ana çalışma fonksiyonunu tanımlıyoruz
# Python projelerinde genellikle tüm başlangıç işlemleri burada yapılır
def main():
    # QApplication nesnesini oluşturuyoruz
    # sys.argv, program çalıştırılırken komut satırından gelen parametreleri tutar
    # PySide6 uygulamaları QApplication OLMADAN çalışamaz
    app = QApplication(sys.argv)

    # MainWindow sınıfından bir nesne oluşturuyoruz
    # Bu, ekranda göreceğimiz ana pencereyi temsil eder
    window = MainWindow()

    # Oluşturduğumuz pencereyi ekranda görünür hale getiriyoruz
    window.show()

    # Uygulamanın çalışmasını başlatıyoruz (event loop)
    # Kullanıcı tıklamaları, klavye girişleri vb. burada dinlenir
    # sys.exit ile program düzgün bir şekilde kapatılır
    sys.exit(app.exec())


# Bu kontrol bloğu, dosyanın DOĞRUDAN çalıştırılıp çalıştırılmadığını kontrol eder
# Eğer bu dosya başka bir dosya tarafından import edilirse main() çalışmaz
# Eğer python main.py şeklinde çalıştırılırsa main() çalışır
if __name__ == "__main__":
    # main fonksiyonunu çağırarak uygulamayı başlatıyoruz
    main()