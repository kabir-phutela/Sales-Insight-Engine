import os
import sys
import pandas as pd
import time
from pytrends.request import TrendReq

def fetch_trends():
    # Initialize Pytrends connection
    pytrends = TrendReq(hl="en-US", tz=330)

    # Keep it minimal to avoid 429 errors
    keywords = ["Festival"]   # You can later add more
    timeframe = "today 3-m"   # Past 3 months
    geo = "IN"                # India

    print(f"🔍 Fetching trends for keywords: {keywords}")

    # Wait to avoid rate limits
    time.sleep(5)

    # Create payload (search parameters)
    pytrends.build_payload(
        kw_list=keywords,
        timeframe=timeframe,
        geo=geo
    )

    # Download interest over time data
    df = pytrends.interest_over_time()

    # Clean DataFrame
    df = df.reset_index()
    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    # Create directory if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)

    # Save to CSV
    df.to_csv("data/raw/trend_data.csv", index=False)

    print("✅ Trend data saved to data/raw/trend_data.csv")
    print(df.head())

    return df

if __name__ == "__main__":
    fetch_trends()
