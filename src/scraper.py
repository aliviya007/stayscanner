
import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = "https://hotel-example-site.takeyaqa.dev"
plans_url = f"{base_url}/data/en-US/plan_data.json"
page_url = f"{base_url}/en-US/plans.html"

# Fetch plans from the JSON endpoint
response = requests.get(plans_url, timeout=20)
response.raise_for_status()

plans = [
    plan for plan in response.json()
    if plan.get("id") != 0
]

# Extract the recommended plan from the HTML
html = requests.get(page_url, timeout=20)
html.raise_for_status()

soup = BeautifulSoup(html.text, "html.parser")
recommended = soup.select_one(".card-title")

if recommended:
    card = recommended.find_parent(class_="card")
    text = card.get_text(" ", strip=True) if card else ""

    price = re.search(r"\$([\d,.]+)", text)
    guests = re.search(r"at least (\d+) person", text, re.I)

    room_options = [
        "Standard twin room",
        "Premium twin room",
        "Single room",
    ]

    room = next(
        (
            option for option in room_options
            if option.lower() in text.lower()
        ),
        None
    )

    if not all([price, guests, room]):
        raise ValueError("Could not extract recommended plan details")

    plans.insert(0, {
        "id": 0,
        "name": recommended.get_text(strip=True),
        "roomBill": float(price.group(1).replace(",", "")),
        "minHeadCount": int(guests.group(1)),
        "maxHeadCount": None,
        "minTerm": None,
        "maxTerm": None,
        "room": room,
        "only": None,
    })
else:
    raise ValueError("Recommended plan not found on the page")

# Prepare the dataset
df = pd.DataFrame(plans)
df = df.drop(columns=["roomPage"], errors="ignore")

df = df.rename(columns={
    "id": "plan_id",
    "name": "plan_name",
    "roomBill": "price_per_guest",
    "minHeadCount": "minimum_guests",
    "maxHeadCount": "maximum_guests",
    "minTerm": "minimum_nights",
    "maxTerm": "maximum_nights",
    "room": "room_type",
    "only": "access_restriction",
})

df["source_url"] = page_url

# Validate before saving
if df["plan_id"].duplicated().any():
    raise ValueError("Duplicate plan IDs found!")

if df["plan_name"].isna().any() or df["price_per_guest"].isna().any():
    raise ValueError("Missing plan names or prices found!")

# Save the CSV
output = Path("data/raw/hotel_planisphere_plans.csv")
output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)

print(f"Saved {len(df)} unique plans to {output}")
print(
    df[["plan_id", "plan_name", "price_per_guest", "room_type"]]
    .to_string(index=False)
)
