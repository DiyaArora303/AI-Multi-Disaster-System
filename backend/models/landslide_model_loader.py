import os
import joblib
import numpy as np
try:
    import xgboost # Required for unpickling Landslide models
except ImportError:
    print("CRITICAL: xgboost not found. Run 'pip install xgboost'")

def get_landslide_model():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_dir, "models", "landslide", "landslide_model.pkl")
    if not os.path.exists(path):
        path = os.path.join(base_dir, "models", "landslide_model.pkl")
    return joblib.load(path)

try:
    model = get_landslide_model()
    print("Landslide model loaded successfully.")
except Exception as e:
    print(f"Error loading Landslide model: {e}")
    model = None

def predict_landslide(features: np.ndarray):
    if model is None: return {"error": "Model not loaded"}
    # Pass features directly; ensure 2D shape (n_samples, n_features)
    if features.ndim == 1:
        features = features.reshape(1, -1)
    pred = model.predict(features)
    return pred.tolist()