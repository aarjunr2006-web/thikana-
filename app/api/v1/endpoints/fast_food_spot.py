from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.fast_food_spot import (
    FastFoodSpotResponse,
    FastFoodSpotCreate,
    FastFoodSpotUpdate,
)
from app.repositories.fast_food_spot import fast_food_spot_repo

router = APIRouter()

@router.get("/", response_model=List[FastFoodSpotResponse])
async def read_fast_food_spots(
    area: Optional[str] = Query(None, description="Filter by area location (case-insensitive match)"),
    max_cost_for_two: Optional[int] = Query(None, ge=0, description="Filter by maximum average cost for two people"),
    skip: int = Query(0, ge=0, description="Skip offset pagination"),
    limit: int = Query(100, ge=1, le=100, description="Limit response size"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of fast food spots.
    Supports filtering by area and max average cost for two.
    """
    return await fast_food_spot_repo.get_filtered(
        db,
        area=area,
        max_cost_for_two=max_cost_for_two,
        skip=skip,
        limit=limit
    )

@router.get("/{id}", response_model=FastFoodSpotResponse)
async def read_fast_food_spot(
    id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a single fast food spot by its ID.
    """
    db_spot = await fast_food_spot_repo.get(db, id=id)
    if not db_spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fast food spot with ID {id} not found"
        )
    return db_spot

@router.post("/", response_model=FastFoodSpotResponse, status_code=status.HTTP_201_CREATED)
async def create_fast_food_spot(
    spot_in: FastFoodSpotCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new fast food spot.
    """
    return await fast_food_spot_repo.create(db, obj_in=spot_in)

@router.put("/{id}", response_model=FastFoodSpotResponse)
async def update_fast_food_spot(
    id: UUID,
    spot_in: FastFoodSpotUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing fast food spot by its ID.
    """
    db_spot = await fast_food_spot_repo.get(db, id=id)
    if not db_spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fast food spot with ID {id} not found"
        )
    return await fast_food_spot_repo.update(db, db_obj=db_spot, obj_in=spot_in)

@router.delete("/{id}", response_model=FastFoodSpotResponse)
async def delete_fast_food_spot(
    id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a fast food spot by its ID.
    """
    db_spot = await fast_food_spot_repo.get(db, id=id)
    if not db_spot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fast food spot with ID {id} not found"
        )
    return await fast_food_spot_repo.delete(db, id=id)
