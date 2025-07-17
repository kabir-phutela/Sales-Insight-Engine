import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Load merged dataset
data_path = os.path.join("data", "processed", "merged_dataset.csv")
df = pd.read_csv(data_path, parse_dates=["date"])

# --- Feature Engineering ---

# Lag feature: previous day's sales (optional)
df = df.sort_values(["product_id", "date"])
df["sales_lag_1"] = df.groupby("product_id")["sales"].shift(1)

# Date-based features
df["day_of_week"] = df["date"].dt.weekday
df["month"] = df["date"].dt.month
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

# Fill missing lag with 0
df["sales_lag_1"].fillna(0, inplace=True)

# Define target
y = df["sales"]

# Categorical columns
categorical_cols = [
    "product_id",
    "product_name",
    "area",
    "weather_main",
    "weather_desc",
    "name"
]

# Numerical columns
numerical_cols = [
    "temp",
    "humidity",
    "wind_speed",
    "Festival",
    "Shopping",
    "sales_lag_1",
    "day_of_week",
    "month",
    "is_weekend"
]

# Encode categorical columns
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded_cats = encoder.fit_transform(df[categorical_cols])
encoded_cat_cols = encoder.get_feature_names_out(categorical_cols)

# Combine encoded categorical and numerical
X = np.hstack([encoded_cats, df[numerical_cols].values])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred) ** 0.5

print(f"✅ Model trained. RMSE: {rmse:.2f}")

# Save model and encoder
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/xgboost_model.joblib")
joblib.dump(encoder, "models/encoders.joblib")

# Show feature importances
importances = model.feature_importances_
feature_names = list(encoded_cat_cols) + numerical_cols
importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

print("\n🔹 Top 10 Most Important Features:")
print(importance_df.head(10))
