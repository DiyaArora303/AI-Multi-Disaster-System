import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

def get_model_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "models", "flood_model_fast.h5")

try:
    # compile=False is required to skip the 'mse' metric error in Keras 3
    model_fast = load_model(get_model_path(), compile=False)
    print("Flood model loaded successfully.")
except Exception as e:
    print(f"Error loading Flood model: {e}")
    model_fast = None

def predict_flood(flood_input: np.ndarray):
    if model_fast is None: return {"error": "Model not loaded"}
    pred = model_fast.predict(flood_input.astype('float32'))
    return pred.tolist()