import pandas as pd
import os

# FIXED: Correct Excel path
raw_file = "data_pipeline/raw/landslides.csv"
processed_file = "data_pipeline/processed/landslides.csv"

os.makedirs("data_pipeline/processed", exist_ok=True)

# Try Excel first
try:
    df = pd.read_excel(raw_file, engine="openpyxl")
    print("Excel file loaded.")
except Exception as e:
    print("Excel failed — trying CSV...", e)
    df = pd.read_csv(raw_file)

print("Columns found:", list(df.columns))

# Detect useful columns
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

print("Detected Columns:", selected)

# If nothing found → save raw
if len(selected) == 0:
    print("⚠️ No useful columns found — saving RAW file instead.")
    df.to_csv(processed_file, index=False)
else:
    processed_df = df[[selected[k] for k in selected]]
    processed_df.to_csv(processed_file, index=False)

print(f"Processed landslide data saved to {processed_file}")
