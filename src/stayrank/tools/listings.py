from stayrank.data.repository import ListingRepository
from stayrank.models.schemas import ListingSearchCriteria, Listing


def search_listings(criteria: ListingSearchCriteria) -> list[Listing]:
    repo = ListingRepository()
    return repo.search(criteria)