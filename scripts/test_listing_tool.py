from stayrank.tools.listings import search_listings
from stayrank.models.schemas import ListingSearchCriteria

def main():
    criteria = ListingSearchCriteria(
        max_price=190,
        guests=2,
        min_bedrooms=1,
        room_type="Entire Property",
        required_amenities=["Wifi", "Kitchen"],
        preferred_neighborhoods=["Ville-Marie", "Le Plateau-Mont-Royal"],
        limit=5
    )

    print("Searching for listings with the following criteria:")
    print(f"Max Price: ${criteria.max_price}")
    print(f"Guests: {criteria.guests}")
    print(f"Minimum Bedrooms: {criteria.min_bedrooms}")
    print(f"Room Type: {criteria.room_type}")
    print(f"Required Amenities: {', '.join(criteria.required_amenities)}")
    print(f"Preferred Neighborhoods: {', '.join(criteria.preferred_neighborhoods)}")


    listings = search_listings(criteria)

    print(f"Found {len(listings)} listings\n\n")

    for i, listing in enumerate(listings):
        print(f"{i+1}. Listing ID: {listing.listing_id}")
        print(f"Price: ${listing.price}")
        print(f"Neighborhood: {listing.neighborhood}")
        print(f"Rating: {listing.overall_rating}")
        print(f"Number of Reviews: {listing.number_of_reviews}")
        print(f"Amenities: {', '.join(listing.amenities[:8])}")
        print("-" * 30)


if __name__ == "__main__":
    main()