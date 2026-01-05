import rasterio
from rasterio.enums import Resampling
import rasterio.mask
import numpy as np
import geopandas as gpd
import os
import cv2  # for resizing large arrays

def preprocess_flood_input(sensor_image_array=None, target_size=(256, 256)):
    """
    Preprocess flood raster or array for model inference.

    Args:
        sensor_image_array: Optional numpy array from FastAPI.
        target_size: (height, width) to resize large rasters for prediction.

    Returns:
        Numpy array ready for model: shape (1, H, W, 1 or 3)
    """

    raw_flood = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\raw\flood.tif"
    processed_flood = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\flood.npy"
    india_shapefile = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\preprocess\gadm41_IND_0.shp"

    # ----------------------------
    # FASTAPI INFERENCE MODE
    # ----------------------------
    if sensor_image_array is not None:
        arr = sensor_image_array.astype(np.float32)
        arr = np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)

        # Resize if not already target_size
        if arr.shape[0] != target_size[0] or arr.shape[1] != target_size[1]:
            arr = cv2.resize(arr, target_size[::-1], interpolation=cv2.INTER_LINEAR)

        # Normalize
        min_v, max_v = np.min(arr), np.max(arr)
        arr = (arr - min_v) / (max_v - min_v) if max_v > min_v else np.zeros_like(arr)

        # Handle channels
        if arr.ndim == 3 and arr.shape[2] == 3:
            return arr.reshape(1, arr.shape[0], arr.shape[1], 3)
        else:
            return arr.reshape(1, arr.shape[0], arr.shape[1], 1)

    # ----------------------------
    # OFFLINE PREPROCESSING MODE
    # ----------------------------
    os.makedirs(os.path.dirname(processed_flood), exist_ok=True)

    if not os.path.exists(raw_flood):
        raise FileNotFoundError(f"Flood raster not found at {raw_flood}")

    with rasterio.open(raw_flood) as src:
        flood_data = src.read(1).astype(np.float32)
        flood_data = np.nan_to_num(flood_data, nan=0.0, posinf=0.0, neginf=0.0)

        # Clip using shapefile
        if os.path.exists(india_shapefile):
            india = gpd.read_file(india_shapefile)
            shapes = [feat["geometry"] for feat in india.__geo_interface__["features"]]
            out_image, _ = rasterio.mask.mask(src, shapes, crop=True)
            flood_data = out_image[0].astype(np.float32)
            flood_data = np.nan_to_num(flood_data, nan=0.0, posinf=0.0, neginf=0.0)

        # Resize to target size for prediction
        if flood_data.shape != target_size:
            flood_data = cv2.resize(flood_data, target_size[::-1], interpolation=cv2.INTER_LINEAR)

        # Normalize
        f_min, f_max = np.min(flood_data), np.max(flood_data)
        flood_data = (flood_data - f_min) / (f_max - f_min) if f_max > f_min else np.zeros_like(flood_data)

        np.save(processed_flood, flood_data)
        print(f"Flood data preprocessed and saved as {processed_flood}")

    return flood_data.reshape(1, flood_data.shape[0], flood_data.shape[1], 1)
