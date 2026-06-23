# Agentic StayRank

An AI-powered accommodation recommendation system that helps travelers discover the most suitable lodging options based on natural-language requirements.

## Overview

Agentic StayRank enables users to describe their travel requirements in plain English, including destination, budget, accommodation preferences, amenities, transportation constraints, and nearby points of interest. The system leverages an LLM-powered agent to extract structured requirements, retrieve candidate accommodations, enrich listings with external signals, and generate explainable recommendations.

Unlike traditional accommodation search platforms that rely primarily on filtering, Agentic StayRank combines constraint-based filtering, geospatial analysis, transit accessibility, safety indicators, and multi-factor ranking to identify the accommodations that best match a traveler's needs.

## Example Query

> I will be visiting Montreal for Osheaga. My budget is $250/night. I would like to stay near a metro station, prioritize safety, and have access to restaurants and nightlife.

## Planned Features

* Natural-language requirement extraction
* Accommodation retrieval from Airbnb datasets
* Geospatial and proximity analysis
* Transit accessibility scoring
* Safety-aware ranking
* Explainable recommendations
* Tool-calling agent orchestration

## Tech Stack

* Python
* OpenAI API
* DuckDB
* Pandas
* Pydantic
* LangChain (planned)

## Project Status

🚧 In Progress

Current focus:

* Data ingestion pipeline
* Local accommodation database
* Ranking engine
* Agent orchestration workflow

