# backend/models/shared/model_loader.py

import tensorflow as tf
import joblib
import os
import sys

# Add backend directory to path for relative imports (if needed)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Define the absolute model path (re-using the fix from the previous step)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'backend', 'models') 

# Global dictionary to hold all loaded models
LOADED_MODELS = {}

def load_all_models():
    """
    Loads all models into memory once at startup, searching specific subfolders.
    """
    print(f"Loading ML models from forced path: {MODEL_PATH}")
    
    # ----------------------------------------------------------------------
    # 1. TENSORFLOW/KERAS MODELS (.h5)
    # ----------------------------------------------------------------------
    
    # --- Flood Model ---
    try:
        FLOOD_MODEL_PATH = os.path.join(MODEL_PATH, 'flood', 'flood_model.h5')
        LOADED_MODELS['flood'] = tf.keras.models.load_model(FLOOD_MODEL_PATH)
        print("-> Flood Model (Keras) loaded successfully.")
    except Exception as e:
        print(f"CRITICAL: Failed to load Flood Model: {e}. Model set to None.")
        LOADED_MODELS['flood'] = None

    # --- Cyclone Model ---
    try:
        CYCLONE_MODEL_PATH = os.path.join(MODEL_PATH, 'cyclone', 'cyclone_model.h5')
        LOADED_MODELS['cyclone'] = tf.keras.models.load_model(CYCLONE_MODEL_PATH)
        print("-> Cyclone Model (Keras) loaded successfully.")
    except Exception as e:
        print(f"CRITICAL: Failed to load Cyclone Model: {e}. Model set to None.")
        LOADED_MODELS['cyclone'] = None

    # ----------------------------------------------------------------------
    # 2. SCIKIT-LEARN/JOBLIB/PICKLE MODELS (.pkl)
    # ----------------------------------------------------------------------

    # --- Earthquake Model ---
    try:
        EQ_MODEL_PATH = os.path.join(MODEL_PATH, 'earthquake', 'eq_model.pkl')
        LOADED_MODELS['earthquake'] = joblib.load(EQ_MODEL_PATH)
        print("-> Earthquake Model (Joblib) loaded successfully.")
    except Exception as e:
        print(f"CRITICAL: Failed to load Earthquake Model: {e}. Model set to None.")
        LOADED_MODELS['earthquake'] = None

    # --- Heatwave Model ---
    try:
        HW_MODEL_PATH = os.path.join(MODEL_PATH, 'heatwave', 'heatwave_model.pkl')
        LOADED_MODELS['heatwave'] = joblib.load(HW_MODEL_PATH)
        print("-> Heatwave Model (Joblib) loaded successfully.")
    except Exception as e:
        print(f"CRITICAL: Failed to load Heatwave Model: {e}. Model set to None.")
        LOADED_MODELS['heatwave'] = None
        
    # --- Landslide Model ---
    try:
        LS_MODEL_PATH = os.path.join(MODEL_PATH, 'landslide', 'landslide_model.pkl')
        LOADED_MODELS['landslide'] = joblib.load(LS_MODEL_PATH)
        print("-> Landslide Model (Joblib) loaded successfully.")
    except Exception as e:
        print(f"CRITICAL: Failed to load Landslide Model: {e}. Model set to None.")
        LOADED_MODELS['landslide'] = None

    # --- Drought Model - SKIPPED AS REQUESTED ---
    LOADED_MODELS['drought'] = None
    print("-> Drought Model loading skipped.")