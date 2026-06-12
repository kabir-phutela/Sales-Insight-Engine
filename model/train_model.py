import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error


script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "processed", "merged_dataset.csv")
model_dir = os.path.join(script_dir, "..", "models")
os.makedirs(model_dir, exist_ok=True)


if not os.path.exists(data_path):
    raise FileNotFoundError(f"CSV file not found at {data_path}")

df = pd.read_csv(data_path, parse_dates=["date"])

# Feature Engineering

df = df.sort_values(["product_id", "date"])

# Lag feature
df["sales_lag_1"] = df.groupby("product_id")["sales"].shift(1)
df["sales_lag_1"] = df["sales_lag_1"].fillna(0)

# Date features
df["day_of_week"] = df["date"].dt.weekday
df["month"] = df["date"].dt.month
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# -------------------
# Target
# -------------------
y = df["sales"]

# -------------------
# Features
# -------------------
categorical_cols = [
    "product_id",
    "product_name",
    "area",
    "weather_main",
    "weather_desc",
    "name"
]

numerical_cols = [
    "temp",
    "humidity",
    "wind_speed",
    "sales_lag_1",
    "day_of_week",
    "month",
    "is_weekend"
]

# -------------------
# Encoding
# -------------------
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded_cats = encoder.fit_transform(df[categorical_cols])
encoded_cat_cols = encoder.get_feature_names_out(categorical_cols)

# Combine features
X = np.hstack([encoded_cats, df[numerical_cols].values])

# -------------------
# Train/Test Split
# -------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------
# Train Model
# -------------------
model = XGBRegressor(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    random_state=42,
    objective="reg:squarederror"
)

model.fit(X_train, y_train)

# -------------------
# Evaluate
# -------------------
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # Safe for all sklearn versions
print(f"✅ Model trained. RMSE: {rmse:.2f}")

# -------------------
# Save Model & Encoder
# -------------------
joblib.dump(model, os.path.join(model_dir, "xgboost_model.joblib"))
joblib.dump(encoder, os.path.join(model_dir, "encoder.joblib"))

# -------------------
# Feature Importances
# -------------------
feature_names = list(encoded_cat_cols) + numerical_cols
importances = model.feature_importances_
importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print("\n top 10 Most Important Features:")
print(importance_df.head(10))
