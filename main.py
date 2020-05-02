import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen
from mainWindow import MainWindow


def main():
    # Uygulamayı oluştur
    app = QApplication(sys.argv)

    # Splash screen
    splash_pix = QPixmap('img/splash.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # 3 saniye bekle
    time.sleep(3)

    # Ana pencereyi göster
    mainWindow = MainWindow()
    mainWindow.show()

    # Ana pencere gösterilince splash screen'i kapan
    splash.finish(mainWindow)

    # Uygulamayı çalıştır
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
