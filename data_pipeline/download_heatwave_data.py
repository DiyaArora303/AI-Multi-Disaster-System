import os
import requests
import pandas as pd

os.makedirs("data_pipeline/raw", exist_ok=True)
file_path = "data_pipeline/raw/heatwave.csv"

# Single location example: center of India
latitude = 20.0
longitude = 80.0

url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}&"
    f"start_date=2025-01-01&end_date=2025-12-10&"
    f"daily=temperature_2m_max&timezone=Asia/Kolkata"
)

try:
    data = requests.get(url).json()
    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "tmax": data["daily"]["temperature_2m_max"]
    })
    df.to_csv(file_path, index=False)
    print(f"Heatwave data saved to {file_path}")
except Exception as e:
    print("Error downloading heatwave data:", e)
