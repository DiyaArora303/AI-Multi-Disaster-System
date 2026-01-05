# backend/shared/preprocess/processor_utils.py

import numpy as np

def preprocess_for_flood(raw_rainfall_map: np.ndarray) -> np.ndarray:
    """
    Preprocesses raw satellite/radar data into the (5, 256, 256, 1) shape 
    required by the Flood CNN/LSTM model.
    """
    TARGET_H, TARGET_W = 256, 256 

    if raw_rainfall_map is None:
        return np.zeros((5, TARGET_H, TARGET_W, 1), dtype=np.float32)

    try:
        # 1. Ensure the array is 4D: (Time, Height, Width, Channels)
        if raw_rainfall_map.ndim == 3:
            processed_data = np.expand_dims(raw_rainfall_map, axis=-1)
        else:
            processed_data = raw_rainfall_map

        # 2. Slice time dimension to 5 time steps
        if processed_data.shape[0] > 5:
             processed_data = processed_data[-5:] 
        
        # 3. Slice to the required H/W dimensions (256x256)
        final_data = processed_data[:5, :TARGET_H, :TARGET_W, :] 
        
        return final_data
    
    except Exception as e:
        print(f"Flood Preprocessing Failed: {e}")
        return np.zeros((5, TARGET_H, TARGET_W, 1), dtype=np.float32)


def preprocess_for_landslide(features: dict) -> list:
    """
    FIX: Returns exactly 2 features (rainfall_24h, slope_stability) to match the Landslide model's expectation.
    """
    feature_list = [
        features.get('rainfall_24h', 0.0),
        features.get('slope_stability', 5.0),
        # Removed the third feature (soil_saturation)
    ]
    return feature_list