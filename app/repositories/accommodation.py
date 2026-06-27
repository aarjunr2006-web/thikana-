from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.accommodation import Accommodation, TargetAudience

class AccommodationRepository(BaseRepository[Accommodation]):
    def __init__(self):
        super().__init__(Accommodation)

    async def get_filtered(
        self,
        db: AsyncSession,
        *,
        target_audience: Optional[TargetAudience] = None,
        max_distance_km: Optional[float] = None,
        area: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> Sequence[Accommodation]:
        """Fetch accommodations, filtering optionally by target audience, max distance, and area."""
        query = select(Accommodation)
        
        if target_audience:
            query = query.filter(Accommodation.target_audience == target_audience)
        if max_distance_km is not None:
            query = query.filter(Accommodation.distance_from_college_km <= max_distance_km)
        if area:
            query = query.filter(Accommodation.area.icontains(area))
            
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

accommodation_repo = AccommodationRepository()
