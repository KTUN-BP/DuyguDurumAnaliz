import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from pictureThread import PictureThread


class PictureFileDialog(QDialog):
    def __init__(self):
        super(PictureFileDialog, self).__init__()

        self.Window = uic.loadUi('ui/pictureFileDialog.ui', self)
        self.setWindowTitle('Resim dosyası')

        self.setFixedSize(self.size())

        self.pictureThread = PictureThread()
        self.pictureThread.changePixmap.connect(self.setImage)
        self.pictureThread.setTerminationEnabled(True)

        self.output = None
        self.output_name = None

    @pyqtSlot()
    def on_pushButtonFileSelect_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters(['Resim dosyası (*.jpg *.jpeg *.png)'])

        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.output_name = os.path.basename(filenames[0])
            self.Window.labelSelectedFileName.setText(self.output_name)
            self.pictureThread.setPath(filenames[0])
            # Fotoğrafı aynalamak istersek
            #self.pictureThread.setFlip(True)
            self.Window.labelPictureFrame.setText('İşleniyor, lütfen bekleyin...')
            self.pictureThread.start()

    def closeEvent(self, event):
        if self.pictureThread.isRunning():
            self.pictureThread.quit()

    @pyqtSlot()
    def on_pushButtonSave_clicked(self):
        name = QFileDialog.getSaveFileName(self, 'Kaydet', self.output_name)
        if name[0] is not '':
            self.output.save(name[0])

    @pyqtSlot()
    def on_pushButtonClose_clicked(self):
        self.close()

    @pyqtSlot(QImage)
    def setImage(self, image):
        width = self.Window.labelPictureFrame.width()
        height = self.Window.labelPictureFrame.height()
        self.Window.labelPictureFrame.setPixmap(QPixmap.fromImage(image).scaled(width, height, Qt.KeepAspectRatio))

        # Kaydedilebilir çıktı
        self.output = image

        # Kaydetme butonunu aktifleştir
        self.Window.pushButtonSave.setEnabled(True)
