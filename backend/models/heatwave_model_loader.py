import joblib
import numpy as np

model = joblib.load("backend/models/heatwave/heatwave_model.pkl")
scaler = joblib.load("backend/models/heatwave/heatwave_scaler.pkl")

def predict_heatwave(features: np.ndarray):
    """
    features: 2D array of heatwave features (e.g., 'tmax'), shape (n_samples, 1)
    """
    # FIX 1: Pass the 2D features directly to the scaler's transform method.
    # The test script ensures features has shape (N, 1).
    # Original: features_scaled = scaler.transform([features]) <-- This created a 3D array
    features_scaled = scaler.transform(features)
    
    # FIX 2: Pass the scaled features directly to the model.
    # Original: pred = model.predict(features_scaled) (This was correct, if not for fix 1)
    pred = model.predict(features_scaled) 
    
    return pred.tolist()