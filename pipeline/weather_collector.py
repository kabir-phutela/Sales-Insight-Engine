import pandas as pd
import random
from datetime import datetime, timedelta
import os

cities = ["Bathinda", "Malout", "Mohali", "Rajpura", "Patiala"]

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 9, 30)


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

    # Ensure directory exists
    save_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/raw/weather_data.csv"))
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    df.to_csv(save_path, index=False)

    print(f"✅ Simulated weather data saved at: {save_path}")
    print("Unique cities in data:", df["city"].unique())
    print(df.head())

    return df


if __name__ == "__main__":
    simulate_weather_data()
