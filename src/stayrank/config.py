from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

# Raw data paths
RAW_DIR = DATA_DIR / "raw"
RAW_LISTINGS_PATH = RAW_DIR / "listings.csv.gz"
RAW_STM_STOPS_PATH = RAW_DIR / "stm_stops.csv"
RAW_DESTINATIONS_PATH = RAW_DIR / "montreal_destinations.txt"
RAW_EVENTS_PATH = RAW_DIR / "montreal_events.csv"

# Processed data paths
PROCESSED_DIR = DATA_DIR / "processed"
METRO_STATIONS_PATH = PROCESSED_DIR / "montreal_metro_stations.parquet"

# Database path
DB_PATH = DATA_DIR / "stayrank.duckdb"

# Neighborhood/boroughs
BOROUGHS_LIST = [
    'Ville-Marie', 'Rosemont-La Petite-Patrie',
    'Côte-des-Neiges-Notre-Dame-de-Grâce', 'Le Sud-Ouest',
    'Le Plateau-Mont-Royal', 'Villeray-Saint-Michel-Parc-Extension',
    "Baie-d'Urfé", 'Saint-Laurent', 'Mercier-Hochelaga-Maisonneuve',
    'Lachine', 'Outremont', 'Ahuntsic-Cartierville', 'Westmount',
    'Dorval', 'Anjou', 'Pointe-Claire', 'Verdun', 'Mont-Royal',
    'LaSalle', 'Côte-Saint-Luc', "L'Île-Bizard-Sainte-Geneviève",
    'Hampstead', 'Saint-Léonard', 'Beaconsfield',
    'Dollard-des-Ormeaux', 'Pierrefonds-Roxboro', 'Montréal-Ouest',
    'Rivière-des-Prairies-Pointe-aux-Trembles', 'Montréal-Nord',
    'Kirkland', 'Montréal-Est', 'Sainte-Anne-de-Bellevue'
]