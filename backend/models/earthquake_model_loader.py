import joblib
import numpy as np # Added import for clarity

model = joblib.load("backend/models/earthquake/eq_model.pkl")

def predict_earthquake(features: np.ndarray):
    """
    features: 2D array of earthquake parameters, shape (n_samples, n_features)
    returns probability or magnitude prediction
    """
    # FIX: Pass the features array directly. The test script ensures it's 2D (5, 3).
    # Original: pred = model.predict([features]) <-- This was causing the 3D error
    pred = model.predict(features)
    return pred.tolist()