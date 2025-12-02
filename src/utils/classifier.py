import joblib
import os
from utils.feature_extractor import extract_features

# Ruta relativa al modelo desde src/
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ml", "model.pkl")

# Cargar el modelo entrenado
model = joblib.load(MODEL_PATH)

def classify(code: str):
    """Clasifica código como seguro o vulnerable."""
    text_features, raw_data = extract_features(code)
    pred = model.predict([text_features])[0]
    prob = max(model.predict_proba([text_features])[0])

    return pred, prob, raw_data
