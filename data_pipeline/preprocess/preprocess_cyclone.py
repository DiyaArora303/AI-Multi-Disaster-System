import pandas as pd
import os

# -------------------------
# File paths
# -------------------------
raw_file = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\raw\cyclones.csv"
processed_file = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\cyclones.csv"

# Ensure processed folder exists
os.makedirs(os.path.dirname(processed_file), exist_ok=True)

# -------------------------
# Load raw CSV
# -------------------------
df = pd.read_csv(raw_file, low_memory=False)

# -------------------------
# Keep only useful columns
# Update column names to match your CSV
# -------------------------
columns_to_keep = ['NAME', 'ISO_TIME', 'LAT', 'LON', 'WMO_WIND', 'WMO_PRES']
df = df[columns_to_keep]

# -------------------------
# Save processed CSV
# -------------------------
df.to_csv(processed_file, index=False)
print(f"Processed cyclone data saved to {processed_file}")
