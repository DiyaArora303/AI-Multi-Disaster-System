import pandas as pd
import os

def preprocess_heatwave_input():
    raw_file = "data_pipeline/raw/heatwave.csv"
    processed_file = "data_pipeline/processed/heatwave_processed.csv"
    os.makedirs(os.path.dirname(processed_file), exist_ok=True)

    df = pd.read_csv(raw_file, parse_dates=['date'])
    df['anomaly'] = df['tmax'] - df['tmax'].rolling(window=7, min_periods=1).mean()
    df[['tmax', 'anomaly']].to_csv(processed_file, index=False)
    print(f"Processed heatwave data saved at {processed_file}")

if __name__ == "__main__":
    preprocess_heatwave_input()
