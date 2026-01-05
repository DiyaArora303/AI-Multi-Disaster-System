import os
import requests

os.makedirs("data_pipeline/raw", exist_ok=True)
file_path = "data_pipeline/raw/population.tif"

# Example: WorldPop population raster data
url = "https://data.worldpop.org/GIS/Population/India/india_ppp_2025.tif"

try:
    r = requests.get(url, stream=True)
    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f"Population data saved to {file_path}")
except Exception as e:
    print("Error downloading population data:", e)
