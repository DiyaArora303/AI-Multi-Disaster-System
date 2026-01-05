import rasterio
from rasterio.enums import Resampling
import numpy as np
import os

def preprocess_flood_population():
    flood_path = "data_pipeline/raw/flood.tif"
    pop_path   = "data_pipeline/raw/population.tif"
    processed_file = "data_pipeline/processed/flood_population.npy"

    os.makedirs(os.path.dirname(processed_file), exist_ok=True)

    with rasterio.open(flood_path) as f_r:
        flood_data = f_r.read(1)

    with rasterio.open(pop_path) as p_r:
        pop_data = p_r.read(
            1,
            out_shape=flood_data.shape,
            resampling=Resampling.bilinear
        )

    pop_data = pop_data / pop_data.max()
    combined = np.stack([flood_data, pop_data], axis=-1)
    np.save(processed_file, combined)
    print(f"Processed flood + population data saved as {processed_file}")

if __name__ == "__main__":
    preprocess_flood_population()
