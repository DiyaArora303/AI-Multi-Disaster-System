import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os

# -------------------------
# Paths
# -------------------------
processed_file = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\heatwave_processed.csv"
model_path = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\ml_models\heatwave\heatwave_model.pkl"
scaler_path = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\ml_models\heatwave\heatwave_scaler.pkl"
os.makedirs(os.path.dirname(model_path), exist_ok=True)
os.makedirs(os.path.dirname(scaler_path), exist_ok=True)

# -------------------------
# Load data
# -------------------------
df = pd.read_csv(processed_file)
X = df[['tmax']].values
y = df['anomaly'].values

# -------------------------
# Scale features
# -------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, scaler_path)

# -------------------------
# Train/test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# -------------------------
# Train model
# -------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -------------------------
# Save model
# -------------------------
joblib.dump(model, model_path)
print(f"Heatwave model and scaler saved at {model_path} and {scaler_path}")
