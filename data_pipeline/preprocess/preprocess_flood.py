import rasterio
import rasterio.mask
from rasterio.enums import Resampling
import os
import numpy as np
import geopandas as gpd

# -------------------------
# Absolute Paths (Windows)
# -------------------------
raw_flood = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\raw\flood.tif"
processed_flood = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\flood.npy"
india_shapefile = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\preprocess\gadm41_IND_0.shp"

# -------------------------
# Ensure processed folder exists
# -------------------------
os.makedirs(os.path.dirname(processed_flood), exist_ok=True)

# -------------------------
# Check if flood raster exists
# -------------------------
if not os.path.exists(raw_flood):
    raise FileNotFoundError(f"Flood raster not found at {raw_flood}. Please download it first.")

# -------------------------
# Clip to India boundary
# -------------------------
if os.path.exists(india_shapefile):
    india = gpd.read_file(india_shapefile)
    shapes = [feature["geometry"] for feature in india.__geo_interface__["features"]]
else:
    print(f"Warning: Shapefile {india_shapefile} not found. Skipping clipping.")
    shapes = None

# -------------------------
# Open raster and process
# -------------------------
with rasterio.open(raw_flood) as src:
    # Optional downsampling factor (e.g., 10x smaller)
    scale_factor = 0.1
    out_height = int(src.height * scale_factor)
    out_width = int(src.width * scale_factor)

    if shapes:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        flood_data = out_image[0]
    else:
        flood_data = src.read(1)

    # -------------------------
    # Resample (resize) raster
    # -------------------------
    flood_data_resampled = np.empty(shape=(out_height, out_width), dtype=np.float32)
    rasterio.warp.reproject(
        source=flood_data,
        destination=flood_data_resampled,
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=src.transform * src.transform.scale(
            src.width / out_width,
            src.height / out_height
        ),
        dst_crs=src.crs,
        resampling=Resampling.bilinear
    )
    flood_data = flood_data_resampled

# -------------------------
# Replace NaNs or infinities
# -------------------------
flood_data = np.nan_to_num(flood_data, nan=0.0, posinf=0.0, neginf=0.0)

# -------------------------
# Safe normalization
# -------------------------
f_min = np.min(flood_data)
f_max = np.max(flood_data)
if f_max > f_min:
    flood_data = (flood_data - f_min) / (f_max - f_min)
else:
    flood_data = np.zeros_like(flood_data)

# -------------------------
# Save processed flood data
# -------------------------
np.save(processed_flood, flood_data)
print(f"Flood data preprocessed and saved as {processed_flood}")
