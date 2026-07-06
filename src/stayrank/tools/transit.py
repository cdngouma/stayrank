import pandas as pd
from stayrank.config import METRO_STATIONS_PATH
from stayrank.geo.distance import haversine_km, estimate_walking_time
from stayrank.models.schemas import TransitInfo


# Load once when the module is imported to avoid repeated I/O operations
METRO_STATIONS = pd.read_parquet(METRO_STATIONS_PATH)


def find_nearest_metro_station(lat: float, lon: float) -> TransitInfo:
    stations = METRO_STATIONS.copy()

    stations['distance_km'] = stations.apply(
        lambda row: haversine_km(
                lat, lon, 
                row['stop_lat'], row['stop_lon']
            ),
            axis=1
        )

    nearest_station = stations.loc[stations['distance_km'].idxmin()]

    walking_distance_km = nearest_station['distance_km'] * 1.2 # Adjusting for walking path
    walking_time_min = estimate_walking_time(walking_distance_km)

    return TransitInfo(
        station_name=nearest_station['stop_name'],
        distance_km=round(nearest_station['distance_km'], 2),
        walking_distance=round(walking_distance_km, 2),
        walking_time_min=round(walking_time_min, 2)
    )