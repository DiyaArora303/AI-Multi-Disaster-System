import os
import tensorflow as tf
from tensorflow.keras.models import load_model

def load_prediction_model(model_path):
    """
    Loads model for inference only. 
    By setting compile=False, we avoid 'mse' and 'time_major' deserialization errors.
    """
    try:
        # We load without compiling because we only need model.predict()
        model = load_model(model_path, compile=False)
        print(f"Successfully loaded model: {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model {model_path}: {str(e)}")
        return None

# Use absolute path checking to be safe
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_FILE = os.path.join(BASE_DIR, "models", "cyclone_model.h5")

model = load_prediction_model(MODEL_FILE)

def predict_cyclone(data):
    if model is None:
        return {"error": "Model not loaded"}
    # model.predict requires a batch dimension
    prediction = model.predict(data)
    return prediction