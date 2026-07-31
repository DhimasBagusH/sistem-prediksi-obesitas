# utils/predictor.py

import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'sistem_tingkat_obesitas_rf_top12fitur.pkl')

# Mapping integer (sesuai encoding_target saat training) ke label hasil prediksi
RISK_MAPPING = {
    0: 'Berat Badan Kurang',
    1: 'Berat Badan Normal',
    2: 'Kelebihan Berat Badan',
    3: 'Obesitas Kelas 1',
    4: 'Obesitas Kelas 2',
    5: 'Obesitas Kelas 3',
}

def load_model():
    """Load model Random Forest dari file .pkl"""
    return joblib.load(MODEL_PATH)

def predict_risk(X_processed):
    model = load_model()
    classifier = model.named_steps['classifier']

    prediksi_raw = int(classifier.predict(X_processed)[0])
    probabilitas = classifier.predict_proba(X_processed)[0]
    classes = classifier.classes_

    label = RISK_MAPPING.get(prediksi_raw, f"Kelas {prediksi_raw}")

    return label, probabilitas, classes

def get_probability_text(probabilitas, classes):
    """Mengubah array probabilitas menjadi teks yang rapi"""
    result = []
    for cls, prob in zip(classes, probabilitas):
        label_id = RISK_MAPPING.get(int(cls), f"Kelas {cls}")
        result.append(f"{label_id}: {prob * 100:.1f}%")
    return "\n".join(result)