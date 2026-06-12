from flask import Flask, request, jsonify,send_from_directory,Response
import joblib
import numpy as np
import pandas as pd
import os
from datetime import date

app = Flask(__name__)


# Load model & encoder

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "..", "models", "xgboost_model.joblib")
encoder_path = os.path.join(script_dir, "..", "models", "encoder.joblib")

print("Loading model from:", model_path)
print("Loading encoder from:", encoder_path)

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)

@app.route("/google13edae5904ab576e.html")
def google_verification():
    return send_from_directory(".", "google13edae5904ab576e.html")

# Predict route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print("Received JSON:", data)

        # ------------------------
        # Required fields
        # ------------------------
        required_fields = [
            "product_id", "product_name", "area",
            "weather_main", "weather_desc", "name",
            "date", "temp", "humidity", "wind_speed",
            "sales_lag_1"
        ]
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        # ------------------------
        # Feature engineering
        # ------------------------
        date = pd.to_datetime(data["date"])
        day_of_week = date.weekday()
        month = date.month
        is_weekend = int(day_of_week in [5, 6])

        # ------------------------
        # Categorical encoding
        # ------------------------
        cat_df = pd.DataFrame([{
            "product_id": str(data["product_id"]),
            "product_name": str(data["product_name"]),
            "area": str(data["area"]),
            "weather_main": str(data["weather_main"]),
            "weather_desc": str(data["weather_desc"]),
            "name": str(data["name"])
        }])

        encoded_cats = encoder.transform(cat_df)
        if hasattr(encoded_cats, "toarray"):
            encoded_cats = encoded_cats.toarray()

        # ------------------------
        # Numerical features
        # ------------------------
        num_features = np.array([[
            data["temp"],
            data["humidity"],
            data["wind_speed"],
            data["sales_lag_1"],
            day_of_week,
            month,
            is_weekend
        ]])

        # Combine features
        X_input = np.hstack([encoded_cats, num_features])

        # ------------------------
        # Prediction
        # ------------------------
        pred = model.predict(X_input)[0]
        print("Predicted sales:", pred)

        # ------------------------
        # Save input + prediction
        # ------------------------
        save_data = {
            **data,
            "day_of_week": day_of_week,
            "month": month,
            "is_weekend": is_weekend,
            "predicted_sales": float(pred)
        }
        df_save = pd.DataFrame([save_data])
        print("Data to save:\n", df_save)

        save_dir = os.path.join(script_dir, "..", "data", "new_inputs")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, "user_inputs.csv")
        print("Saving to CSV:", save_path)

        if not os.path.exists(save_path):
            df_save.to_csv(save_path, index=False)
        else:
            df_save.to_csv(save_path, mode="a", header=False, index=False)

        return jsonify({
            "predicted_sales": float(pred),
            "message": "Prediction successful and input saved for retraining"
        })

    except Exception as e:
        print("Error during prediction:", e)
        return jsonify({"error": str(e)}), 500

# Home route

@app.route("/")
def home():
    return "Sales Prediction API is running!"


@app.route("/sitemap.xml", methods=["GET"])
def sitemap():
    """
    Dynamically generates sitemap.xml
    """

    # Routes we never want Google to index
    excluded_prefixes = [
        "/api",
        "/admin",
        "/login",
        "/logout",
        "/register",
        "/debug",
        "/static"
    ]

    pages = []

    for rule in app.url_map.iter_rules():

        # Only GET routes
        if "GET" not in rule.methods:
            continue

        # Ignore Flask internal/static routes
        if rule.endpoint == "static":
            continue

        # Ignore dynamic routes like /user/<id>
        if "<" in rule.rule:
            continue

        # Ignore unwanted prefixes
        if any(rule.rule.startswith(prefix) for prefix in excluded_prefixes):
            continue

        pages.append(rule.rule)

    pages = sorted(set(pages))

    today = date.today().isoformat()

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:

        url = request.host_url.rstrip("/") + page

        xml.append("  <url>")
        xml.append(f"      <loc>{url}</loc>")
        xml.append(f"      <lastmod>{today}</lastmod>")
        xml.append("      <changefreq>weekly</changefreq>")
        xml.append("      <priority>0.8</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")

    return Response(
        "\n".join(xml),
        mimetype="application/xml"
    )    

@app.route("/robots.txt", methods=["GET"])
def robots():

    robots_txt = f"""
User-agent: *
Disallow: /api/
Disallow: /admin/
Disallow: /login/
Disallow: /logout/

Allow: /

Sitemap: https://sales-insight-engine.onrender.com/sitemap.xml
"""

    return Response(
        robots_txt,
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
