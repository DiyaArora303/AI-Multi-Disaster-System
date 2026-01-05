import pandas as pd
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Paths
processed_file = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\data_pipeline\processed\landslides.csv"
model_save_path = r"C:\Users\Lenovo\Desktop\AI-Multi-Disaster-System\ml_models\landslide\landslide_model.pkl"
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)

# Load data
df = pd.read_csv(processed_file)
X = df[['latitude', 'longitude']]
size_mapping = {'small': 0, 'medium': 1, 'large': 2}
y = df['landslide_size'].map(size_mapping)

X = X.fillna(0)
y = y.fillna(0)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
model = xgb.XGBRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Landslide model trained. MSE: {mse:.3f}")

# Save using joblib (safe for CPU and avoids bad allocation)
joblib.dump(model, model_save_path)
print(f"Landslide model saved at {model_save_path}")
