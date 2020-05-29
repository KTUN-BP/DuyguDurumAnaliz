import cv2

from faceDetect import FaceDetect


def main():
    # OpenCV ile görüntü yakalamak için WebCam'i kullanıyoruz
    capture = cv2.imread('./data/test/pictures/01.jpg')

    frame = cv2.resize(capture, (600, 800))

    # Yüz tanıma sınıfımızı kullanabilmek için bir nesne oluşturuyoruz
    face_detect = FaceDetect()

    detect = face_detect.run(frame)['frame']

    # Görüntü çıktısını alıyoruz
    cv2.imshow('frame', detect)

    # Kapanması için bir tuşa basılmasını bekle
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
