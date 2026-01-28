"""Data transformation mappers for gear API responses."""

from typing import Dict, List, Any


def map_gear_set_to_response(gear_set) -> Dict[str, Any]:
    """
    Map GearSet model to GearSetResponse schema.

    Args:
        gear_set: GearSet SQLModel instance

    Returns:
        Dictionary matching GearSetResponse schema
    """
    import json

    # Parse JSON and convert string keys to integers (JSON keys are always strings)
    items_dict = json.loads(gear_set.items)
    items_with_int_keys = {int(k): int(v) for k, v in items_dict.items()}

    return {
        "id": gear_set.id or 0,
        "name": gear_set.name,
        "description": gear_set.description,
        "items": items_with_int_keys,
        "total_cost": gear_set.total_cost,
        "created_at": gear_set.created_at.isoformat(),
        "updated_at": gear_set.updated_at.isoformat(),
    }


def transform_progression_data(enriched_data: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
    """
    Transform enriched progression data to match frontend expectations.

    Args:
        enriched_data: Raw enriched progression data from service

    Returns:
        Transformed data with consistent field names
    """
    transformed_data = {}
    for slot, tiers in enriched_data.items():
        transformed_tiers = []
        for tier_data in tiers:
            transformed_items = []
            for item in tier_data["items"]:
                transformed_items.append(
                    {
                        "name": item["name"],
                        "id": item["id"],
                        "icon_url": item.get("icon") or item.get("icon_url"),
                        "price": item["price"],
                        "wiki_url": item["wiki_url"],
                        "requirements": item.get("requirements"),
                        "stats": item.get("stats"),
                        "not_found": item.get("not_found", False),
                    }
                )
            transformed_tiers.append({"tier": tier_data["tier"], "items": transformed_items})
        transformed_data[slot] = transformed_tiers

    return transformed_data


def transform_slot_progression_data(enriched_data: Dict[str, List[Dict]], slot: str) -> List[Dict]:
    """
    Transform slot-specific progression data.

    Args:
        enriched_data: Raw enriched progression data from service
        slot: Equipment slot name

    Returns:
        Transformed tier list for the slot
    """
    tiers = enriched_data[slot]
    transformed_tiers = []
    for tier_data in tiers:
        transformed_items = []
        for item in tier_data["items"]:
            transformed_items.append(
                {
                    "name": item["name"],
                    "id": item["id"],
                    "icon_url": item.get("icon") or item.get("icon_url"),
                    "price": item["price"],
                    "wiki_url": item["wiki_url"],
                    "requirements": item.get("requirements"),
                    "stats": item.get("stats"),
                    "not_found": item.get("not_found", False),
                }
            )
        transformed_tiers.append({"tier": tier_data["tier"], "items": transformed_items})

    return transformed_tiers
