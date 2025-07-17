import os
import sys
import requests
import pandas as pd
from datetime import datetime

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.api_keys import CALENDARIFIC_API_KEY  # Ensure this exists

def fetch_holidays(country="IN", year=None):
    """
    Fetches public holidays for the specified country and year using Calendarific API.
    """
    if year is None:
        year = datetime.now().year

    print(f"🔍 Fetching holidays for {country} in {year}...")

    url = (
        f"https://calendarific.com/api/v2/holidays"
        f"?api_key={CALENDARIFIC_API_KEY}"
        f"&country={country}"
        f"&year={year}"
    )

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ API error: {response.status_code}")
            return

        data = response.json()

        if "response" not in data or "holidays" not in data["response"]:
            print("⚠️ No holidays found in API response.")
            return

        holidays = []
        for item in data["response"]["holidays"]:
            holidays.append({
                "date": item["date"]["iso"],
                "name": item["name"],
                "description": item.get("description", ""),
                "type": ", ".join(item.get("type", []))
            })

        if not holidays:
            print("⚠️ No holidays data extracted.")
            return

        df = pd.DataFrame(holidays)

        # Confirm DataFrame is not empty before saving
        if df.empty:
            print("⚠️ DataFrame is empty. Nothing to save.")
        else:
            os.makedirs("data/raw", exist_ok=True)
            df.to_csv("data/raw/holiday_data.csv", index=False, encoding="utf-8-sig")
            print("✅ Holiday data saved to data/raw/holiday_data.csv")
            print(df.head())

        return df

    except Exception as e:
        print(f"❌ Error fetching holidays: {e}")


# If run as a script
if __name__ == "__main__":
    fetch_holidays()
