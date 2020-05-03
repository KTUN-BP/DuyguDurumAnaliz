import settings

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QComboBox
from pictureFileDialog import PictureFileDialog
from videoCaptureDialog import VideoCaptureDialog
from videoFileDialog import VideoFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('ui/mainWindow.ui', self)
        self.setWindowTitle('Duygu Durum Analiz')

        # Aktif analiz kaynağı
        self.source = None

        # Analiz kaynaklarını QtComboBox nesnesine aktar
        self.comboBoxSource.addItem('Seçin')
        for i in settings.SOURCES:
            self.comboBoxSource.addItem(settings.SOURCES[i], i)

        self.comboBoxSource.currentIndexChanged.connect(self.on_combobox_changed)

    # Kaynak Combobox'ında seçim yapıldığında yapılacaklar
    def on_combobox_changed(self, index):
        # Aktif analiz kaynağını değiştir
        self.source = self.comboBoxSource.itemData(index)
        # Analiz kaynağı boş değilse butonu aktif, boşsa pasif et
        if self.source is not None:
            self.pushButtonResourceStart.setEnabled(True)
        else:
            self.pushButtonResourceStart.setEnabled(False)

    # Analizi başlat butonuna tıklanırsa yapılacaklar
    @pyqtSlot()
    def on_pushButtonResourceStart_clicked(self):
        if self.source == 'picture':
            pictureFileDialog = PictureFileDialog()
            pictureFileDialog.exec_()
        elif self.source == 'camera':
            videoCaptureDialog = VideoCaptureDialog()
            videoCaptureDialog.exec_()
        elif self.source == 'video':
            videoFileDialog = VideoFileDialog()
            videoFileDialog.exec_()
