from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_LISTINGS_PATH = RAW_DIR / "listings.csv.gz"
DB_PATH = DATA_DIR / "stayrank.duckdb"