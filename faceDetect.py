import cv2
import settings
import numpy as np

from keras_preprocessing.image import img_to_array
from tensorflow.keras.models import load_model


class FaceDetect:
    options = {
        'genders': [],
        'emotions': [],
    }

    def __init__(self):
        # Yüz tespiti için gerekli XML verisi
        self.face_cascade = cv2.CascadeClassifier(settings.DATA['cascades']['face'])

        # Göz tespiti için gerekli XML verisi
        self.eye_cascade = cv2.CascadeClassifier(settings.DATA['cascades']['eye'])

        # Gülümseme tespiti için gerekli XML verisi
        self.smile_cascade = cv2.CascadeClassifier(settings.DATA['cascades']['smile'])

        # Duygu durum modeli
        self.emotion_model = load_model(settings.DATA['models']['emotion'], compile=False)

        # Cinsiyet modeli
        self.gender_model = load_model(settings.DATA['models']['gender'], compile=False)

    def run(self, frame, flip=False, options=None, _eyes=False, _smiles=False):
        # Görüntüyü aynalıyoruz
        if options is None:
            options = self.options

        if flip is True:
            frame = cv2.flip(frame, 1)

        # Görüntüyü gri tona çeviriyoruz
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Oluşturulan gri görüntüden yüzleri tespit ediyoruz
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        label = {}

        # Her bulunan yüz üzerinde işlem yapmak için bir döngü kullanıyoruz
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # Bulunan yüzün oldugu kareyi siyah beyaz yapıyoruz
                roi_gray = gray[y:y + h, x:x + w]

                # Bulunun yüzün olduğu kareyi renkli yapıyoruz
                roi_color = frame[y:y + h, x:x + w]

                # Bulunan yüz verisini ölçeklendirip numpy ve keras ile işliyoruz
                roi_gray = cv2.resize(roi_gray, (64, 64))
                roi_gray = roi_gray.astype('float') / 255.0
                roi_gray = img_to_array(roi_gray)
                roi_gray = np.expand_dims(roi_gray, axis=0)

                # Cinsiyeti analiz ediyoruz
                gender_predict = self.gender_model.predict(roi_gray)[0]
                # En yüksek skoru alan cinsiyet
                gender_probability = np.max(gender_predict)
                # Tüm cinsiyet verileri
                genders = []
                for (i, (gender, probability)) in enumerate(zip(settings.GENDERS, gender_predict)):
                    genders.append({
                        'title': gender,
                        'percent': round(probability * 100, 2),
                    })

                # Duygu durumunu analiz ediyoruz
                emotion_predict = self.emotion_model.predict(roi_gray)[0]
                # En yüksek skoru alan duygu durumu
                emotion_probability = np.max(emotion_predict)
                # Tüm duygu durum verileri
                emotions = []
                for (i, (emotion, probability)) in enumerate(zip(settings.EMOTIONS, emotion_predict)):
                    emotions.append({
                        'title': emotion,
                        'percent': round(probability * 100, 2),
                    })

                # Elde edilen skorları bir nesneye atıyoruz
                label = {
                    'gender': {
                        'title': settings.GENDERS[gender_predict.argmax()],
                        'percent': round(gender_probability * 100, 2),
                    },
                    'emotion': {
                        'title': settings.EMOTIONS[emotion_predict.argmax()],
                        'percent': round(emotion_probability * 100, 2),
                    },
                    'genders': genders,
                    'emotions': emotions,
                }

                # Bulunan yüze uygulayacağımız çerçeveyi oluşturuyoruz
                if gender_predict.argmax() in options['genders'] or emotion_predict.argmax() in options['emotions']:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)

                # Cinsiyet verisini görüntüye yazdırıyoruz
                if gender_predict.argmax() in options['genders']:
                    cv2.putText(frame, str(label['gender']['title']) + ' (%' + str(label['gender']['percent']) + ')',
                                (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 0, 255), 1)

                # Duygu verisini görüntüye yazdırıyoruz
                if emotion_predict.argmax() in options['emotions']:
                    cv2.putText(frame, str(label['emotion']['title']) + ' (%' + str(label['emotion']['percent']) + ')',
                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 0, 255), 1)

                # print(label)

                if _eyes:
                    # Bulunan yüzdeki gözleri tespit ediyoruz
                    eyes = self.eye_cascade.detectMultiScale(roi_gray)
                    # Bulunan gözlerde işlem yapmak için bir döngü kullanıyoruz
                    for (ex, ey, ew, eh) in eyes:
                        # Bulunan gözleri çerçeve içine alıyoruz
                        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                if _smiles:
                    # Bulunan yüzde gülücük arıyoruz
                    smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.7, 22)
                    # Bulunan gülücük verisininde işlem yapmak için bir döngü kullanıyoruz
                    for (sx, sy, sw, sh) in smiles:
                        # Bulunan gülücüği çerçeve içine alıyoruz
                        cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)

        # Oluşturulan yeni görüntüyü çıktı olarak veriyoruz
        return {
            'frame': frame,
            'label': label
        }
