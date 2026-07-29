# Agentic StayRank: Project Plan

## Description
An logding AI agent that helps travelers identify suitable stays in a city (Montreal) by interpreting natural-language travel goals, building a structured recommendation plan, selecting and using relevant tools, evaluating results, and adapting its search strategy when necessary.

The system combines LLM-based intent understanding and planning with deterministic retrieval, geographical analysis, constraint handling, and ranking. Its goal is not only to return a ranked list of listings, but to maintain the traveler's objective across multiple steps, reason about tradeoffs, recover from insufficient results, and request approval before relaxing important comnstraints.

The project is designed to demonstrate practical agent behavior while preserving explainability, reproducibility, and cost efficiency.

## Agent Objectives
The StayRank agent should be able to:
- Interpret open-ended accommodation requests
- Separate explicit constraints from inferred assumptions
- Identify hard constraints, soft preferences, and priorities
- Dynamically determine which tools and data sources are required
- Retrive and enrich relevant listing candidates
- Rank listings using deterministic scoring
- Evaluate whether the results satisfy the user's goal

In future work:
- Replan when no satisfactory results are found by relaxing constraints while preserving non-negotiables requirements
- Maintain a search state across conversational turns
- Incorporate user feedback into subsequent searches

## Data Sources
StayRank separates external data sources from the runtime recommendation logic through provider and repository abstractions. Development uses local snapshots and preprocessed datasets for reproducibility, while the production-oriented design allows the same interfaces to be backed by APIs, scheduled ingestion jobs, or managed databases.

### Accommodation Listings
During development, accommodation data comes from an Inside Airbnb snapshot stored in a database such as DuckDB.

The application accesses listings through a `ListingProvider` interface rather than querying DuckDB directly. This allows to replace the snapshot with a live API without changing much.

### Transit Data
Transit station data is sourced from public GTFS feeds published by local transit agencies. Transit data should not be fetched with each request. A scheduled ingestion process should routinely retrieve the GTFS feeds. For the Montreal demo, STM data is downloaded ahead of time.

### Neighborhood Context
We get this data from OpenStreetMap data using OSMnx and Geopy. Similar to transit data, OSM data should be collected during preprocessing or through scheduled ingestion rather than during every user request.

Context categories may include restaurants and cafés, grocery stores, retail and shopping, bars and nightlife venues, parks and green spaces.

### Places and Destinations
Because proximity to a traveler's actual destination is an important recommendation signal, we use a destination resolver. Geocoding providers such as Nominatim may resolve coordinates for place entities (e.g. address, venues, landmarks, neighborhoods, named geographic features, etc.)

Resolved destinations should be cached to reduce repeatedd external requests and improve consistency.

### Events (Future work)
Event names cannot reliably be resolved through geocoding alone, so it should therefore follow a two-stage process.

```text
Event query
    ↓
Event or venue lookup
    ↓
Extract venue, address, or associated place
    ↓
Resolve the venue to coordinates
```

## Project Structure

```text
stayrank/
├── README.md
├── pyproject.toml
├── .env.example
├── data/
│   ├── raw/
│   │   ├── listings.csv.gz                       # Inside Airbnb snapshot used during development
│   │   ├── parks.csv                             # Montreal parks and open-space data
│   │   └── stops.csv                             # STM transit stops or GTFS data
│   └── processed/
│       ├── clean_listings.parquet                # Cleaned listing data
│       ├── montreal_metro_stations.parquet       # Metro stations and coordinates
│       ├── montreal_parks.parquet                # Park counts and proximity data
│       └── montreal_neighborhood_context.parquet # Aggregated neighborhood context signals
├── docs/
├── scripts/
├── src/
│   └── stayrank/
│       ├── data/
│       │   ├── ingest.py                         # Dataset ingestion and preprocessing
│       │   └── repository.py                     # Database queries
│       ├── tools/
│       │   ├── listings.py                       # Listing search tool
│       │   ├── destinations.py                   # Destination resolution tool
│       │   ├── transit.py                        # Metro proximity tool
│       │   ├── neighborhoods.py                  # Neighborhood context tool
│       │   └── shortlist.py                      # Shortlist persistence tool
│       ├── geo/
│       │   ├── distance.py                       # Distance and walking-time utilities
│       │   └── neighborhoods.py                  # Neighborhood geometry and proximity utilities
│       ├── ranking/
│       │   ├── scoring.py                        # Deterministic weighted scoring
│       │   └── explanations.py                   # Score contribution summaries
│       ├── models/
│       │   ├── schemas.py                        # Shared Pydantic schemas
│       │   ├── plan.py                           # RecommendationPlan models
│       │   ├── state.py                          # Agent task-state models
│       │   └── results.py                        # Ranked result models
│       ├── agent/
│       │   ├── planner.py                        # Intent interpretation and plan generation
│       │   ├── orchestrator.py                   # Main decision and execution loop
│       │   ├── evaluator.py                      # Goal-satisfaction evaluation
│       │   ├── replanner.py                      # Search recovery and plan revision
│       │   └── responder.py                      # Final grounded response generation
│       └── config.py
└── tests/
```

