import json
import pandas as pd
import os

def preprocess_earthquake_input():
    raw_file = "data_pipeline/raw/earthquakes.json"
    processed_file = "data_pipeline/processed/earthquakes.csv"
    os.makedirs(os.path.dirname(processed_file), exist_ok=True)

    with open(raw_file) as f:
        data = json.load(f)

    features = data['features']
    rows = []
    for f in features:
        props = f['properties']
        geom = f['geometry']['coordinates']
        rows.append({
            'longitude': geom[0],
            'latitude': geom[1],
            'depth': geom[2],
            'magnitude': props['mag'],
            'place': props['place'],
            'time': props['time']
        })

    pd.DataFrame(rows).to_csv(processed_file, index=False)
    print(f"Processed earthquake data saved to {processed_file}")

if __name__ == "__main__":
    preprocess_earthquake_input()
