from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog
from videoThread import VideoThread


class VideoCaptureDialog(QDialog):
    def __init__(self):
        super(VideoCaptureDialog, self).__init__()

        self.Window = uic.loadUi('ui/videoCaptureDialog.ui', self)
        self.setWindowTitle('Video yakala')

        self.setFixedSize(self.size())

        self.VideoThread = VideoThread()
        self.VideoThread.changePixmap.connect(self.setImage)
        self.VideoThread.setTerminationEnabled(True)

        self.VideoThread.start()

    def closeEvent(self, event):
        if self.VideoThread.isRunning():
            self.VideoThread.quit()

    @pyqtSlot()
    def on_pushButtonClose_clicked(self):
        self.close()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.Window.labelVideoFrame.setPixmap(QPixmap.fromImage(image))
