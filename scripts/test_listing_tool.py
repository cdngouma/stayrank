from stayrank.tools.listings import search_listings
from stayrank.models.schemas import ListingSearchCriteria

def main():
    criteria = ListingSearchCriteria(
        max_price=190,
        guests=2,
        min_bedrooms=1,
        room_type="Entire Property",
        required_amenities=["Wifi", "Kitchen"],
        preferred_neighborhoods=["Ville-Marie"],
        limit=10
    )

    listings = search_listings(criteria)

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