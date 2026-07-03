from stayrank.data.repository import ListingRepository
from stayrank.models.schemas import ListingSearchCriteria, Listing

repo = ListingRepository()

def search_listings(criteria: ListingSearchCriteria) -> list[Listing]:
    return repo.search(criteria)