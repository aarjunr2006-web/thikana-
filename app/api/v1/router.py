from fastapi import APIRouter
from app.api.v1.endpoints import accommodation, food_service, fast_food_spot

api_router = APIRouter()
api_router.include_router(accommodation.router, prefix="/accommodations", tags=["accommodations"])
api_router.include_router(food_service.router, prefix="/food-services", tags=["food-services"])
api_router.include_router(fast_food_spot.router, prefix="/fast-food-spots", tags=["fast-food-spots"])
