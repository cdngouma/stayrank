# Agentic StayRank

An AI-powered accommodation recommendation system that transforms natural-language travel goals into personalized lodging recommendations using LLM planning, deterministic ranking, and geospatial intelligence.

## Overview

Agentic StayRank enables travelers to describe their accommodation needs in plain English instead of relying on manual filters.

The system interprets travel goals, retrieves candidate accommodations, enriches listings with neighborhood, transit, and geographic context, and applies deterministic multi-factor scoring to recommend the best lodging options. Rather than allowing an LLM to rank results directly, StayRank uses AI for planning and explanation while keeping retrieval and ranking transparent, reproducible, and explainable.

## Example Query

> *I'm visiting Montreal for Osheaga with a budget of $250/night. I'd like to stay near a metro station, prioritize safety, and have restaurants and nightlife within walking distance.*

## Architecture

```text
                Natural-Language Query
                         │
                         ▼
               LLM Recommendation Planner
                         │
          Structured Recommendation Plan
                         │
                         ▼
          Deterministic Orchestrator
        ┌────────────┬──────────────┬──────────────┐
        │            │              │              │
        ▼            ▼              ▼              ▼
  Listing Search  Transit Data  OSM Enrichment  Destination Resolution
        └────────────┴──────────────┴──────────────┘
                         │
                         ▼
              Deterministic Ranking Engine
                         │
                         ▼
               LLM Recommendation Response
```

## Features

- Interpret natural-language travel requirements
- Generate structured recommendation plans
- Retrieve accommodation listings
- Enrich listings with neighborhood and transit intelligence
- Apply deterministic multi-factor ranking
- Generate grounded recommendation explanations

## Ranking Signals

Listings are scored using deterministic criteria, including:

- Budget fit
- Destination proximity
- Transit accessibility
- Neighborhood amenities
- Safety indicators
- Accommodation preferences
- User-defined priorities

The ranking algorithm remains deterministic to ensure consistent, explainable recommendations while the LLM focuses on planning and natural-language interaction.

## Tech Stack

Core:

- Google Gemini
- Google ADK
- Pydantic
- Python
- DuckDB
- Pandas

Geospatial:
- OSMnx
- OpenStreetMap
- GTFS Transit Data

## Project Structure

```text
stayrank/
├── app/
│   ├── agent/
│   ├── orchestration/
│   ├── ranking/
│   ├── retrieval/
│   ├── enrichment/
│   ├── tools/
│   └── models/
├── data/
├── notebooks/
├── tests/
├── README.md
└── plan.md
```

## Design Documentation

The complete project architecture, workflow, data sources, and implementation roadmap are available in **`docs/plan.md`**.

## Goals

- Build a hybrid AI recommendation agent for travel accommodations
- Demonstrate deterministic AI system design
- Combine LLM planning with explainable ranking
- Explore geospatial and transit-aware recommendation systems
- Showcase production-oriented AI engineering practices

## Project Status

🚧 **In Active Development**


Current focus includes:

- Tool orchestration
- Recommendation evaluation