import os
import numpy as np
import cv2
import joblib
import tensorflow as tf
from skimage.feature import hog

HERE = os.path.dirname(os.path.abspath(__file__))
CLASSES = ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise']

cnn = tf.keras.models.load_model(os.path.join(HERE, 'cnn_best.keras'))
svm = joblib.load(os.path.join(HERE, 'svm_hog.joblib'))
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def _hog(img48):
    return hog(img48, orientations=9, pixels_per_cell=(6, 6),
               cells_per_block=(2, 2), block_norm='L2-Hys')


def _softmax(z):
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def _detect_faces(gray, max_width=None):
    """Haar detection, optionally on a downscaled copy to keep live frames fast."""
    if max_width and gray.shape[1] > max_width:
        scale = max_width / gray.shape[1]
        small = cv2.resize(gray, (max_width, int(round(gray.shape[0] * scale))),
                           interpolation=cv2.INTER_AREA)
        faces = face_detector.detectMultiScale(
            small, scaleFactor=1.1, minNeighbors=5, minSize=(32, 32))
        if len(faces) == 0:
            return []
        return [(int(x / scale), int(y / scale), int(w / scale), int(h / scale))
                for x, y, w, h in faces]
    return face_detector.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))


def analyze(rgb, detect_max_width=None):
    """rgb: HxWx3 uint8 array. Returns dict with annotated image, face crop, and both models' outputs.

    detect_max_width is an optional speed-up for live frames: face detection runs
    on a smaller copy, while the crop and annotation still use the full frame.
    """
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    faces = _detect_faces(gray, max_width=detect_max_width)

    annotated = rgb.copy()
    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])  # largest face
        face = gray[y:y + h, x:x + w]
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (76, 120, 168), 3)
        face_found = True
    else:
        face = gray          # fallback: use the whole image
        face_found = False

    face48 = cv2.resize(face, (48, 48), interpolation=cv2.INTER_AREA)

    # Direct call is faster than cnn.predict() for single frames; output is identical.
    batch = face48.astype('float32')[None, ..., None] / 255.0
    cnn_probs = np.asarray(cnn(batch, training=False)[0])

    h_feat = _hog(face48)[None, :]
    svm_label = int(svm.predict(h_feat)[0])
    svm_scores = svm.decision_function(h_feat)[0]
    svm_probs = _softmax(svm_scores)   # relative scores, NOT calibrated probabilities

    return dict(annotated=annotated, face48=face48, face_found=face_found,
                cnn_probs=cnn_probs, svm_probs=svm_probs,
                cnn_label=int(cnn_probs.argmax()), svm_label=svm_label)
