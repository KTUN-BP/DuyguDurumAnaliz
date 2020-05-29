import cv2

from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QImage
from faceDetect import FaceDetect


class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)
    capture = None
    path = None
    flip = True
    options = {
        'genders': [],
        'emotions': [],
    }

    def setPath(self, path):
        self.path = path

    def setOptions(self, options):
        self.options = options

    def getCapture(self):
        if self.capture is None:
            if self.path is None:
                source = 0
            else:
                source = self.path
                self.flip = False

            self.capture = cv2.VideoCapture(source)

        return self.capture

    def quit(self):
        self.capture.release()
        self.capture = None

    def run(self):
        capture = self.getCapture()
        face_detect = FaceDetect()

        while True:
            # Her döngü yenilenmesinde bir kare alıyoruz
            ret, frame = capture.read()

            if ret:
                # Yüz tanıma sınıfımızı kullanarak görüntüyü alıyoruz
                detect = face_detect.run(frame=frame, flip=self.flip, options=self.options)['frame']

                # Görüntü renklerini düzenliyoruz
                frame = cv2.cvtColor(detect, cv2.COLOR_BGR2RGB)

                # Görüntüyü QT objesine aktarıyoruz
                h, w, ch = frame.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(frame, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(800, 600, Qt.KeepAspectRatioByExpanding)
                self.changePixmap.emit(p)
