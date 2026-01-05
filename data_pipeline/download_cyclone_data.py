import pandas as pd
import os

os.makedirs("data_pipeline/raw", exist_ok=True)

# Choose one of the working URLs:
url = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.since1980.list.v04r01.csv"

file_path = "data_pipeline/raw/cyclones.csv"

try:
    df = pd.read_csv(url)
    df.to_csv(file_path, index=False)
    print("Cyclone data downloaded and saved to:", file_path)
    print("Rows:", len(df))
except Exception as e:
    print("Error:", e)
