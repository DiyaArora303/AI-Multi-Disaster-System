import pandas as pd
import os

def preprocess_landslide_input():
    raw_file = "data_pipeline/raw/landslides.csv"
    processed_file = "data_pipeline/processed/landslides.csv"
    os.makedirs(os.path.dirname(processed_file), exist_ok=True)

    try:
        df = pd.read_excel(raw_file, engine="openpyxl")
    except Exception:
        df = pd.read_csv(raw_file)

    possible_cols = {
        "latitude": ["latitude", "lat", "y"],
        "longitude": ["longitude", "lon", "lng", "x"],
        "date": ["event_date", "date", "reported_date"],
        "size": ["landslide_size", "size"],
        "trigger": ["trigger"],
    }

    selected = {}
    for key, options in possible_cols.items():
        for col in df.columns:
            if col.strip().lower() in options:
                selected[key] = col
                break

    if selected:
        df = df[[selected[k] for k in selected]]

    df.to_csv(processed_file, index=False)
    print(f"Processed landslide data saved to {processed_file}")

if __name__ == "__main__":
    preprocess_landslide_input()
