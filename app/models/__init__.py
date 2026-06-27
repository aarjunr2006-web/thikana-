from app.db.base_class import Base
from app.models.accommodation import Accommodation, TargetAudience
from app.models.food_service import FoodService, FoodServiceType, BudgetType
from app.models.fast_food_spot import FastFoodSpot

__all__ = [
    "Base",
    "Accommodation",
    "TargetAudience",
    "FoodService",
    "FoodServiceType",
    "BudgetType",
    "FastFoodSpot",
]
