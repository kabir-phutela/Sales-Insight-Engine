import pandas as pd
import numpy as np
import sys
import os
import joblib

# -------------------
# Validate input arguments
# -------------------
if len(sys.argv) != 3:
    print("Usage: python models/predict_model.py <input_csv> <output_csv>")
    sys.exit(1)

input_csv = sys.argv[1]
output_csv = sys.argv[2]

print("📂 Loading dataset...")
df = pd.read_csv(input_csv, parse_dates=["date"])

# -------------------
# Drop rows with missing essential features
# -------------------
required_cols = [
    "product_id", "product_name", "area", "date",
    "temp", "humidity", "wind_speed",
    "weather_main", "weather_desc", "name"
]
df.dropna(subset=required_cols, inplace=True)

print("⚙️ Feature engineering...")
df["sales_lag_1"] = df.get("sales_lag_1", 0)
df["day_of_week"] = df["date"].dt.weekday
df["month"] = df["date"].dt.month
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# -------------------
# Load Model & Encoder
# -------------------
print("📦 Loading model and encoder...")
encoder = joblib.load("models/encoder.joblib")
model = joblib.load("models/xgboost_model.joblib")

categorical_cols = ["product_id", "product_name", "area", "weather_main", "weather_desc", "name"]
numerical_cols = ["temp", "humidity", "wind_speed", "sales_lag_1", "day_of_week", "month", "is_weekend"]

# Encode categorical
encoded_cats = encoder.transform(df[categorical_cols])
X = np.hstack([encoded_cats, df[numerical_cols].values])

# -------------------
# Predict
# -------------------
print("🤖 Generating predictions...")
df["predicted_sales"] = model.predict(X)

# -------------------
# Save to CSV
# -------------------
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
df.to_csv(output_csv, index=False)
print(f"✅ Predictions saved to CSV: {output_csv}")
