import rasterio
from rasterio.enums import Resampling
import numpy as np
import os

# Absolute paths
flood_path = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\raw\flood.tif"
pop_path   = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\raw\population.tif"

os.makedirs(r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed", exist_ok=True)

# Load flood raster
with rasterio.open(flood_path) as flood_raster:
    flood_data = flood_raster.read(1)
    flood_meta = flood_raster.meta

# Load and resample population raster
with rasterio.open(pop_path) as pop_raster:
    pop_data = pop_raster.read(
        1,
        out_shape=flood_data.shape,
        resampling=Resampling.bilinear
    )

# Normalize population
pop_data = pop_data / pop_data.max()

# Combine
combined = np.stack([flood_data, pop_data], axis=-1)
np.save(r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\flood_population.npy", combined)

print("Processed flood + population data saved as flood_population.npy")