## Recommendation Plan
The LLM converts the traveler's request into a validated `RecommendationPlan` consisting of the following:
- *Hard constraints:* Explicit requirements that must not be violated.
- *Soft preferences:* Features that influence ranking but do not exclude candidates (i.e. no impact on retrieval).
- *Preferences weights:* Relative importance assigned to deterministic scoring features.
- *Completion criteria:* Conditions that determine whether the search has produced an acceptable result.

Example recommendation plan:

```json
{
   "hard_constraints": {
      "max_price": {
         "value": 250,
         "currency": "CAD",
         "source": "explicit"
      },
      "guests": {
         "value": 4,
         "source": "explicit"
      },
   },
   "soft_preferences": {
      "quietness": {
         "weight": 0.9,
         "source": "explicit"
      },
      "transit_access": {
         "weight": 0.8,
         "source": "inferred"
      },
      "property_privacy": {
         "weight": 0.49,
         "value": "entire_home",
         "source": "inferred"
      }
   },
   "completion_criteria": {
      "minimum_eligible_candidates": 5,
      "minimum_shortlist_size": 3,
      "all_hard_constraints_satisfied": true
   }
}
```

## Tools
### ListingSearchTool
Finds candidate stays from the local listing database (in dev). Supported filters may include `max_price`, `guests`, `bedrooms`, `amenities`, `property_privacy` (entire property, private room, or shared room), `property_type`, `host_verified`, `minimum_nights`, `preferred_neighborhoods`, and `excluded_neighborhoods`.

Only explicit hard constraints should be applied as mandatory database (or API) filters. Inferred preferences should be affecting scoring rather than eligibility.

A development version may use simulated availability until a legitimate live source is available.

### TransitProximityTool
This tool finds the nearest metro to a stay by computing straight-line distance, as well as the estimated walking distance and time.

### NeighborhoodContextTool
Retrieves structured neighborhood signals such as green spaces score, park count, dining score, grocery score, nightlife score (bars, pubs and night clubs), and general liveliness.

These values are used as ranking features and proxies, not as definitive description of a neighborhood.

### ShortlistTool (Future work)
Stores or retrieves a user's current shortlist. This would supports conversational refinement, rejected listing cache, and comparison across search iterations.

### DestinationResolverTool (Future work)
Converts a destination, address, venue, attraction, or event name into canonical entity and coordinates.

## Ranking and Scoring Logic
We score candidates using nornmalized structured signals such as:
- price
- review quality
- cleanliness score
- host trust
- amenity matches
- user preference: transit accessibility, green spaces, nightlife or liveliness, property privacy, etc.

The ranking module is deterministic and records the contribution of each feature to the final score.

Example score breakdown:

```json
{
   "listing_id": 123,
   "total_score": 87.4,
   "score_components": {
      "price": 16.2,
      "reviews": 13.8,
      "cleanliness": 9.4,
      "host_trust": 4.6,
      "transit_access": 18.7,
      "destination_proximity": 14.1,
      "green_space": 8.5,
      "quietness": 2.1
   }
}
```

## Orchestration Architecture


```text
User Travel Goal
        │
        ▼
Planner Agent
  - extract explicit constraints
  - extract soft preferences
  - record inferred assumptions
  - identify destinations
  - propose ranking priorities
  - define completion criteria
        │
        ▼
RecommendationPlan Validator
  - validate schema
  - normalize weights
  - enforce constraint policies
        │
        ▼
Search Orchestrator
   - Resolve destinations
   - Rearch listings using hard constraints
   - Enrich candidates as required
      ├── neighborhood context
      ├── transit proximity
      └──destination proximity
        │
        ▼
Enriched Candidates
        │
        ▼
Deterministic Scoring and Ranking
        │
        ▼
Ranked Shortlist with Score Breakdown
        │
        ▼
Deterministic Goal Evaluator
        │
        ├── Goal satisfied
        │       → Final Recommendations
        └── Insufficient results
                → update state, relax according to policy and replan
```

