from pydantic import BaseModel
from typing import Optional, List


class Listing(BaseModel):
    # Indentifiers
    listing_id: int
    listing_url: str
    listing_name: Optional[str] = None
    description: Optional[str] = None
    # Host information
    host_id: Optional[int] = None
    host_name: Optional[str] = None
    host_verified: Optional[bool] = None
    # Location information
    city: str
    province: str
    neighborhood: Optional[str] = None
    latitude: float
    longitude: float
    # Property information
    property_category: Optional[str] = None
    room_type: Optional[str] = None
    accommodates: int
    bedrooms: Optional[int] = None
    beds: Optional[float] = None
    amenities: list[str] = []
    price: float
    minimum_nights: Optional[int] = None
    # Reviews information
    number_of_reviews: Optional[int] = None
    overall_rating: Optional[float] = None
    cleanliness_rating: Optional[float] = None
    location_rating: Optional[float] = None


class ListingSearchCriteria(BaseModel):
    max_price: float
    guests: int
    min_bedrooms: Optional[int] = None
    room_type: Optional[str] = None
    property_category: Optional[str] = None
    required_amenities: list[str] = []
    preferred_neighborhoods: Optional[list[str]] = []
    verified_host: Optional[bool] = False
    limit: int = 50


class Recommendation(BaseModel):
    listing_id: str
    name: str
    score: float
    reasons: Optional[List[str]] = None