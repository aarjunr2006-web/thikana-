from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from uuid import UUID

class FastFoodSpotBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the fast food spot")
    area: str = Field(..., min_length=1, max_length=255, description="Area location in Jodhpur")
    address: str = Field(..., min_length=1, max_length=500, description="Full physical address")
    contact_number: str = Field(..., min_length=1, max_length=50, description="Contact phone number")
    specialties: List[str] = Field(default=[], description="List of specialty items")
    average_cost_for_two: int = Field(..., ge=0, description="Average cost for two people in INR")
    top_items: Dict[str, float] = Field(default={}, description="JSON mapping of top items to their price")

class FastFoodSpotCreate(FastFoodSpotBase):
    pass

class FastFoodSpotUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    area: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    contact_number: Optional[str] = Field(None, min_length=1, max_length=50)
    specialties: Optional[List[str]] = None
    average_cost_for_two: Optional[int] = Field(None, ge=0)
    top_items: Optional[Dict[str, float]] = None

class FastFoodSpotResponse(FastFoodSpotBase):
    id: UUID

    class Config:
        from_attributes = True
