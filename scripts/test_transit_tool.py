
from stayrank.tools.transit import find_nearest_metro_station


def main():
    # 4272 R. Saint-Denis, Montréal, QC H2J 2K8
    address = "4272 R. Saint-Denis, Montréal, QC H2J 2K8"
    latitude = 45.5221278
    longitude = -73.5793662

    result = find_nearest_metro_station(latitude, longitude)

    print(f"Address: {address}")
    print("--------------------------------")
    print(f"Nearest metro station: {result.station_name}")
    print(f"Straight-line distance: {result.distance_km} km")
    print(f"Estimated walking distance: {result.walking_distance} km")
    print(f"Estimated walking time: {result.walking_time_min} min")   


if __name__ == "__main__":
    main()