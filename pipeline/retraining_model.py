# pipeline/retrain_model.py

import pandas as pd
import joblib
import os
from xgboost import XGBRegressor
from sklearn.preprocessing import OneHotEncoder
import numpy as np

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "..", "data", "new_inputs", "user_inputs.csv")
model_path = os.path.join(base_dir, "..", "models", "xgboost_model.joblib")
encoder_path = os.path.join(base_dir, "..", "models", "encoder.joblib")

# Load new training data
if not os.path.exists(data_path):
    print(f"No new data found at {data_path}. Skipping retraining.")
    exit()

df = pd.read_csv(data_path)

# ----------------------
# Prepare features
# ----------------------
cat_features = ["product_id", "product_name", "area", "weather_main", "weather_desc", "name"]
num_features = ["temp", "humidity", "wind_speed", "sales_lag_1", "day_of_week", "month", "is_weekend"]
target = "predicted_sales"  # or the actual sales column if available

# Encode categorical features
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
X_cat = encoder.fit_transform(df[cat_features])

# Numerical features
X_num = df[num_features].values

# Combine features
X = np.hstack([X_cat, X_num])
y = df[target].values

# Train new model
model = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1)
model.fit(X, y)

# Save model & encoder
os.makedirs(os.path.join(base_dir, "..", "models"), exist_ok=True)
joblib.dump(model, model_path)
joblib.dump(encoder, encoder_path)

print(f"Model retrained and saved at {model_path}")
print(f"Encoder saved at {encoder_path}")
