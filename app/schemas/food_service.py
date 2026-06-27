from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from app.models.food_service import FoodServiceType, BudgetType

class FoodServiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the food service")
    type: FoodServiceType = Field(..., description="Type of service (Tiffin, Dhaba, Bhojnalaya)")
    area: str = Field(..., min_length=1, max_length=255, description="Area in Jodhpur")
    address: str = Field(..., min_length=1, max_length=500, description="Full physical address")
    contact_number: str = Field(..., min_length=1, max_length=50, description="Contact phone number")
    timings: str = Field(..., min_length=1, max_length=255, description="Operating timings")
    budget_type: BudgetType = Field(..., description="Budget category (Budget, Mid-range)")
    usp: str = Field(..., min_length=1, max_length=255, description="Unique Selling Proposition")

class FoodServiceCreate(FoodServiceBase):
    pass

class FoodServiceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[FoodServiceType] = None
    area: Optional[str] = Field(None, min_length=1, max_length=255)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    contact_number: Optional[str] = Field(None, min_length=1, max_length=50)
    timings: Optional[str] = Field(None, min_length=1, max_length=255)
    budget_type: Optional[BudgetType] = None
    usp: Optional[str] = Field(None, min_length=1, max_length=255)

class FoodServiceResponse(FoodServiceBase):
    id: UUID

    class Config:
        from_attributes = True
