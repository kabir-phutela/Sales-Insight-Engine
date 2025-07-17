from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

# Load trained model and encoder
model = joblib.load("models/xgboost_model.joblib")
encoder = joblib.load("models/encoders.joblib")

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Sales Prediction API is running!"

@app.route("/predict", methods=["GET","POST"])
def predict():
    data = request.json

    # Check required fields
    required_fields = [
        "product_id",
        "product_name",
        "area",
        "weather_main",
        "weather_desc",
        "name",
        "date",
        "temp",
        "humidity",
        "wind_speed",
        "Festival",
        "Shopping",
        "sales_lag_1"
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    # Convert date
    date = pd.to_datetime(data["date"])
    day_of_week = date.weekday()
    month = date.month
    is_weekend = int(day_of_week in [5, 6])

    # Create dataframe for encoder
    cat_df = pd.DataFrame([{
        "product_id": str(data["product_id"]),
        "product_name": str(data["product_name"]),
        "area": str(data["area"]),
        "weather_main": str(data["weather_main"]),
        "weather_desc": str(data["weather_desc"]),
        "name": str(data["name"])
    }])

    # Encode categorical
    encoded_cats = encoder.transform(cat_df)

    # Numerical features
    num_features = np.array([[
        data["temp"],
        data["humidity"],
        data["wind_speed"],
        data["Festival"],
        data["Shopping"],
        data["sales_lag_1"],
        day_of_week,
        month,
        is_weekend
    ]])

    # Concatenate
    X_input = np.hstack([encoded_cats, num_features])

    # Predict
    pred = model.predict(X_input)[0]

    return jsonify({"predicted_sales": float(pred)})

if __name__ == "__main__":
    app.run(debug=True)
