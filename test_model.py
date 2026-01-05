# test_model.py

import tensorflow as tf
import os
import sys

# Define the base path (adjust if necessary)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_PATH, 'backend', 'models', 'flood', 'flood_model.h5')

print(f"Attempting to load model from: {MODEL_PATH}")

try:
    # This is the same function used in your backend
    model = tf.keras.models.load_model(MODEL_PATH)
    print("\nSUCCESS: Flood Model loaded successfully!")
    print(f"Model input shape: {model.input_shape}")

except Exception as e:
    print(f"\nFAILURE: The model file is likely corrupted or invalid.")
    print(f"Detailed Error: {e}")
    # sys.exit(1)