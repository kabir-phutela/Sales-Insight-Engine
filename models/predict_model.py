import pandas as pd
import numpy as np
import sys
import os
import joblib
from datetime import datetime

# Validate input arguments
if len(sys.argv) != 3:
    print("Usage: python models/predict_model.py <input_csv> <output_csv>")
    sys.exit(1)

input_csv = sys.argv[1]
output_csv = sys.argv[2]

print("🔹 Loading dataset...")
df = pd.read_csv(input_csv, parse_dates=["date"])

# Drop rows with missing essential features
required_cols = [
    "product_id", "product_name", "area", "date", "temp", "humidity", "wind_speed",
    "Festival", "Shopping", "weather_main", "weather_desc", "name"
]
df.dropna(subset=required_cols, inplace=True)

print("🔹 Feature engineering...")

# Optional: Handle missing or zero sales lag intelligently (we'll just fill with 0 here)
df["sales_lag_1"] = df.get("sales_lag_1", 0)

# Date-based features
df["day_of_week"] = df["date"].dt.weekday
df["month"] = df["date"].dt.month
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# Categorical columns (same as used in training)
categorical_cols = [
    "product_id", "product_name", "area", "weather_main", "weather_desc", "name"
]
numerical_cols = [
    "temp", "humidity", "wind_speed", "Festival", "Shopping",
    "sales_lag_1", "day_of_week", "month", "is_weekend"
]

print("🔹 Encoding categorical columns...")
# Load encoder and model
encoder = joblib.load("models/encoders.joblib")
model = joblib.load("models/xgboost_model.joblib")

# Encode categories
encoded_cats = encoder.transform(df[categorical_cols])
X = np.hstack([encoded_cats, df[numerical_cols].values])

print("🔹 Generating predictions...")
preds = model.predict(X)
df["predicted_sales"] = preds

print("✅ Predictions saved to:", output_csv)
df.to_csv(output_csv, index=False)
