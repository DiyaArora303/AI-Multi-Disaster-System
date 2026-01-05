import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os

# -------------------------
# Paths
# -------------------------
processed_eq_csv = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\earthquakes.csv"
model_save_path = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\ml_models\earthquake\eq_model.pkl"

os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

# -------------------------
# Load preprocessed data
# -------------------------
df = pd.read_csv(processed_eq_csv)

# -------------------------
# Remove rows with NaNs
# -------------------------
df = df.dropna(subset=['longitude', 'latitude', 'depth', 'magnitude'])

# Features: longitude, latitude, depth
X = df[['longitude', 'latitude', 'depth']]
# Target: magnitude
y = df['magnitude']

# -------------------------
# Split into training/testing
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------
# Train Random Forest model
# -------------------------
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# -------------------------
# Evaluate model
# -------------------------
y_pred = rf.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Model trained! MSE: {mse:.3f}, R2 Score: {r2:.3f}")

# -------------------------
# Save model using pickle (Python 3.11 compatible)
# -------------------------
with open(model_save_path, "wb") as f:
    pickle.dump(rf, f)

print(f"Trained Earthquake model saved at {model_save_path}")
