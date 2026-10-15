import re
import pandas as pd


booking_file = "data/raw/booking_hotel.csv"
tripadvisor_file = "data/raw/tripadvisor_room.csv"
output_file = "data/processed/hotel_data_cleaned.csv"


booking = pd.read_csv(booking_file, encoding="latin1")
tripadvisor = pd.read_csv(tripadvisor_file, encoding="latin1")


# Clean column names
def clean_column_names(df):
    df.columns = (
        df.columns
        .str.replace("\xa0", " ", regex=False)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    return df


booking = clean_column_names(booking)
tripadvisor = clean_column_names(tripadvisor)


# Rename columns
booking = booking.rename(columns={
    "Hotel Name": "hotel_name",
    "Location": "location",
    "Rating": "rating",
    "Review Score": "review_score",
    "Number of": "review_count_booking",
    "Room Score": "room_score",
    "Room Type": "room_type",
    "Bed Type": "bed_type",
    "Room Price (in BDT or any other currency)": "price_booking"
})

tripadvisor = tripadvisor.rename(columns={
    "property name": "hotel_name",
    "Room Price (in BDT or any other currency)": "price_tripadvisor",
    "review_count": "review_count_tripadvisor",
    "Comment about room": "review_text"
})


def clean_hotel_name(name):
    if pd.isna(name):
        return None

    name = str(name)
    name = re.sub(r"^\s*\d+\.\s*", "", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def clean_number(value):
    if pd.isna(value):
        return None

    value = re.sub(r"[^\d.]", "", str(value))

    return float(value) if value else None


booking["hotel_name"] = booking["hotel_name"].apply(clean_hotel_name)
tripadvisor["hotel_name"] = tripadvisor["hotel_name"].apply(clean_hotel_name)

booking["price_booking"] = booking["price_booking"].apply(clean_number)
tripadvisor["price_tripadvisor"] = tripadvisor["price_tripadvisor"].apply(clean_number)

booking["review_count_booking"] = (
    booking["review_count_booking"]
    .apply(lambda x: int(clean_number(x)) if pd.notna(x) else None)
)

tripadvisor["review_count_tripadvisor"] = (
    tripadvisor["review_count_tripadvisor"]
    .apply(lambda x: int(clean_number(x)) if pd.notna(x) else None)
)


booking["rating"] = pd.to_numeric(
    booking["rating"],
    errors="coerce"
)

booking["room_score"] = pd.to_numeric(
    booking["room_score"],
    errors="coerce"
)


tripadvisor["review_text"] = (
    tripadvisor["review_text"]
    .fillna("")
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# Match hotels found in both datasets
merged = booking.merge(
    tripadvisor,
    on="hotel_name",
    how="inner"
)


merged.to_csv(output_file, index=False)


print(f"Booking rows: {len(booking)}")
print(f"TripAdvisor rows: {len(tripadvisor)}")
print(f"Matched hotels: {len(merged)}")
print(f"Saved cleaned data to: {output_file}")