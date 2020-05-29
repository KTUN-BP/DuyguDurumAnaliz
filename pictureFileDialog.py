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

        self.selected_file = None

        self.setFixedSize(self.size())

        self.pictureThread = PictureThread()
        self.pictureThread.changePixmap.connect(self.setImage)
        self.pictureThread.setTerminationEnabled(True)

        self.output = None
        self.output_name = None

        self.Window.checkBoxGender.setVisible(False)
        self.Window.checkBoxFemale.setVisible(False)
        self.Window.checkBoxMale.setVisible(False)
        self.Window.checkBoxEmotion.setVisible(False)
        self.Window.checkBoxAngry.setVisible(False)
        self.Window.checkBoxDisgust.setVisible(False)
        self.Window.checkBoxScared.setVisible(False)
        self.Window.checkBoxHappy.setVisible(False)
        self.Window.checkBoxSad.setVisible(False)
        self.Window.checkBoxSurprised.setVisible(False)
        self.Window.checkBoxNeutral.setVisible(False)
        self.Window.pushButtonStart.setVisible(False)

        self.checkBoxGender.stateChanged.connect(self.onGenderChanged)
        self.checkBoxEmotion.stateChanged.connect(self.onEmotionChanged)

    @pyqtSlot()
    def on_pushButtonFileSelect_clicked(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilters(['Resim dosyası (*.jpg *.jpeg *.png)'])

        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            self.output_name = os.path.basename(filenames[0])
            self.Window.labelSelectedFileName.setText(self.output_name)
            self.selected_file = filenames[0]

            self.Window.checkBoxGender.setVisible(True)
            self.Window.checkBoxEmotion.setVisible(True)
            self.Window.pushButtonStart.setVisible(True)

    def closeEvent(self, event):
        if self.pictureThread.isRunning():
            self.pictureThread.quit()

    @pyqtSlot()
    def onGenderChanged(self):
        if self.Window.checkBoxGender.isChecked():
            self.Window.checkBoxFemale.setVisible(True)
            self.Window.checkBoxMale.setVisible(True)
        else:
            self.Window.checkBoxFemale.setVisible(False)
            self.Window.checkBoxMale.setVisible(False)

    @pyqtSlot()
    def onEmotionChanged(self):
        if self.Window.checkBoxEmotion.isChecked():
            self.Window.checkBoxAngry.setVisible(True)
            self.Window.checkBoxDisgust.setVisible(True)
            self.Window.checkBoxScared.setVisible(True)
            self.Window.checkBoxHappy.setVisible(True)
            self.Window.checkBoxSad.setVisible(True)
            self.Window.checkBoxSurprised.setVisible(True)
            self.Window.checkBoxNeutral.setVisible(True)
        else:
            self.Window.checkBoxAngry.setVisible(False)
            self.Window.checkBoxDisgust.setVisible(False)
            self.Window.checkBoxScared.setVisible(False)
            self.Window.checkBoxHappy.setVisible(False)
            self.Window.checkBoxSad.setVisible(False)
            self.Window.checkBoxSurprised.setVisible(False)
            self.Window.checkBoxNeutral.setVisible(False)

    @pyqtSlot()
    def on_pushButtonStart_clicked(self):
        self.pictureThread.setPath(self.selected_file)
        # Fotoğrafı aynalamak istersek
        # self.pictureThread.setFlip(True)
        self.Window.labelPictureFrame.setText('İşleniyor, lütfen bekleyin...')

        option_genders = []
        if self.Window.checkBoxGender.isChecked():
            if self.Window.checkBoxFemale.isChecked():
                option_genders.append(0)
            if self.Window.checkBoxMale.isChecked():
                option_genders.append(1)

        option_emotions = []
        if self.Window.checkBoxEmotion.isChecked():
            if self.Window.checkBoxAngry.isChecked():
                option_emotions.append(0)
            if self.Window.checkBoxDisgust.isChecked():
                option_emotions.append(1)
            if self.Window.checkBoxScared.isChecked():
                option_emotions.append(2)
            if self.Window.checkBoxHappy.isChecked():
                option_emotions.append(3)
            if self.Window.checkBoxSad.isChecked():
                option_emotions.append(4)
            if self.Window.checkBoxSurprised.isChecked():
                option_emotions.append(5)
            if self.Window.checkBoxNeutral.isChecked():
                option_emotions.append(6)

        self.pictureThread.options = {
            'genders': option_genders,
            'emotions': option_emotions,
        }

        self.pictureThread.start()

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
