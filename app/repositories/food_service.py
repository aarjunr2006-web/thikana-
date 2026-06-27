from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.food_service import FoodService, FoodServiceType

class FoodServiceRepository(BaseRepository[FoodService]):
    def __init__(self):
        super().__init__(FoodService)

    async def get_filtered(
        self,
        db: AsyncSession,
        *,
        service_type: Optional[FoodServiceType] = None,
        area: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[FoodService]:
        """Fetch food services, filtering optionally by type and area."""
        query = select(FoodService)
        
        if service_type:
            query = query.filter(FoodService.type == service_type)
        if area:
            query = query.filter(FoodService.area.icontains(area))
            
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

food_service_repo = FoodServiceRepository()
