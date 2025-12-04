import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import os
from src.utils.feature_extractor import extract_features

# Ruta relativa al modelo desde src/
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "model.pkl")

# Cargar el modelo entrenado (pipeline con TF-IDF)
model = joblib.load(MODEL_PATH)

def classify(code: str):
    """Clasifica código como seguro o vulnerable."""
    # El modelo es un pipeline que acepta texto directamente
    pred = model.predict([code])[0]
    prob = float(max(model.predict_proba([code])[0]))  # Convertir a float nativo
    
    # Extraer características adicionales para detalles
    _, raw_data = extract_features(code)
    
    # Convertir todos los valores a tipos nativos de Python
    details = {k: int(v) if isinstance(v, (int, float)) else v for k, v in raw_data.items()}

    return str(pred), prob, details
