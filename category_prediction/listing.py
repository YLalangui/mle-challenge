from pydantic import BaseModel


class ListingInfo(BaseModel):
    """Class to represent a listing information created when category inference
    Args:
        id: id number
        accommodates: number of people inside that house
        room_type: Room type
        beds: number of beds
        bedrooms: number of bedrooms
        bathrooms: number of bathrooms
        neighbourhood: number of neighbourhood
        tv: 1 if there is TV, otherwise 0
        elevator: 1 if there is elevator, otherwise 0
        internet: 1 if there is internet, otherwise 0
        latitude: GPS latitude
        longitude: GPS longitude
    """

    id: int
    accommodates: int
    room_type: str
    beds: int
    bedrooms: int
    bathrooms: float
    neighbourhood: str
    tv: int
    elevator: int
    internet: int
    latitude: float
    longitude: float


class ServiceResponse(BaseModel):
    """Class to represent service response
    Args:
        id: id number
        category: category inference
    """

    id: int
    price_category: str
