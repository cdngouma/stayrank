# Agentic StayRank: Project Design

## Project Structure

```text
agentic-stayrank/
├── README.md
├── pyproject.toml
├── .env.example
├── data/
│   ├── raw/
│   │   ├── listings.csv.gz                    # Inside Airbnb listing snapshot used in dev instead of a live API
│   │   ├── parks.csv                          # Montreal parks/open-space data
│   │   └── stops.csv                          # STM transit stops / GTFS stops data
│   ├── reference/
│   │   └── montreal_destinations.csv          # Curated destinations/events and coordinates
│   └── processed/
│       ├── clean_listings.parquet             # Cleaned listing data
│       ├── montreal_destinations.parquet      # Known destinations and coordinates
│       ├── montreal_metro_stations.parquet    # Metro stations and coordinates
│       └── montreal_parks.parquet             # Park counts or park proximity data by neighborhood
├── docs/
│   └── architecture.md
├── scripts/
│   └── test_listing_query.py
├── src/
│   └── stayrank/
│       ├── data/
│       │   ├── ingest.py                      # Airbnb listings ingestion
│       │   ├── repository.py                  # Listing database queries
│       │   ├── destinations.py                # Loads known destinations
│       │   └── transit.py                     # Loads metro station data
│       ├── tools/
│       │   ├── listings.py                    # Listing search tool
│       │   ├── destinations.py                # Destination resolver tool
│       │   └── transit.py                     # Metro proximity tool
│       ├── geo/
│       │   └── distance.py                    # Distance and walking-time utilities
│       ├── models/
│       │   └── schemas.py                     # Pydantic schemas
│       └── agent/
│           └── orchestrator.py                # Main agent workflow
└── tests/
    └── test_listing_tool.py
```

## Tools

### V1 Tools

* **ListingSearchTool**: Finds candidate stays from the local database using hard constraints such as budget, guests, bedrooms, amenities, room type, property category, verified host status, and preferred neighborhoods.

* **DestinationResolverTool**: Converts a destination, address, venue, or event name into coordinates. For example, `"Osheaga"` can resolve to `"Parc Jean-Drapeau"` with latitude and longitude.

* **TransitProximityTool**: Finds the nearest metro station to a listing and estimates walking distance and walking time.

### Internal Utilities

* **Distance Utilities**: Compute haversine distance and estimated walking time between two coordinate pairs. These are helper functions, not agent tools.

* **Ranking / Scoring Logic**: Scores candidate listings using structured signals such as price, reviews, host trust, metro proximity, destination proximity, and user preferences. This is deterministic business logic, not an LLM tool.

### Future Tools

* **NeighborhoodContextTool**: Adds neighborhood-level context such as parks, restaurants, transit density, and general liveliness.

* **SafetyTool**: Adds safety-related neighborhood signals if reliable public data is available.

* **EventLookupTool**: Searches for unknown events and resolves their venue/location when the event is not already in the curated destination list.

* **RestaurantDensityTool**: Estimates nearby restaurant/cafe density using OpenStreetMap or another POI source.

* **PopulationDensityTool**: Adds census-based population density data if useful for neighborhood context.


## Orchestration Architecture

```text
User Query
   ↓
Orchestrator Agent
   ↓
LLM Intent Extraction
   ├─ hard constraints
   ├─ soft preferences
   ├─ destinations/events
   └─ priority weights
   ↓
ListingSearchTool
   ↓
Candidate Listings
   ↓
Parallel Enrichment
   ├─ DestinationResolverTool
   │    └─ distance to intended places/events
   ├─ TransitProximityTool
   │    └─ nearest metro + walking estimate
   └─ NeighborhoodContextTool
        └─ parks, restaurants, groceries, liveliness/safety context
   ↓
Preference-Conditioned Scoring
   ↓
Shortlist
   ↓
LLM Reranking + Tradeoff Explanation
   ↓
Top-K Recommendations
```

## Design Principle

The LLM is responsible for understanding user intent, deciding which tools are needed, and explaining the final recommendations. Deterministic code handles database filtering, distance calculation, transit proximity, and scoring so that the system remains reliable, debuggable, and reproducible.

## Example of What is Passed to the LLM (Re-ranking)

```json
{
  "listing_id": 123,
  "name": "Quiet Plateau apartment",
  "description_summary": "Renovated apartment near Saint-Denis, quiet bedroom, workspace.",
  "price": 162,
  "host_verified": true,
  "neighborhood": "Le Plateau-Mont-Royal",
  "property_category": "Apartment",
  "room_type": "Entire Property",
  "accommodates": 2,
  "bedrooms": 1,
  "beds": 1,
  "matched_amenities": ["Wifi", "Kitchen", "Dedicated workspace"],
  "reviews": {
    "count": 55,
    "overall": 5.0,
    "cleanliness": 5.0,
    "location": 4.96
  },
  "transit": {
    "nearest_metro": "Mont-Royal",
    "walking_minutes": 8
  },
  "destinations": [
    {"name": "Parc Jean-Drapeau", "distance_km": 5.2, "estimated_travel_context": "metro-accessible"}
  ],
  "neighborhood_context": {
    "restaurant_count": 42,
    "grocery_count": 5,
    "park_count": 3,
    "liveliness": "high"
  },
  "structured_score": 87.4
}
```

## Example of LLM-derived Weights

```json
weights = {
    "price": 0.20,
    "reviews": 0.15,
    "cleanliness": 0.10,
    "host_trust": 0.05,
    "transit_access": 0.25,
    "destination_proximity": 0.20,
    "neighborhood_context": 0.05,
}
```
