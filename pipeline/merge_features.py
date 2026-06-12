import os
import pandas as pd

# Make sure paths are relative to this script's folder
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def merge_data():
    print("Loading datasets.")

    # Paths to all raw data files
    sales_path = os.path.join(BASE_DIR, "data", "raw", "internal_sales.csv")
    weather_path = os.path.join(BASE_DIR, "data", "raw", "weather_data.csv")
    holiday_path = os.path.join(BASE_DIR, "data", "raw", "holiday_data.csv")



    print("Checking files:")
    for path in [sales_path, weather_path, holiday_path]:
        print(f"  {path} -> Exists: {os.path.exists(path)}")

    # Load CSVs
    sales_df = pd.read_csv(sales_path, parse_dates=["date"])
    weather_df = pd.read_csv(weather_path, parse_dates=["date"])
    holiday_df = pd.read_csv(holiday_path, parse_dates=["date"])

    print("Datasets loaded successfully.")

    # Convert dates
    sales_df["date"] = pd.to_datetime(sales_df["date"], errors="coerce")
    weather_df["date"] = pd.to_datetime(weather_df["date"], errors="coerce")
    holiday_df["date"] = pd.to_datetime(holiday_df["date"], errors="coerce")


    # Merge sales + weather
    merged_df = pd.merge(
        sales_df,
        weather_df,
        left_on=["date", "area"],
        right_on=["date", "city"],
        how="left"
    )

    # Merge holiday data
    merged_df = pd.merge(
        merged_df,
        holiday_df[["date", "name"]],
        on="date",
        how="left"
    )



    # Drop redundant city column
    if "city" in merged_df.columns:
        merged_df.drop(columns="city", inplace=True)

    # Sort by date so forward-fill works
    merged_df = merged_df.sort_values("date")



    # Fill other missing numeric data
    merged_df.fillna({
        "temp": 0,
        "humidity": 0,
        "wind_speed": 0,
        "Festival": 0,
        "Shopping": 0
    }, inplace=True)

    # Fill missing text data
    merged_df["weather_main"].fillna("Unknown", inplace=True)
    merged_df["weather_desc"].fillna("Unknown", inplace=True)
    merged_df["name"].fillna("None", inplace=True)

    # Save merged dataset
    output_dir = os.path.join(BASE_DIR, "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "merged_dataset.csv")
    merged_df.to_csv(output_path, index=False)

    print(f"Merged dataset saved to {output_path}")

    return merged_df


if __name__ == "__main__":
    df = merge_data()
    print(df.head())
