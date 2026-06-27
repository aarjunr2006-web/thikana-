from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from app.models.accommodation import TargetAudience

class AccommodationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the accommodation")
    area: str = Field(..., min_length=1, max_length=255, description="Area location in Jodhpur")
    address: str = Field(..., min_length=1, max_length=500, description="Full physical address")
    contact_number: str = Field(..., min_length=1, max_length=50, description="Contact phone number")
    target_audience: TargetAudience = Field(..., description="Target audience (Boys, Girls, Co-ed)")
    features: List[str] = Field(default=[], description="List of key features")
    distance_from_college_km: float = Field(..., ge=0.0, description="Distance from college in KM")
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Optional GPS latitude coordinate")
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Optional GPS longitude coordinate")

class AccommodationCreate(AccommodationBase):
    pass

class AccommodationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    area: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    contact_number: Optional[str] = Field(None, min_length=1, max_length=50)
    target_audience: Optional[TargetAudience] = None
    features: Optional[List[str]] = None
    distance_from_college_km: Optional[float] = Field(None, ge=0.0)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)

class AccommodationResponse(AccommodationBase):
    id: UUID

    class Config:
        from_attributes = True
