import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog, QLabel

from videoThread import VideoThread


class VideoFileDialog(QDialog):
    def __init__(self):
        super(VideoFileDialog, self).__init__()

        # type: QLabel
        self.labelSelectedFileName = None

        self.Window = uic.loadUi('ui/videoFileDialog.ui', self)
        self.setWindowTitle('Video dosyası')

        self.setFixedSize(self.size())

        self.videoThread = VideoThread()
        self.videoThread.changePixmap.connect(self.setImage)
        self.videoThread.setTerminationEnabled(True)

    def closeEvent(self, event):
        if self.videoThread.isRunning():
            self.videoThread.quit()

    @pyqtSlot()
    def on_pushButtonFileSelect_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters(['Mp4 video dosyası (*.mp4)'])

        if file_dialog.exec_():
            if self.videoThread.isRunning():
                self.videoThread.quit()
                self.videoThread = VideoThread()
                self.videoThread.changePixmap.connect(self.setImage)
                self.videoThread.setTerminationEnabled(True)

            filenames = file_dialog.selectedFiles()
            self.labelSelectedFileName.setText(os.path.basename(filenames[0]))
            self.videoThread.setPath(filenames[0])
            self.videoThread.start()

    @pyqtSlot()
    def on_pushButtonClose_clicked(self):
        self.close()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.Window.labelVideoFrame.setPixmap(QPixmap.fromImage(image))
