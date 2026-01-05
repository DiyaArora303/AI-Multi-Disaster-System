import requests
import json
import os

# Save path
os.makedirs("data_pipeline/raw", exist_ok=True)
file_path = "data_pipeline/raw/earthquakes.json"

# USGS API for past 30 days earthquakes
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

response = requests.get(url)
data = response.json()

with open(file_path, "w") as f:
    json.dump(data, f, indent=4)

print(f"Earthquake data saved to {file_path}")
