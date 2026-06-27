from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.food_service import FoodServiceType
from app.schemas.food_service import (
    FoodServiceResponse,
    FoodServiceCreate,
    FoodServiceUpdate,
)
from app.repositories.food_service import food_service_repo

router = APIRouter()

@router.get("/", response_model=List[FoodServiceResponse])
async def read_food_services(
    service_type: Optional[FoodServiceType] = Query(None, alias="type", description="Filter by type of food service (Tiffin, Dhaba, Bhojnalaya)"),
    area: Optional[str] = Query(None, description="Filter by area location (case-insensitive match)"),
    skip: int = Query(0, ge=0, description="Skip offset pagination"),
    limit: int = Query(100, ge=1, le=100, description="Limit response size"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of food services.
    Supports filtering by type and area.
    """
    return await food_service_repo.get_filtered(
        db,
        service_type=service_type,
        area=area,
        skip=skip,
        limit=limit
    )

@router.get("/{id}", response_model=FoodServiceResponse)
async def read_food_service(
    id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a single food service by its ID.
    """
    db_food_service = await food_service_repo.get(db, id=id)
    if not db_food_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food service with ID {id} not found"
        )
    return db_food_service

@router.post("/", response_model=FoodServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_food_service(
    food_service_in: FoodServiceCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new food service.
    """
    return await food_service_repo.create(db, obj_in=food_service_in)

@router.put("/{id}", response_model=FoodServiceResponse)
async def update_food_service(
    id: UUID,
    food_service_in: FoodServiceUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing food service by its ID.
    """
    db_food_service = await food_service_repo.get(db, id=id)
    if not db_food_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food service with ID {id} not found"
        )
    return await food_service_repo.update(db, db_obj=db_food_service, obj_in=food_service_in)

@router.delete("/{id}", response_model=FoodServiceResponse)
async def delete_food_service(
    id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a food service by its ID.
    """
    db_food_service = await food_service_repo.get(db, id=id)
    if not db_food_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food service with ID {id} not found"
        )
    return await food_service_repo.delete(db, id=id)
