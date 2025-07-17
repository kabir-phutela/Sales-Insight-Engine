import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="📈 Product Stock Prediction", layout="centered")

st.title("🛒 SALES INSIGHT ENGINE")

# --- Input fields ---
with st.form("prediction_form"):
    st.subheader("Enter Details:")

    product_id = st.text_input("Product ID", "1")
    product_name = st.text_input("Product Name", "Soft Drink")
    area = st.selectbox("Area", ["Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai"])
    date_input = st.date_input("Date", date.today())
    temp = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
    wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=20.0, value=3.0)
    weather_main = st.text_input("Weather Main", "Clear")
    weather_desc = st.text_input("Weather Description", "scattered clouds")
    holiday_name = st.text_input("Holiday/Festival Name", "Rath Yatra")
    festival_score = st.slider("Festival Score", 0, 100, 50)
    shopping_score = st.slider("Shopping Score", 0, 100, 50)
    sales_lag_1 = st.number_input("Previous Day Sales", min_value=0.0, value=100.0)

    submitted = st.form_submit_button("Predict Sales")

# --- Predict ---
if submitted:
    # Prepare data
    payload = {
        "product_id": product_id,
        "product_name": product_name,
        "area": area,
        "date": date_input.strftime("%Y-%m-%d"),
        "temp": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "weather_main": weather_main,
        "weather_desc": weather_desc,
        "name": holiday_name,
        "Festival": festival_score,
        "Shopping": shopping_score,
        "sales_lag_1": sales_lag_1
    }

    try:
        # Call API
        response = requests.post("http://127.0.0.1:5000/predict", json=payload)

        if response.status_code == 200:
            prediction = response.json()["predicted_sales"]
            st.success(f"✅ Predicted Sales: **{prediction:.2f} units**")
        else:
            st.error(f"❌ Error {response.status_code}: {response.text}")

    except Exception as e:
        st.error(f"Request failed: {e}")
