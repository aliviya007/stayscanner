# StayScanner — Hotel Price & Review Intelligence

StayScanner is a portfolio project that combines hotel data cleaning, price and rating comparison, review sentiment analysis, web scraping, and an interactive Streamlit dashboard.

The goal is to demonstrate how raw accommodation data can be transformed into a structured dataset and a useful comparison experience.

## Features

- **Data cleaning:** Standardizes hotel information and prepares price, rating, and review-count fields.
- **Hotel comparison:** Combines available Booking.com and Tripadvisor data for comparison.
- **Review sentiment analysis:** Uses VADER sentiment scoring to classify review text as positive, neutral, or negative.
- **Review topic indicators:** Uses keyword-based rules to flag mentions of service, cleanliness, room comfort, location, food, and value for money.
- **Web scraping:** Collects sample accommodation-plan information from a demo hotel website.
- **Interactive dashboard:** Filters hotels by location and minimum rating, compares available metrics, and explores review insights.

## Tech Stack

Python · Pandas · Streamlit · VADER Sentiment · Requests · Beautiful Soup

## Project Structure

```text
stayscanner/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── clean_data.py
│   ├── scraper.py
│   ├── review_analysis.py
│   └── hotel_summary.py
├── requirements.txt
└── README.md
```

## Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/aliviya007/stayscanner.git
   cd stayscanner
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Launch the dashboard:

   ```bash
   streamlit run dashboard/app.py
   ```

## Data & Methodology

The project uses a sample hotel dataset containing accommodation details, prices, ratings, review counts, and review text. Data cleaning and matching are performed in Python before the results are used for analysis.

The scraper targets a demonstration hotel website. Its output is intended for practicing data extraction and is not presented as live market pricing.

## Limitations

- Hotel matching depends on the available hotel names and fields.
- Price comparisons are limited to records that could be matched across the source datasets.
- VADER provides a general-purpose sentiment estimate; it may not interpret context, sarcasm, or nuanced hotel feedback accurately.
- Review topic indicators are keyword-based, not a trained topic model.
- The sample data and scraped demo plans do not represent a real-time hotel booking service.

## Future Improvements

- Deploy the dashboard publicly.
- Improve hotel matching and data validation.
- Add more robust review-topic classification.
- Extend the comparison experience with additional accommodation sources.

---

**Disclaimer:** StayScanner is an independent portfolio project for data analytics and engineering practice. It is not affiliated with Booking.com or Tripadvisor.