## Tool-Calling Policy
The LLM may determine which information is required, but deterministic orchestration enforces valid execution.

Examples:

```python
if plan.destinations and not state.destinations_resolved:
   call_destination_resolver()

if plan.requires_feature("transit_access"):
   call_transit_proximity_tool()

if plan.requires_feature("green_space"):
   call_neighborhood_context_tool()
```

## Example Workflow

### User Request
> I am traveling with a family of four to Montreal for the Grand Prix. We would like somewhere fairly quiet, accessible by public transit, and close to parks. Our budget is CAD 250 per night.

### Step 1: Build Recommendation Plan
The planner extracts:

```json
{
   "hard_constraints": {
      "max_price": {
         "value": 250,
         "currency": "CAD",
         "source": "explicit",
         "weight": 0.15
      },
      "guests": {
         "value": 4,
         "source": "explicit"
      }
   },
   "soft_preferences": {
      "quietness": {
         "weight": 0.9,
         "source": "explicit"
      },
      "green_spaces": {
         "weight": 0.9,
         "source": "explicit"
      },
      "transit_access": {
         "weight": 0.85,
         "source": "explicit"
      },
      "liveliness": {
         "weight": -0.7,
         "source": "explicit"
      },
      "property_privacy": {
         "value": "entire_home_preferred",
         "weight": 0.6,
         "source": "inferred"
      }
   },
   "destinations": [
      {
         "query": "Montreal Grand Prix",
         "type": "event"
      }
   ]
}
```

### Step 2: Resolve Destination (Future work)
The agent calls `DestinationResolverTool` and maps "Montreal Grand Prix" --> "Circuit Gilles-Villeneuve" --> Resolved coordinates.

### Step 3: Retrieve Candidates
The agent calls `ListingSearchTool` using only explicit hard constraints.

```json
{
   "max_price": 250,
   "guests": 4,
   "limit": 200
}
```

### Step 4: Enrich Candidates
Based on the plan, the agent may determine that the following features are required:
- Destination proximity
- Transit proximity
- Green spaces (neighborhood context)
- Neighborhood liveliness (neighborhood context)

The system then computes:
- Distance from each listing to Circuit Gilles-Villeneuve
- Distance to the nearest metro station
- Estimated walking time to the nearest metro station
- Neighborhood green space score
- Neighborhood nightlife or liveliness score

### Step 5: Rank Listings
The scoring module applies preference weights and returns the top K listings ranked based on the user's preferences.

### Step 6: Evaluate Results
The evaluator checks:
- At least 1 eligible candidates exist
- All hard constraints are satisfied
- The top candidates have sufficient evidence
- The shortlist contains meaningful alternatives

### Step 8: Generate Grounded Recommendations
The response generator receives only the top K listings and their evidence.

For each listing, it generates a short description explaining which requirements it satisfies and any relevant tradeoffs.

The LLM does not silently re-rank the deterministic results.

## Example Ranked Listing Payload

```json
{
  "listing_id": 123,
  "name": "Quiet family apartment near the metro",
  "description_summary": "Two-bedroom apartment with a kitchen, quiet rear bedrooms, and nearby park access.",
  "price": 238,
  "host_verified": true,
  "neighborhood": "Rosemont–La Petite-Patrie",
  "property_category": "Apartment",
  "room_type": "Entire home/apt",
  "accommodates": 4,
  "bedrooms": 2,
  "beds": 3,
  "matched_amenities": [
    "Wifi",
    "Kitchen",
    "Washer"
  ],
  "reviews": {
    "count": 84,
    "overall": 4.89,
    "cleanliness": 4.92,
    "location": 4.81
  },
  "transit": {
    "nearest_metro": "Beaubien",
    "distance_km": 0.62,
    "walking_minutes": 9
  },
  "destinations": [
    {
      "name": "Circuit Gilles-Villeneuve",
      "distance_km": 7.8,
      "travel_context": "Accessible through the metro network"
    }
  ],
  "neighborhood_context": {
    "green_space_score": 0.84,
    "nightlife_score": 0.31,
    "liveliness_score": 0.46
  },
  "structured_score": 87.4,
  "score_components": {
    "price": 12.8,
    "reviews": 9.1,
    "cleanliness": 9.5,
    "host_trust": 4.7,
    "transit_access": 18.2,
    "destination_proximity": 11.6,
    "green_space": 13.1,
    "quietness": 8.4
  }
}
```

## Tech Stack

* Python
* Google ADK
* DuckDB
* Pandas
* Pydantic