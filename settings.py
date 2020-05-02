import os

# Proje dizini
BASE_DIRECTORY = os.path.abspath(os.getcwd())

# Analiz kaynakları
SOURCES = {
    'picture': 'Fotoğraf',
    'video': 'Video',
    'camera': 'Kamera',
}

# DataSet
DATA = {
    'cascades': {
        # Yüz tespiti için gerekli XML dosyasının yolu
        'face': os.path.join(BASE_DIRECTORY, 'data', 'cascades', 'haarcascade_frontalface_default.xml'),
        # Göz tespiti için gerekli XML verisi
        'eye': os.path.join(BASE_DIRECTORY, 'data', 'cascades', 'haarcascade_eye.xml'),
        # Gülümseme tespiti için gerekli XML verisi
        'smile': os.path.join(BASE_DIRECTORY, 'data', 'cascades', 'haarcascade_smile.xml'),
    },
    'models': {
        # Yüz ifadesi modeli
        'emotion': os.path.join(BASE_DIRECTORY, 'data', 'models', '_mini_XCEPTION.102-0.66.hdf5'),
        # Cinsiyet modeli
        'gender': os.path.join(BASE_DIRECTORY, 'data', 'models', 'gender_mini_XCEPTION.21-0.95.hdf5'),
    },
}

# Duygu durumları
EMOTIONS = ['Sinirli', 'Igrenmis', 'Korkmus', 'Mutlu', 'Uzgun', 'Saskin', 'Notr']

# Cinsiyetler
GENDERS = ['Kadin', 'Erkek']
