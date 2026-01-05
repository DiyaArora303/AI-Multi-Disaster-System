import pandas as pd
import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# -------------------------
# Paths
# -------------------------
processed_file = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\cyclones.csv"
model_save_path = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\ml_models\cyclone\cyclone_model.h5"
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(processed_file, low_memory=False)

# Keep only rows where LAT and LON are numeric
df = df[pd.to_numeric(df['LAT'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['LON'], errors='coerce').notnull()]

# Convert columns to float
df['LAT'] = df['LAT'].astype(np.float32)
df['LON'] = df['LON'].astype(np.float32)

# -------------------------
# Create sequences for LSTM
# -------------------------
def create_sequences(data, seq_length=3):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

data = df[['LAT', 'LON']].values
X, y = create_sequences(data)

# -------------------------
# Build LSTM model
# -------------------------
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(2))  # predict LAT and LON
model.compile(optimizer='adam', loss='mse')

# -------------------------
# Train model
# -------------------------
model.fit(X, y, epochs=10, batch_size=64, verbose=1)

# Save model
model.save(model_save_path)
print(f"Cyclone LSTM model saved at {model_save_path}")
