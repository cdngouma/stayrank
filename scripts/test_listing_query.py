from stayrank.data.repository import ListingRepository
from stayrank.models.schemas import ListingSearchCriteria


def main():
    repo = ListingRepository()

    criteria = ListingSearchCriteria(
        max_price=190,
        guests=2,
        min_bedrooms=1,
        room_type="Entire Property",
        required_amenities=["Wifi", "Kitchen"],
        preferred_neighborhoods=["Ville-Marie"],
        limit=10
    )

    listings = repo.search(criteria, debug=True)

    print(f"Found {len(listings)} listings\n")

    for listing in listings:
        print(f"{listing.listing_id} | {listing.listing_name}")
        print(f"Price: ${listing.price}")
        print(f"Neighborhood: {listing.neighborhood}")
        print(f"Rating: {listing.overall_rating}")
        print(f"Number of Reviews: {listing.number_of_reviews}")
        print(f"Amenities: {', '.join(listing.amenities[:8])}")
        print(f"URL: {listing.listing_url}")
        print("-" * 80)


if __name__ == "__main__":
    main()