# Agentic StayRank

An AI-powered accommodation recommendation system that combines LLM reasoning with deterministic retrieval, geospatial analysis, and structured ranking to generate personalized, explainable lodging recommendations.

Unlike traditional accommodation search platforms that rely primarily on filtering, Agentic StayRank interprets a traveler's intent, orchestrates specialized retrieval tools, enriches candidate listings with contextual signals, and reasons about tradeoffs to recommend accommodations that best satisfy the user's priorities.

---

## Motivation

Finding accommodation often involves balancing competing objectives:

- Budget
- Transit accessibility
- Destination proximity
- Neighborhood quality
- Amenities
- Safety

Traditional search platforms expose these constraints as independent filters, leaving users to manually compare dozens of listings.

Agentic StayRank approaches the problem as an **AI decision-making task**. Rather than filtering listings alone, the system combines structured retrieval, geospatial reasoning, and LLM-based preference understanding to generate recommendations that reflect how people naturally plan trips.

---

## Features

### Agent Reasoning

- Natural-language travel planning
- Intent and preference extraction
- Tool orchestration
- Explainable recommendation generation

### Retrieval & Ranking

- Constraint-based accommodation retrieval
- Destination proximity analysis
- Transit accessibility scoring
- Neighborhood context enrichment
- Hybrid deterministic + LLM ranking
- Preference-conditioned scoring

---

## Example Query

> I'm visiting Montreal for Osheaga in August. My budget is under \$250 per night. I'd like to stay close to a metro station, prioritize safety, and have restaurants and nightlife within walking distance.

---

## System Architecture

```text
                 User Query
                     │
                     ▼
             LLM Intent Extraction
        ┌────────────┼────────────┐
        │            │            │
 Hard Constraints  Preferences  Destinations
        │            │            │
        └────────────┼────────────┘
                     ▼
            Listing Search Tool
                     │
                     ▼
            Candidate Accommodations
                     │
                     ▼
          Parallel Tool Orchestration
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
 Destination  Transit Tool  Neighborhood Tool
 Resolution
        │            │            │
        └────────────┼────────────┘
                     ▼
        Preference-Conditioned Ranking
                     ▼
         LLM Tradeoff Reasoning
                     ▼
      Explainable Top-K Recommendations
```

---

## Design Philosophy

The LLM is responsible for reasoning—not computation.

Deterministic components perform:

- Database filtering
- Geospatial calculations
- Distance estimation
- Transit analysis
- Candidate scoring

The LLM performs:

- Intent understanding
- Preference extraction
- Tool orchestration
- Tradeoff reasoning
- Recommendation explanation

Separating deterministic computation from language reasoning improves reproducibility, debuggability, and reliability while allowing the system to remain flexible to natural-language inputs.

---

## Ranking Strategy

Candidate listings are first filtered using hard constraints such as budget, room type, occupancy, and amenities.

Remaining candidates are enriched with additional signals including:

- Destination proximity
- Transit accessibility
- Host trust
- Review quality
- Neighborhood context

The LLM infers user preference weights from the natural-language query and applies them to produce a structured ranking before performing a final reasoning pass.

Example inferred weights:

```python
{
    "price": 0.20,
    "reviews": 0.15,
    "cleanliness": 0.10,
    "host_trust": 0.05,
    "transit_access": 0.25,
    "destination_proximity": 0.20,
    "neighborhood_context": 0.05,
}
```

This hybrid approach combines deterministic ranking with LLM reasoning to produce recommendations that remain explainable while adapting to individual traveler priorities.

---

## Project Structure

```text
agentic-stayrank/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
│
├── docs/
│
├── src/
│   ├── agent/
│   ├── data/
│   ├── geo/
│   ├── models/
│   └── tools/
│
├── tests/
├── pyproject.toml
└── README.md
```

---

## Data Sources

Current development uses publicly available datasets:

- Inside Airbnb listing snapshots
- STM GTFS transit data
- Curated destination database
- Public neighborhood datasets

The modular architecture allows additional data providers to be integrated with minimal changes to the ranking pipeline.

---

## Tech Stack

- Python
- OpenAI API
- LangChain
- DuckDB
- Pandas
- Pydantic

---

## Current Status

🚧 **In Development**

Current progress includes:

- Listing ingestion pipeline
- Local accommodation database
- Agent orchestration workflow
- Geospatial utilities
- Tool interfaces
- Preference-conditioned ranking engine

---

## Future Work

- Neighborhood safety signals
- OpenStreetMap POI integration
- FastAPI backend
- Streamlit interface
- Multi-city support
- Evaluation benchmark for recommendation quality
