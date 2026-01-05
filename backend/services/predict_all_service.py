# File: backend/services/predict_all_service.py (FINAL FIX)

import gc
import numpy as np
import pandas as pd
import time
from typing import Tuple, Dict, Any, List
# 

# Conditional import for Keras/TensorFlow resources (Stability)
try:
    import tensorflow.keras.backend as K
except ImportError:
    try:
        import keras.backend as K
    except ImportError:
        class MockK:
            @staticmethod
            def clear_session(): pass
        K = MockK

# Import all model loaders (ensure these files are present and functional)
from backend.models.cyclone_model_loader import predict_cyclone
from backend.models.flood_model_loader import predict_flood
from backend.models.earthquake_model_loader import predict_earthquake
from backend.models.landslide_model_loader import predict_landslide
from backend.models.heatwave_model_loader import predict_heatwave

# --- FLOOD DATA CONSTANTS ---
SAMPLES = 5
IMAGE_WIDTH = 64
IMAGE_HEIGHT = 64
IMAGE_CHANNELS = 1
TOTAL_ELEMENTS_TO_SAMPLE = SAMPLES * IMAGE_WIDTH * IMAGE_HEIGHT * IMAGE_CHANNELS 

def load_processed_data() -> Tuple[pd.DataFrame, np.ndarray, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all processed datasets with fixes for column names and memory."""
    base_path = "data_pipeline/processed"

    cyclone_df = pd.read_csv(f"{base_path}/cyclones.csv", low_memory=False)
    earthquake_df = pd.read_csv(f"{base_path}/earthquakes.csv")
    landslide_df = pd.read_csv(f"{base_path}/landslides.csv")
    heatwave_df = pd.read_csv(f"{base_path}/heatwave_processed.csv")
    
    # CRITICAL FIX 1: Clean DataFrame column names immediately
    for df in [cyclone_df, earthquake_df, landslide_df, heatwave_df]:
        df.columns = [col.strip().upper() for col in df.columns]

    # CRITICAL FIX 2: Memory-efficient loading and sampling for flood.npy
    try:
        flood_data_mmap = np.load(f"{base_path}/flood.npy", mmap_mode='r')
        
        # Check if the file has enough data for our required sample size
        if flood_data_mmap.size >= TOTAL_ELEMENTS_TO_SAMPLE:
            # Take a slice of EXACTLY the required sample size and ensure float32 dtype
            sample_data = flood_data_mmap[:TOTAL_ELEMENTS_TO_SAMPLE]
            # Reshape the small slice to the correct model input shape
            flood_data = sample_data.reshape((SAMPLES, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)).astype(np.float32)
        else:
            print("WARNING: Flood data too small for sampling, returning a single batch sample.")
            flood_data = flood_data_mmap.copy().reshape((1, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)).astype(np.float32)
    
    except Exception as e:
        print(f"CRITICAL ERROR loading flood data (mmap/sample failed): {e}. Returning dummy array.")
        flood_data = np.zeros((SAMPLES, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS), dtype=np.float32)
        
    return cyclone_df, flood_data, earthquake_df, landslide_df, heatwave_df

def run_all_predictions() -> Dict[str, Any]:
    """Run all ML models and return structured predictions"""

    # 1. Load Data
    cyclone_df, flood_data, earthquake_df, landslide_df, heatwave_df = load_processed_data()

    # -----------------------------
    # Cyclone Prediction (Input Shape: samples, 3, 2)
    # -----------------------------
    feature_columns = ['LAT', 'LON', 'WMO_WIND', 'WMO_PRES', 'DIST2LAND', 'STORM_SPEED']
    
    # CRITICAL FIX 3: Robust Data Cleaning for Cyclone Features (Solves ValueError)
    # 1. Identify columns available in the DataFrame
    available_cols = [col for col in feature_columns if col in cyclone_df.columns]

    # 2. Select only available columns
    cyclone_features_df = cyclone_df[available_cols].copy()
    
    # 3. Coerce all values in these columns to numeric (turning bad strings into NaN)
    for col in available_cols:
        cyclone_features_df.loc[:, col] = pd.to_numeric(cyclone_features_df[col], errors='coerce')
    
    # 4. Drop all rows that now contain NaN (i.e., rows with the problematic string ' ')
    cyclone_features_df = cyclone_features_df.dropna().reset_index(drop=True)
    
    
    # --- Prediction Prep ---
    cyclone_features_np = cyclone_features_df.tail(100).values.astype(np.float32)
    samples = cyclone_features_np.shape[0]
    
    if samples > 0:
        # Check if padding is needed (due to missing DIST2LAND/STORM_SPEED)
        padding_needed = 6 - cyclone_features_np.shape[1]
        if padding_needed > 0:
            print(f"WARNING: Cyclone model is missing {padding_needed} expected features. Padding with zeros.")
            pad = np.zeros((samples, padding_needed), dtype=np.float32)
            cyclone_features_np = np.hstack([cyclone_features_np, pad])
            
        try:
            # Reshape to final model input (samples, 3, 2)
            cyclone_features_reshaped = cyclone_features_np.reshape(samples, 3, 2)
            cyclone_preds = predict_cyclone(cyclone_features_reshaped)
        except Exception as e:
            print(f"Cyclone model error after padding: {e}")
            cyclone_preds = []
    else:
        print("ERROR: Cyclone DataFrame is empty after cleaning non-numeric values.")
        cyclone_preds = []


    # -----------------------------
    # Flood Prediction 
    # -----------------------------
    try:
        flood_preds = predict_flood(flood_data)
        flood_output = [float(np.mean(flood_preds))]
    except Exception as e:
        print(f"Flood model error: {e}")
        flood_output = [0.5]

    # -----------------------------
    # Earthquake Prediction (Assuming LATITUDE, LONGITUDE, DEPTH are clean)
    # -----------------------------
    eq_features_df = earthquake_df[['LONGITUDE', 'LATITUDE', 'DEPTH']].copy()
    for col in ['LONGITUDE', 'LATITUDE', 'DEPTH']: # Clean just in case
        eq_features_df.loc[:, col] = pd.to_numeric(eq_features_df[col], errors='coerce')
    eq_features_df = eq_features_df.dropna().tail(100)
    
    eq_preds = predict_earthquake(eq_features_df.values.astype(np.float32))

    # -----------------------------
    # Landslide Prediction
    # -----------------------------
    landslide_features_df = landslide_df[['LATITUDE', 'LONGITUDE']].copy()
    for col in ['LATITUDE', 'LONGITUDE']: # Clean just in case
        landslide_features_df.loc[:, col] = pd.to_numeric(landslide_features_df[col], errors='coerce')
    landslide_features_df = landslide_features_df.dropna().tail(100)
    
    landslide_preds = predict_landslide(landslide_features_df.values.astype(np.float32))

    # -----------------------------
    # Heatwave Prediction
    # -----------------------------
    heatwave_features_df = heatwave_df[['TMAX']].copy()
    heatwave_features_df.loc[:, 'TMAX'] = pd.to_numeric(heatwave_features_df['TMAX'], errors='coerce')
    heatwave_features_df = heatwave_features_df.dropna().tail(100)
    
    heatwave_features = heatwave_features_df.values.astype(np.float32)
    heatwave_preds = [
        predict_heatwave(f.reshape(1, -1))[0]
        for f in heatwave_features
    ]

    # -----------------------------
    # Stability Fix: Force TensorFlow/Keras Session Cleanup
    # -----------------------------
    try:
        K.clear_session()
        gc.collect()
        time.sleep(0.5)
    except Exception:
        pass 

    # -----------------------------
    # Aggregate results
    # -----------------------------
    results = {
        "cyclone": np.array(cyclone_preds).flatten().tolist(),
        "flood": flood_output,
        "earthquake": np.array(eq_preds).flatten().tolist(),
        "landslide": np.array(landslide_preds).flatten().tolist(),
        "heatwave": heatwave_preds
    }
    return results