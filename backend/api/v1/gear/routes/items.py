"""Item lookup endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel

from backend.db.session import get_session
from backend.models import Item
from backend.services.gear.pricing import get_item_price


router = APIRouter()


class ItemResponse(BaseModel):
    """Response model for item data."""

    id: int
    name: str
    icon_url: Optional[str] = None
    price: int
    slot: Optional[str] = None
    members: bool = True
    value: int = 0
    stats: dict = {}
    requirements: dict = {}

    class Config:
        """Pydantic config."""

        from_attributes = True


@router.get("/gear/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, session: Session = Depends(get_session)) -> ItemResponse:
    """
    Get item details by ID.

    Args:
        item_id: Item ID
        session: Database session

    Returns:
        Item details including name, icon, price, stats, and requirements
    """
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )

    price = get_item_price(session, item)

    return ItemResponse(
        id=item.id,
        name=item.name,
        icon_url=item.icon_url,
        price=price,
        slot=item.slot,
        members=item.members,
        value=item.value,
        stats={
            "attack_stab": item.attack_stab,
            "attack_slash": item.attack_slash,
            "attack_crush": item.attack_crush,
            "attack_magic": item.attack_magic,
            "attack_ranged": item.attack_ranged,
            "melee_strength": item.melee_strength,
            "ranged_strength": item.ranged_strength,
            "magic_damage": item.magic_damage,
            "prayer_bonus": item.prayer_bonus,
            "defence_stab": item.defence_stab,
            "defence_slash": item.defence_slash,
            "defence_crush": item.defence_crush,
            "defence_magic": item.defence_magic,
            "defence_ranged": item.defence_ranged,
        },
        requirements={
            "attack": item.attack_req,
            "strength": item.strength_req,
            "defence": item.defence_req,
            "ranged": item.ranged_req,
            "magic": item.magic_req,
            "prayer": item.prayer_req,
            "quest": item.quest_req,
            "achievement": item.achievement_req,
        },
    )
