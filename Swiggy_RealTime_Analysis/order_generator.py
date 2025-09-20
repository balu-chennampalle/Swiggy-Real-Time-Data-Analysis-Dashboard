import pandas as pd
import random
import time
from datetime import datetime
import os

# Load Cleaned Zomato dataset
file = "zomato.csv"
df = pd.read_csv(file, encoding="utf-8")

# Extract unique lists
restaurants = df["name"].dropna().unique().tolist()
cuisines = df["cuisines"].dropna().unique().tolist()
locations = df["location"].dropna().unique().tolist()

# Excel output file
excel_file = "orders.xlsx"

# Create empty Excel file if it doesn't exist
if not os.path.exists(excel_file):
    orders_df = pd.DataFrame(columns=["order_id","restaurant","cuisine","location","price","delivery_time","rating","timestamp"])
    orders_df.to_excel(excel_file, index=False)

order_id = 1
print("🚀 Real-time order generator started... (Press CTRL+C to stop)")

while True:
    # Generate random number of orders per minute (e.g., 5 to 15)
    num_orders = random.randint(5, 15)
    orders = []

    for _ in range(num_orders):
        order = {
            "order_id": order_id,
            "restaurant": random.choice(restaurants),
            "cuisine": random.choice(cuisines),
            "location": random.choice(locations),
            "price": random.randint(150, 800),
            "delivery_time": random.randint(20, 60),
            "rating": random.randint(1, 5),
            "time": datetime.now().strftime("%H:%M")  # only hour and minute
        }
        orders.append(order)
        order_id += 1

    # Append to Excel efficiently
    new_orders_df = pd.DataFrame(orders)
    if os.path.exists(excel_file):
        with pd.ExcelWriter(excel_file, mode="a", if_sheet_exists="overlay", engine="openpyxl") as writer:
            # Read existing data
            existing_df = pd.read_excel(excel_file)
            combined_df = pd.concat([existing_df, new_orders_df], ignore_index=True)
            combined_df.to_excel(writer, index=False)
    else:
        new_orders_df.to_excel(excel_file, index=False)

    print(f"✅ {num_orders} new orders added at {datetime.now().strftime('%H:%M')}")

    # Wait 1 minute before next batch
    time.sleep(60)
