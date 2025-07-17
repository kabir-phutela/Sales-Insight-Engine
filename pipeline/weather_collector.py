import pandas as pd
import random
from datetime import datetime, timedelta
import os

# ----------------------------------------
# 🗓️ Configuration
# ----------------------------------------

cities = ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru"]

start_date = datetime(2025, 6, 27)
end_date = datetime(2025, 9, 30)

# ----------------------------------------
# 🌤️ Simulate Weather Data
# ----------------------------------------

def simulate_weather_data():
    weather_data = []

    date = start_date
    while date <= end_date:
        for city in cities:
            weather_data.append({
                "city": city,
                "date": date.strftime("%Y-%m-%d"),
                "temp": round(random.uniform(20, 40), 2),
                "humidity": random.randint(40, 90),
                "weather_main": random.choice(["Clouds", "Rain", "Clear"]),
                "weather_desc": random.choice([
                    "scattered clouds",
                    "light rain",
                    "moderate rain",
                    "overcast clouds",
                    "clear sky"
                ]),
                "wind_speed": round(random.uniform(1, 10), 2)
            })
        date += timedelta(days=1)

    df = pd.DataFrame(weather_data)

    # Save to data/raw
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/weather_data.csv", index=False)

    print(f"✅ Simulated weather data saved to data/raw/weather_data.csv")
    print(df.head())

    return df

# ----------------------------------------
# ▶ Run Script
# ----------------------------------------

if __name__ == "__main__":
    simulate_weather_data()
