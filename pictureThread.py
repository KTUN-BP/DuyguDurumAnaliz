import cv2
import imutils

from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QImage
from faceDetect import FaceDetect


class PictureThread(QThread):
    changePixmap = pyqtSignal(QImage)
    capture = None
    path = None
    flip = False

    def setPath(self, path):
        self.path = path

    def getCapture(self):
        self.capture = cv2.imread(self.path)

        return self.capture

    def setFlip(self, flip=True):
        self.flip = flip

    def quit(self):
        self.capture.release()
        self.capture = None

    def run(self):
        face_detect = FaceDetect()

        capture = self.getCapture()

        # Resmi en/boy oranını koruyarak imutils kütüphanesiyle ölçeklendiriyoruz
        frame = imutils.resize(capture, 800)

        # Yüz tanıma sınıfımızı kullanarak görüntüyü alıyoruz
        detect = face_detect.run(frame, self.flip)

        # Görüntü renklerini düzenliyoruz
        frame = cv2.cvtColor(detect, cv2.COLOR_BGR2RGB)

        # Görüntüyü QT objesine aktarıyoruz
        h, w, ch = frame.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(frame, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(800, 600, Qt.KeepAspectRatioByExpanding)
        self.changePixmap.emit(p)
