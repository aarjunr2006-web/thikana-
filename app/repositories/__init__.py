from app.repositories.base import BaseRepository
from app.repositories.accommodation import accommodation_repo, AccommodationRepository
from app.repositories.food_service import food_service_repo, FoodServiceRepository
from app.repositories.fast_food_spot import fast_food_spot_repo, FastFoodSpotRepository

__all__ = [
    "BaseRepository",
    "AccommodationRepository",
    "accommodation_repo",
    "FoodServiceRepository",
    "food_service_repo",
    "FastFoodSpotRepository",
    "fast_food_spot_repo",
]
