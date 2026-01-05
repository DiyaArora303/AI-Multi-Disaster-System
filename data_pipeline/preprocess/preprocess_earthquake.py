import json
import pandas as pd
import os

raw_file = "data_pipeline/raw/earthquakes.json"
processed_file = "data_pipeline/processed/earthquakes.csv"

os.makedirs("data_pipeline/processed", exist_ok=True)

with open(raw_file) as f:
    data = json.load(f)

# Flatten data
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

df = pd.DataFrame(rows)
df.to_csv(processed_file, index=False)
print(f"Processed earthquake data saved to {processed_file}")
