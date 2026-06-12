import pandas as pd
import random
from datetime import datetime, timedelta
import os


products = [
    {"product_id": "P001", "product_name": "Soft Drink "},
    {"product_id": "P002", "product_name": "Sweets "},
    {"product_id": "P003", "product_name": "Moisturizer "},
    {"product_id": "P004", "product_name": "Pooja Articles"},
    {"product_id": "P005", "product_name": "Gift Hamper"}
]

cities = ["Bathinda", "Malout", "Mohali", "Rajpura", "Patiala"]

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 9, 30)  # 9 months


def generate_sales_data():
    all_data = []

    date = start_date
    while date <= end_date:
        for product in products:
            for city in cities:
                # Define product-based seasonal effects
                if product["product_name"] == "Soft Drink ":
                    base_sales = 250 if date.month in [7, 8] else 180
                elif product["product_name"] == "Sweets ":
                    base_sales = 200 if date.month == 8 else 120
                elif product["product_name"] == "Moisturizer ":
                    base_sales = 100 if date.month == 9 else 60
                elif product["product_name"] == "Pooja Articles":
                    base_sales = 180 if date.month in [7, 8] else 150
                elif product["product_name"] == "Gift Hamper":
                    base_sales = 220
                else:
                    base_sales = 100

                # Add random noise to simulate real-world variance
                noise = random.gauss(0, 25)  # Mean=0, SD=25
                sales = max(0, int(base_sales + noise))  # No negative sales

                all_data.append({
                    "product_id": product["product_id"],
                    "product_name": product["product_name"],
                    "area": city,
                    "date": date.strftime("%Y-%m-%d"),
                    "sales": sales
                })

        date += timedelta(days=1)

    df = pd.DataFrame(all_data)

    # Ensure output folder exists
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/internal_sales.csv", index=False)
    print(f"Generated {len(df)} rows of synthetic sales data.")
    print("Saved to: data/raw/internal_sales.csv")

if __name__ == "__main__":
    generate_sales_data()
