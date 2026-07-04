from difflib import get_close_matches
from geopy.geocoders import Nominatim

import pandas as pd
import time

from stayrank.config import DESTINATIONS_PATH
from stayrank.models.schemas import DestinationInfo


DESTINATIONS = pd.read_parquet(DESTINATIONS_PATH)


def geocode_location(query: str) -> dict:
    geocoder = Nominatim(user_agent="stayrank", timeout=10)
    
    location = geocoder.geocode(f"{query}, Montreal, Quebec, Canada")
    
    time.sleep(1)  # To respect Nominatim's usage policy and avoid rate limiting
    
    if location:
        return {
            "name": query,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "type": "geocoded"
        }


def resolve_destination(query: str) -> DestinationInfo:
    if not query or not isinstance(query, str):
        return None
    
    destinations = DESTINATIONS.copy()

    normalized_query = query.strip().lower()
    normalized_names = destinations["name"].str.strip().str.lower()

    row = None
    match_method = None

    # Exact match
    exact_match = destinations[normalized_names == normalized_query]
    if not exact_match.empty:
        row = exact_match.iloc[0]
        match_method = "exact"
    
    # Fuzzy match
    else:
        close_matches = get_close_matches(
            normalized_query,
            normalized_names.tolist(),
            n=1,
            cutoff=0.6
        )

        if close_matches:
            row = destinations[normalized_names == close_matches[0]].iloc[0]
            match_method = "fuzzy"

    if row is None:
        row = geocode_location(query)
        match_method = "geocoded"
    
    if row is None:
        return None
    
    return DestinationInfo(
        name=row["name"],
        latitude=row["latitude"],
        longitude=row["longitude"],
        destination_type=row["type"],
        match_method=match_method
    )


def resolve_destinations(queries: list[str]) -> list[DestinationInfo]:
    results = []

    for query in queries:
        resolved = resolve_destination(query)
        
        if resolved:
            results.append(resolved)
    
    return results