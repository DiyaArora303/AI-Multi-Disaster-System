import os
import requests

os.makedirs("data_pipeline/raw", exist_ok=True)
out_path = "data_pipeline/raw/landslides.csv"

# List of candidate URLs (mirrors / catalog)
urls = [
    # Try NASA GLC CSV resource from data.gov
    "https://catalog.data.gov/dataset/7eca1a7a-4299-49e9-9e3a-2584d871009e/resource/a5c72ebd-ec18-410a-8847-1e4055c325ce/download/Global_Landslide_Catalog.csv",
    # Try GitHub / mirror on Kaggle raw file (via raw.githubusercontent.com or other gist) — example placeholder
    "https://raw.githubusercontent.com/nafayunnoor/global-landslide-catalog-glc-dataset/main/GLC.csv",
    # Try COOLR mirror from humanitarian data exchange (if hosted)
    "https://data.humdata.org/dataset/global-landslide-catalog-glc/download/global_landslides.csv"
]

for url in urls:
    try:
        print("Trying download from:", url)
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(r.content)
        print("✅ Download succeeded — saved to", out_path)
        break
    except Exception as e:
        print("❌ Download failed from:", url, "| Error:", e)

if not os.path.exists(out_path):
    raise RuntimeError("All download attempts failed — no landslide data file available.")
