from stayrank.tools.destinations import resolve_destination, resolve_destinations


def main():
    print("Testing single destination resolution...")
    print("Query: 'Bell Centre'")
    print(f"Resolved: {resolve_destination('Bell Centre')}\n")

    print()

    print("Testing multiple destination resolution...")
    queries = [ 
        "Montreal Museum of Fine Arts",
        "Centre Bell",
        "Oshelaga",
        "Buits d'Afrique",
        "Concordia University",
        "Not a real place"
    ]

    results = resolve_destinations(queries)

    for result in results:
        print(f"Name: {result.name}")
        print(f"Latitude: {result.latitude}")
        print(f"Longitude: {result.longitude}")
        print(f"Type: {result.destination_type}")
        print(f"Match Method: {result.match_method}")
        print()

if __name__ == "__main__":
    main()
