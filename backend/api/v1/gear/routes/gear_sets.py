"""Gear set CRUD endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from backend.db.session import get_session
from backend.services.gear import GearService
from backend.api.v1.gear.schemas import GearSetCreate, GearSetResponse
from backend.api.v1.gear.mappers import map_gear_set_to_response

router = APIRouter()


@router.post("/gear", response_model=GearSetResponse, status_code=status.HTTP_201_CREATED)
async def create_gear_set(
    gear_data: GearSetCreate, session: Session = Depends(get_session)
) -> GearSetResponse:
    """
    Create a new gear set.

    Args:
        gear_data: Gear set creation data
        session: Database session

    Returns:
        Created gear set
    """
    service = GearService(session)
    gear_set = await service.create_gear_set(gear_data.name, gear_data.items, gear_data.description)

    return GearSetResponse(**map_gear_set_to_response(gear_set))


@router.get("/gear", response_model=List[GearSetResponse])
async def get_gear_sets(session: Session = Depends(get_session)) -> List[GearSetResponse]:
    """
    Get all gear sets.

    Args:
        session: Database session

    Returns:
        List of all gear sets
    """
    service = GearService(session)
    gear_sets = service.get_all_gear_sets()

    return [GearSetResponse(**map_gear_set_to_response(gs)) for gs in gear_sets]


@router.get("/gear/{gear_set_id}", response_model=GearSetResponse)
async def get_gear_set(
    gear_set_id: int, session: Session = Depends(get_session)
) -> GearSetResponse:
    """
    Get gear set by ID.

    Args:
        gear_set_id: Gear set ID
        session: Database session

    Returns:
        Gear set data
    """
    service = GearService(session)
    gear_set = service.get_gear_set_by_id(gear_set_id)

    if not gear_set:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gear set not found")

    return GearSetResponse(**map_gear_set_to_response(gear_set))


@router.delete("/gear/{gear_set_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gear_set(gear_set_id: int, session: Session = Depends(get_session)) -> None:
    """
    Delete a gear set.

    Args:
        gear_set_id: Gear set ID
        session: Database session
    """
    service = GearService(session)
    deleted = service.delete_gear_set(gear_set_id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gear set not found")
