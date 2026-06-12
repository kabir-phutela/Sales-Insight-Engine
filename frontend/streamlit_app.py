import streamlit as st
import requests
from datetime import datetime

st.title("📈 Sales Insight Engine")

with st.form("prediction_form"):
    product_id = st.selectbox("Product ID", ["P001", "P002", "P003"])
    product_name = st.selectbox("Product Name", ["Soft Drink", "Gift Hamper","Moisturizer","Pooja Articles","Sweets"])
    area = st.selectbox("Area", ["Bathinda", "Patiala","Malout","Mohali","Rajpura"])
    date = st.date_input("Date")
    temp = st.number_input("Temperature (°C)", value=25.0)
    humidity = st.number_input("Humidity (%)", value=50.0)
    wind_speed = st.number_input("Wind Speed", value=5.0)
    weather_main = st.selectbox("Weather Main", ["Clear", "Clouds", "Rain"])
    weather_desc = st.selectbox("Weather Description", ["clear sky", "few clouds", "light rain"])
    holiday_name = st.selectbox("Holiday Name", [
        "None",
        "New Year's Day",
        "Republic Day",
        "Independence Day",
        "Diwali",
        "Christmas"
    ])
    sales_lag_1 = st.number_input("Previous Day Sales (lag 1)", value=0)

    submitted = st.form_submit_button("Predict")

if submitted:
    payload = {
        "product_id": product_id,
        "product_name": product_name,
        "area": area,
        "date": date.strftime("%Y-%m-%d"),
        "temp": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "weather_main": weather_main,
        "weather_desc": weather_desc,
        "name": holiday_name,
        "sales_lag_1": sales_lag_1
    }

    try:
        response = requests.post("http://localhost:5000/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success(f"Predicted Sales: {data['predicted_sales']:.2f}")
            st.info(data.get("message"))
        else:
            st.error(f"API Error: {response.json().get('error')}")
    except Exception as e:
        st.error(f"Failed to connect to API: {e}")
