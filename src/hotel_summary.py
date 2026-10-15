
from pathlib import Path
import pandas as pd

input_file = Path("data/processed/hotel_review_analysis.csv")
output_file = Path("data/processed/hotel_summary.csv")

df = pd.read_csv(input_file)

# Create one row per hotel
summary = (
    df.groupby(["hotel_name", "location"], dropna=False)
    .agg(
        rating=("rating", "first"),
        review_score=("review_score", "first"),
        room_score=("room_score", "first"),
        price_booking=("price_booking", "first"),
        price_tripadvisor=("price_tripadvisor", "first"),
        review_count_booking=("review_count_booking", "first"),
        review_count_tripadvisor=("review_count_tripadvisor", "first"),
        reviews_analyzed=("review_text", "count"),
        avg_sentiment=("sentiment_score", "mean"),
        positive_reviews=("sentiment", lambda x: (x == "Positive").sum()),
        neutral_reviews=("sentiment", lambda x: (x == "Neutral").sum()),
        negative_reviews=("sentiment", lambda x: (x == "Negative").sum()),
        staff_service_mentions=("staff_service", "sum"),
        cleanliness_mentions=("cleanliness", "sum"),
        room_comfort_mentions=("room_comfort", "sum"),
        location_beach_mentions=("location_beach", "sum"),
        food_dining_mentions=("food_dining", "sum"),
        value_for_money_mentions=("value_for_money", "sum"),
    )
    .reset_index()
)

summary["positive_review_pct"] = (
    summary["positive_reviews"]
    / summary["reviews_analyzed"].replace(0, pd.NA)
    * 100
).round(1)

summary["negative_review_pct"] = (
    summary["negative_reviews"]
    / summary["reviews_analyzed"].replace(0, pd.NA)
    * 100
).round(1)

summary["avg_sentiment"] = summary["avg_sentiment"].round(3)

summary.to_csv(output_file, index=False)

print(f"Hotels summarized: {len(summary)}")
print(f"Saved to: {output_file}")

print("\nTop hotels by average sentiment:")
print(
    summary.sort_values("avg_sentiment", ascending=False)[
        ["hotel_name", "avg_sentiment", "reviews_analyzed", "positive_review_pct"]
    ].head(10).to_string(index=False)
)
