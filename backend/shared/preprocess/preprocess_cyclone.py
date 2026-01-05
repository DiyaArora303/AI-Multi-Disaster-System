import pandas as pd
import os

def preprocess_cyclone_input():
    raw_file = "data_pipeline/raw/cyclones.csv"
    processed_file = "data_pipeline/processed/cyclones.csv"
    os.makedirs(os.path.dirname(processed_file), exist_ok=True)

    df = pd.read_csv(raw_file, low_memory=False)
    columns_to_keep = ['NAME', 'ISO_TIME', 'LAT', 'LON', 'WMO_WIND', 'WMO_PRES']
    df = df[columns_to_keep]
    df.to_csv(processed_file, index=False)
    print(f"Processed cyclone data saved to {processed_file}")

if __name__ == "__main__":
    preprocess_cyclone_input()
