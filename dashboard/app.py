
from pathlib import Path

import pandas as pd
import streamlit as st

# Page setup
st.set_page_config(
    page_title="StayScanner | Hotel Explorer",
    page_icon="🏨",
    layout="wide",
)

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "processed" / "hotel_data_cleaned.csv"
REVIEW_FILE = BASE_DIR / "data" / "processed" / "hotel_review_analysis.csv"


@st.cache_data
def load_data():
    hotels = pd.read_csv(DATA_FILE)
    reviews = pd.read_csv(REVIEW_FILE)
    return hotels, reviews


hotels, reviews = load_data()

# Header
st.title("🏨 StayScanner")
st.caption("Explore hotels, compare available prices, and understand guest reviews.")

# Sidebar filters
st.sidebar.header("Find your stay")

locations = sorted(hotels["location"].dropna().unique().tolist())
selected_locations = st.sidebar.multiselect(
    "Destination",
    options=locations,
    default=[],
)

min_rating = st.sidebar.slider(
    "Minimum hotel rating",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.5,
)

# Apply filters
filtered = hotels.copy()

if selected_locations:
    filtered = filtered[filtered["location"].isin(selected_locations)]

if "rating" in filtered.columns:
    filtered = filtered[
        filtered["rating"].isna() | (filtered["rating"] >= min_rating)
    ]

# KPI cards
col1, col2, col3 = st.columns(3)

col1.metric("Hotels found", filtered["hotel_name"].nunique())
col2.metric(
    "Average hotel rating",
    f"{filtered['rating'].mean():.2f}" if filtered["rating"].notna().any() else "N/A",
)
col3.metric(
    "Hotels with review text",
    filtered.loc[filtered["review_text"].notna(), "hotel_name"].nunique(),
)

st.divider()

# Hotel comparison
st.subheader("Hotel comparison")

display_columns = [
    "hotel_name",
    "location",
    "rating",
    "review_score",
    "price_booking",
    "price_tripadvisor",
    "review_count_booking",
    "review_count_tripadvisor",
]

display_columns = [col for col in display_columns if col in filtered.columns]

st.dataframe(
    filtered[display_columns].sort_values(
        by="rating", ascending=False, na_position="last"
    ),
    use_container_width=True,
    hide_index=True,
)

# Review analysis
st.divider()
st.subheader("Guest review insights")

review_data = reviews.copy()
review_data["hotel_name"] = review_data["hotel_name"].astype(str)

matching_hotels = filtered["hotel_name"].dropna().astype(str).unique()
review_data = review_data[review_data["hotel_name"].isin(matching_hotels)]

if not review_data.empty:
    sentiment_counts = (
        review_data["sentiment"]
        .value_counts()
        .reindex(["Positive", "Neutral", "Negative"], fill_value=0)
    )

    left, right = st.columns(2)

    with left:
        st.markdown("**Review sentiment distribution**")
        st.bar_chart(sentiment_counts)

    topic_columns = [
        "staff_service",
        "cleanliness",
        "room_comfort",
        "location_beach",
        "food_dining",
        "value_for_money",
    ]

    topic_columns = [c for c in topic_columns if c in review_data.columns]

    if topic_columns:
        topic_counts = review_data[topic_columns].sum().sort_values(
            ascending=False
        )
        topic_counts.index = (
            topic_counts.index
            .str.replace("_", " ")
            .str.title()
        )

        with right:
            st.markdown("**Topics mentioned in reviews**")
            st.bar_chart(topic_counts)

    with st.expander("Read analyzed reviews"):
        review_columns = [
            c for c in ["hotel_name", "review_text", "sentiment"]
            if c in review_data.columns
        ]
        st.dataframe(
            review_data[review_columns],
            use_container_width=True,
            hide_index=True,
        )
else:
    st.info("No review data is available for the selected filters.")

st.caption(
    "Demo project: ratings and prices come from the supplied dataset. "
    "Review sentiment is an automated estimate, not a verified quality score."
)
