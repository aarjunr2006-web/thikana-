from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.fast_food_spot import FastFoodSpot

class FastFoodSpotRepository(BaseRepository[FastFoodSpot]):
    def __init__(self):
        super().__init__(FastFoodSpot)

    async def get_filtered(
        self,
        db: AsyncSession,
        *,
        area: Optional[str] = None,
        max_cost_for_two: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[FastFoodSpot]:
        """Fetch fast food spots, filtering optionally by area and maximum cost for two."""
        query = select(FastFoodSpot)
        
        if area:
            query = query.filter(FastFoodSpot.area.icontains(area))
        if max_cost_for_two is not None:
            query = query.filter(FastFoodSpot.average_cost_for_two <= max_cost_for_two)
            
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

fast_food_spot_repo = FastFoodSpotRepository()
