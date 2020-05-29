import cv2

from faceDetect import FaceDetect


def main():
    # OpenCV ile görüntü yakalamak için WebCam'i kullanıyoruz
    capture = cv2.VideoCapture(0)

    # Yüz tanıma sınıfımızı kullanabilmek için bir nesne oluşturuyoruz
    face_detect = FaceDetect()

    # Sonsuz bir döngü ile kameradan sürekli görüntü alacağız
    while True:
        # Her döngü yenilenmesinde bir kare alıyoruz
        ret, frame = capture.read()

        detect = face_detect.run(frame)['frame'];

        # Görüntü çıktısını alıyoruz
        cv2.imshow('frame', detect)

        # Q tuşu ile döngünün kırılmasını sağlıyoruz
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kamerayı kapatıyoruz
    capture.release()

    # Tüm pencereleri sonlandırıyoruz
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
