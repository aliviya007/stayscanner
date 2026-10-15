
from pathlib import Path

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

input_file = Path("data/processed/hotel_data_cleaned.csv")
output_file = Path("data/processed/hotel_review_analysis.csv")

df = pd.read_csv(input_file)

# Keep reviews that contain text
df["review_text"] = df["review_text"].fillna("").astype(str).str.strip()
reviews = df[df["review_text"] != ""].copy()


# Calculate sentiment scores
analyzer = SentimentIntensityAnalyzer()

reviews["sentiment_score"] = reviews["review_text"].apply(
    lambda text: analyzer.polarity_scores(text)["compound"]
)

def classify_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    return "Neutral"

reviews["sentiment"] = reviews["sentiment_score"].apply(
    classify_sentiment
)

# Identify topics mentioned in reviews
topics = {
    "Staff & Service": [
        "staff", "service", "friendly", "helpful", "reception"
    ],
    "Cleanliness": [
        "clean", "dirty", "filthy", "hygiene", "smell", "stinks"
    ],
    "Room & Comfort": [
        "room", "bed", "mattress", "air conditioning", "air-conditioning"
    ],
    "Location & Beach": [
        "location", "beach", "sea", "view", "mountain"
    ],
    "Food & Dining": [
        "food", "breakfast", "restaurant", "dinner", "meal"
    ],
    "Value for Money": [
        "price", "money", "expensive", "cheap", "value", "waste"
    ],
}

for topic, keywords in topics.items():
    column = (
        topic.lower()
        .replace(" & ", "_")
        .replace(" ", "_")
    )

    reviews[column] = reviews["review_text"].apply(
        lambda text: int(
            any(keyword in text.lower() for keyword in keywords)
        )
    )

# Display topic frequency
topic_columns = [
    topic.lower().replace(" & ", "_").replace(" ", "_")
    for topic in topics
]

print("\nReviews mentioning each topic:")
print(reviews[topic_columns].sum().sort_values(ascending=False))

# Analyse sentiment for each topic
print("\nSentiment by topic:")

for topic in topics:
    column = topic.lower().replace(" & ", "_").replace(" ", "_")
    topic_reviews = reviews[reviews[column] == 1]

    print(f"\n{topic} ({len(topic_reviews)} reviews)")
    print(topic_reviews["sentiment"].value_counts().to_string())


# Save results
reviews.to_csv(output_file, index=False)

print(f"Unique reviews analysed: {len(reviews)}")
print("\nSentiment distribution:")
print(reviews["sentiment"].value_counts())

print(f"\nSaved results to: {output_file}")
print("\nSample results:")
print(
    reviews[["hotel_name", "sentiment_score", "sentiment"]]
    .head(10)
    .to_string(index=False)
)