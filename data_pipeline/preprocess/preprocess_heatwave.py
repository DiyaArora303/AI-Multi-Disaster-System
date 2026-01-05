import pandas as pd
import os

raw_file = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\raw\heatwave.csv"
processed_file = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\heatwave_processed.csv"

os.makedirs(os.path.dirname(processed_file), exist_ok=True)

# Load raw data
df = pd.read_csv(raw_file, parse_dates=['date'])

# Compute anomaly relative to rolling 7-day average
df['anomaly'] = df['tmax'] - df['tmax'].rolling(window=7, min_periods=1).mean()

# Save processed CSV
df[['tmax', 'anomaly']].to_csv(processed_file, index=False)
print(f"Processed heatwave data saved at {processed_file}")
