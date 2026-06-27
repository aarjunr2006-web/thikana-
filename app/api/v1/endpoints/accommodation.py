from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.accommodation import TargetAudience
from app.schemas.accommodation import (
    AccommodationResponse,
    AccommodationCreate,
    AccommodationUpdate,
)
from app.repositories.accommodation import accommodation_repo

router = APIRouter()

@router.get("/", response_model=List[AccommodationResponse])
async def read_accommodations(
    target_audience: Optional[TargetAudience] = Query(None, description="Filter by target audience (Boys, Girls, Co-ed)"),
    max_distance_km: Optional[float] = Query(None, ge=0.0, description="Filter by maximum distance from college in KM"),
    area: Optional[str] = Query(None, description="Filter by area location (case-insensitive match)"),
    skip: int = Query(0, ge=0, description="Skip offset pagination"),
    limit: int = Query(100, ge=1, le=100, description="Limit response size"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of accommodations.
    Supports filtering by target audience, maximum distance, and area.
    """
    return await accommodation_repo.get_filtered(
        db,
        target_audience=target_audience,
        max_distance_km=max_distance_km,
        area=area,
        skip=skip,
        limit=limit
    )

@router.get("/{id}", response_model=AccommodationResponse)
async def read_accommodation(
    id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a single accommodation by its ID.
    """
    db_accommodation = await accommodation_repo.get(db, id=id)
    if not db_accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accommodation with ID {id} not found"
        )
    return db_accommodation

@router.post("/", response_model=AccommodationResponse, status_code=status.HTTP_201_CREATED)
async def create_accommodation(
    accommodation_in: AccommodationCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new accommodation.
    """
    return await accommodation_repo.create(db, obj_in=accommodation_in)

@router.put("/{id}", response_model=AccommodationResponse)
async def update_accommodation(
    id: UUID,
    accommodation_in: AccommodationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing accommodation by its ID.
    """
    db_accommodation = await accommodation_repo.get(db, id=id)
    if not db_accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accommodation with ID {id} not found"
        )
    return await accommodation_repo.update(db, db_obj=db_accommodation, obj_in=accommodation_in)

@router.delete("/{id}", response_model=AccommodationResponse)
async def delete_accommodation(
    id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an accommodation by its ID.
    """
    db_accommodation = await accommodation_repo.get(db, id=id)
    if not db_accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Accommodation with ID {id} not found"
        )
    return await accommodation_repo.delete(db, id=id)
