import json
from typing import List

import duckdb

from stayrank.config import DB_PATH
from stayrank.models.schemas import Listing, ListingSearchCriteria


class ListingRepository:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
    
    def search(self, criteria: ListingSearchCriteria, debug: bool=False) -> List[Listing]:
        params = []

        query = "SELECT *"

        if len(criteria.preferred_neighborhoods) > 0:
            placeholders = ", ".join(["?"] * len(criteria.preferred_neighborhoods)) 
            query += f""",
            CASE WHEN neighborhood IN ({placeholders}) THEN 1 ELSE 0 END AS is_preferred_neighborhood
            """
            params.extend(criteria.preferred_neighborhoods)
        else:
            query += ", 1 AS is_preferred_neighborhood"
        
        query += """
        FROM airbnb.listings
        WHERE price IS NOT NULL
          AND latitude IS NOT NULL
          AND longitude IS NOT NULL
        """

        if criteria.max_price is not None:
            query += "\n  AND price <= ?"
            params.append(criteria.max_price)
        
        if criteria.guests is not None:
            query += "\n  AND accommodates >= ?"
            params.append(criteria.guests)

        if criteria.min_bedrooms is not None:
            query += "\n  AND bedrooms >= ?"
            params.append(criteria.min_bedrooms)

        if criteria.room_type is not None:
            query += "\n  AND LOWER(room_type) = LOWER(?)"
            params.append(criteria.room_type)
        
        if criteria.property_category is not None:
            query += "\n  AND LOWER(property_category) = LOWER(?)"
            params.append(criteria.property_category)
        
        if criteria.verified_host:
            query += "\n  AND host_verified IS TRUE"
        
        for amenity in criteria.required_amenities:
            query += "\n  AND amenities ILIKE ?"
            params.append(f'%{amenity}%')
        
        query += """
        ORDER BY
            is_preferred_neighborhood DESC,
            overall_rating DESC NULLS LAST,
            number_of_reviews DESC NULLS LAST,
            price ASC
        LIMIT ?
        """

        if debug:
            print("[DEBUG] Constructed query:\n", query, "\n\n")

        params.append(criteria.limit)

        with duckdb.connect(self.db_path) as con:
            rows = con.execute(query=query, parameters=params).fetchdf()

        listings = []

        for record in rows.to_dict(orient="records"):
            record.pop("is_preferred_neighborhood", None)
            
            if isinstance(record.get("amenities"), str):
                record["amenities"] = json.loads(record["amenities"])
            
            listings.append(Listing(**record))

        return listings
    
    def get_by_id(self, listing_id: int) -> Listing:
        query = """"
            SELECT *
            FROM airbnb.listings
            WHERE listing_id = ?
            LIMIT 1
        """

        with duckdb.connect(self.db_path) as con:
            rows = con.execute(query=query, parameters=[listing_id])

        if rows.empty:
            return None
        
        record  = rows.iloc[0].to_dict()

        if isinstance(record.get("amenities"), str):
            record["amenities"] = json.loads(record["amenities"])

        return Listing(**record)
