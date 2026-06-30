import re
import duckdb
import json
import pandas as pd
from collections import Counter

from stayrank.config import (
    RAW_LISTINGS_PATH,
    DB_PATH,
    PROCESSED_DIR
)
import logging

logger = logging.getLogger(__name__)

KEEP_COLUMNS = [
    # Identifiers
    "id", "listing_url", "name", "description",
    # Host information
    "host_id", "host_name", "host_identity_verified",
    # Location information
    "neighbourhood_cleansed", "latitude", "longitude",
    # Property information
    "property_type", "accommodates", "bedrooms", "beds", "amenities",
    # Price information
    "price", "minimum_nights",
    # Review signals
    "number_of_reviews", "review_scores_rating", "review_scores_cleanliness", "review_scores_location"
]

TOP_10_PROPERTY_TYPES = [
    "Rental Unit", 
    "Condo", 
    "House", 
    "Loft", 
    "Hotel", 
    "Townhouse", 
    "Aparthotel", 
    "Serviced Apartment", 
    "Hostel", 
    "Bed & Breakfast"
]


PROPERTY_TYPES_RENAMES = {
    "Home": "House",
    "Bed and breakfast": "Bed & Breakfast",
}

COMMON_AMENITY_COVERAGE_THRESHOLD = 20

COLUMNS_RENAME = {
    "id": "listing_id",
    "name": "listing_name",
    "host_identity_verified": "host_verified",
    "neighbourhood_cleansed": "neighborhood",
    "review_scores_rating": "overall_rating",
    "review_scores_cleanliness": "cleanliness_rating",
    "review_scores_location": "location_rating"
}


def clean_price(price):
    if isinstance(price, str):
        price = re.sub(r"[^\d.]", "", price)
        try:
            return float(price)
        except ValueError:
            return None
    return price


def clean_binary(value):
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value = value.strip().lower()
        if value in ["t", "true", "1", "yes"]:
            return True
        elif value in ["f", "false", "0", "no"]:
            return False
    
    return None


def clean_property_type(property_type):
    """
    Cleans the property_type column and extracts building_type and room_type.
    """
    if not isinstance(property_type, str):
        return pd.Series({"property_type": None, "room_type": None})
    
    property_type = property_type.strip().lower()

    if re.search(r"^entire", property_type):
        m = re.search(r"^entire\s+(.*)", property_type)
        building_type = m.group(1).title() if m else None
        room_type = "Entire Property"
    
    elif re.search(r"^(private|room)", property_type):
        m = re.search(r"^(private )?room in\s+(.*)", property_type)
        building_type = m.group(2).title() if m else None
        room_type = "Private Room"
    
    elif re.search(r"^shared", property_type):
        m = re.search(r"^shared room in\s+(.*)", property_type)
        building_type = m.group(1).title() if m else None
        room_type = "Shared Room"
    
    else:
        building_type = property_type.title()
        room_type = None

    building_type = PROPERTY_TYPES_RENAMES.get(building_type, building_type)
    
    return pd.Series({"property_type": building_type, "room_type": room_type})


def parse_amenities(amenities):
    if isinstance(amenities, str):
        return re.findall(r'"(.*?)"', amenities)
    return []


def preprocess_listings(df):
    df = df[[col for col in KEEP_COLUMNS if col in df.columns]].copy()

    # Add city and province columns for consistency
    df["city"] = "Montreal"
    df["province"] = "Quebec"

    # Clean price column
    df["price"] = df["price"].apply(clean_price)

    # Clean host_identity_verified column
    df["host_identity_verified"] = df["host_identity_verified"].apply(clean_binary)

    # Clean property_type column and extract building_type and room_type
    df[["property_type", "room_type"]] = df["property_type"].apply(clean_property_type)

    # Group rare property types into "Other" category (if not in the top 10 most common property types)
    df["property_category"] = df["property_type"].where(
        df["property_type"].isin(TOP_10_PROPERTY_TYPES),
        "Other"
    )

    # Parse amenities column
    df["amenities"] = df["amenities"].apply(parse_amenities)

    # Calculate amenity coverage and filter to top amenities (>= 20% coverage)
    amenity_counts = Counter(amenity for amenities in df["amenities"] for amenity in amenities)
    amenity_coverage = (
        pd.DataFrame(amenity_counts.items(), columns=["amenity", "count"])
        .assign(coverage=lambda x: round(100 * x["count"] / len(df), 2))
        .sort_values(by="coverage", ascending=False)
    )

    top_amenities = amenity_coverage.query(f'coverage >= {COMMON_AMENITY_COVERAGE_THRESHOLD}').amenity.tolist()

    df["amenities"] = df["amenities"].apply(lambda x: [amenity for amenity in x if amenity in top_amenities])

    df = df.rename(columns=COLUMNS_RENAME)

    return df


def ingest_listings():
    if not RAW_LISTINGS_PATH.exists():
        raise FileNotFoundError(
            f"Missing {RAW_LISTINGS_PATH}. Download listings.csv.gz from Inside Airbnb into data/raw/"
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_LISTINGS_PATH, compression="gzip", low_memory=False)

    df = preprocess_listings(df)

    df["amenities"] = df["amenities"].apply(json.dumps)  # Convert list to JSON string for DuckDB ingestion

    # Create DuckDB database and ingest the cleaned listings
    schema = "airbnb"
    table_name = "listings"
    with duckdb.connect(str(DB_PATH)) as con:
        con.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        con.execute(f"DROP TABLE IF EXISTS {schema}.{table_name}")
        con.execute(f"CREATE TABLE {schema}.{table_name} AS SELECT * FROM df")
        con.execute(f"CREATE INDEX idx_listing_id ON {schema}.{table_name}(listing_id)")
    
    logger.info(f"Listings ingested: {len(df)} rows saved to {DB_PATH}")


if __name__ == "__main__":
    ingest_listings()