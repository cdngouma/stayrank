from stayrank.tools.borough_context import get_borough_context


def main():
    print("Testing single borough context retrieval...")
    borough = "Rosemont-La Petite-Patrie"
    context = get_borough_context(borough)
    print(f"Context for {borough}:\n{context}")

    print("\nTesting invalid borough context retrieval...")
    invalid_borough = "NonExistentBorough"
    invalid_context = get_borough_context(invalid_borough)
    print(f"Context for {invalid_borough}:\n{invalid_context}")


if __name__ == "__main__":
    main()