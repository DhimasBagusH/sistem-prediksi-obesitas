# utils/preprocessor.py

import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'sistem_tingkat_obesitas_rf_top12fitur.pkl')

def preprocess_user_input(data_dict: dict):
    """
    Mengubah input user (dictionary) menjadi DataFrame yang siap diprediksi
    oleh model Random Forest (25 fitur).
    """
    # Buat DataFrame dari input (16 fitur asli)
    df = pd.DataFrame([data_dict])

    # Load pipeline model
    pipeline = joblib.load(MODEL_PATH)
    preprocessor = pipeline.named_steps['preprocessor']

    # Transformasi menggunakan preprocessor (menghasilkan 25 fitur)
    X_processed = preprocessor.transform(df)

    return X_processed

def get_feature_names():
    """Mendapatkan nama fitur setelah preprocessing"""
    pipeline = joblib.load(MODEL_PATH)
    preprocessor = pipeline.named_steps['preprocessor']
    return preprocessor.get_feature_names_out()