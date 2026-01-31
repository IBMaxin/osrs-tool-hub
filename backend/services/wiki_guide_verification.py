"""Wiki guide verification constants and validators.

This module provides canonical constants and pure validation functions
for wiki guide data. Used by tests, services, and optionally load-time checks.

Single source of truth for:
- Slot order (11 equipment slots in canonical order)
- Valid combat styles
- Guide structure requirements
"""

from typing import Any

# Canonical slot order - single source of truth
WIKI_GUIDE_SLOT_ORDER = [
    "head",
    "cape",
    "neck",
    "ammo",
    "weapon",
    "body",
    "shield",
    "legs",
    "hands",
    "feet",
    "ring",
]

# Valid combat styles
WIKI_GUIDE_STYLES = ["magic", "melee", "ranged"]


class WikiGuideValidationError(ValueError):
    """Raised when wiki guide validation fails."""

    pass


def validate_slot_order(slot_order: list[str]) -> None:
    """Validate that slot order matches the canonical order.

    Args:
        slot_order: List of slot names in order.

    Raises:
        WikiGuideValidationError: If slot order doesn't match canonical order.
    """
    if slot_order != WIKI_GUIDE_SLOT_ORDER:
        raise WikiGuideValidationError(
            f"Invalid slot_order: expected {WIKI_GUIDE_SLOT_ORDER}, got {slot_order}"
        )


def validate_guide_root(data: dict[str, Any]) -> None:
    """Validate top-level guide structure.

    Args:
        data: Guide data dictionary.

    Raises:
        WikiGuideValidationError: If required keys are missing or invalid.
    """
    required_keys = ["style", "slot_order", "game_stages", "bonus_table", "cost_per_hour_label"]

    for key in required_keys:
        if key not in data:
            raise WikiGuideValidationError(f"Missing required key: {key}")

    if not isinstance(data["style"], str):
        raise WikiGuideValidationError(f"style must be a string, got {type(data['style'])}")

    if data["style"] not in WIKI_GUIDE_STYLES:
        raise WikiGuideValidationError(
            f"Invalid style: {data['style']}, expected one of {WIKI_GUIDE_STYLES}"
        )

    if not isinstance(data["game_stages"], list):
        raise WikiGuideValidationError(
            f"game_stages must be a list, got {type(data['game_stages'])}"
        )

    if not isinstance(data["bonus_table"], list):
        raise WikiGuideValidationError(
            f"bonus_table must be a list, got {type(data['bonus_table'])}"
        )

    validate_slot_order(data["slot_order"])


def validate_slot_value(slot_value: Any) -> None:
    """Validate a single slot value in a tier.

    Args:
        slot_value: Either None or a dict with 'name' key.

    Raises:
        WikiGuideValidationError: If slot value is invalid.
    """
    if slot_value is None:
        return

    if not isinstance(slot_value, dict):
        raise WikiGuideValidationError(
            f"Slot value must be null or dict, got {type(slot_value)}"
        )

    if "name" not in slot_value:
        raise WikiGuideValidationError(
            f"Slot value missing required 'name' key: {slot_value}"
        )

    if not isinstance(slot_value["name"], str):
        raise WikiGuideValidationError(
            f"Slot 'name' must be a string, got {type(slot_value['name'])}"
        )

    # Optional icon_override validation
    if "icon_override" in slot_value and slot_value["icon_override"] is not None:
        if not isinstance(slot_value["icon_override"], str):
            raise WikiGuideValidationError(
                f"Slot 'icon_override' must be a string or null, got {type(slot_value['icon_override'])}"
            )


def validate_tier(tier: dict[str, Any], slot_order: list[str]) -> None:
    """Validate a tier structure.

    Args:
        tier: Tier dictionary with 'label', 'total_cost', 'slots'.
        slot_order: List of expected slot names in order.

    Raises:
        WikiGuideValidationError: If tier structure is invalid.
    """
    required_keys = ["label", "total_cost", "slots"]

    for key in required_keys:
        if key not in tier:
            raise WikiGuideValidationError(f"Missing required key in tier: {key}")

    if not isinstance(tier["label"], str):
        raise WikiGuideValidationError(f"tier 'label' must be a string, got {type(tier['label'])}")

    if not isinstance(tier["total_cost"], (int, float)):
        raise WikiGuideValidationError(
            f"tier 'total_cost' must be a number, got {type(tier['total_cost'])}"
        )

    if not isinstance(tier["slots"], dict):
        raise WikiGuideValidationError(f"tier 'slots' must be a dict, got {type(tier['slots'])}")

    # Verify all expected slots are present
    for slot_name in slot_order:
        if slot_name not in tier["slots"]:
            raise WikiGuideValidationError(
                f"Tier missing slot '{slot_name}', expected all slots in {slot_order}"
            )

        validate_slot_value(tier["slots"][slot_name])


def validate_game_stage(stage: dict[str, Any], slot_order: list[str]) -> None:
    """Validate a game stage structure.

    Args:
        stage: Stage dictionary with 'id', 'title', 'tiers', 'content_specific'.
        slot_order: List of expected slot names in order.

    Raises:
        WikiGuideValidationError: If stage structure is invalid.
    """
    required_keys = ["id", "title", "tiers", "content_specific"]

    for key in required_keys:
        if key not in stage:
            raise WikiGuideValidationError(f"Missing required key in stage: {key}")

    if not isinstance(stage["id"], str):
        raise WikiGuideValidationError(f"stage 'id' must be a string, got {type(stage['id'])}")

    if not isinstance(stage["title"], str):
        raise WikiGuideValidationError(f"stage 'title' must be a string, got {type(stage['title'])}")

    if not isinstance(stage["tiers"], list):
        raise WikiGuideValidationError(f"stage 'tiers' must be a list, got {type(stage['tiers'])}")

    if not isinstance(stage["content_specific"], list):
        raise WikiGuideValidationError(
            f"stage 'content_specific' must be a list, got {type(stage['content_specific'])}"
        )

    # Validate each tier
    for tier in stage["tiers"]:
        if not isinstance(tier, dict):
            raise WikiGuideValidationError(
                f"Each tier must be a dict, got {type(tier)} in stage {stage['id']}"
            )
        validate_tier(tier, slot_order)

    # Validate content_specific items (we don't validate internal structure beyond being a list)
    for item in stage["content_specific"]:
        if not isinstance(item, dict):
            raise WikiGuideValidationError(
                f"Each content_specific item must be a dict, got {type(item)}"
            )


def validate_bonus_row(row: dict[str, Any]) -> None:
    """Validate a bonus table row.

    Args:
        row: Row dictionary with 'item', 'bonus', and optional 'cost', 'delta', 'cost_per_delta'.

    Raises:
        WikiGuideValidationError: If row structure is invalid.
    """
    if "item" not in row:
        raise WikiGuideValidationError("Bonus row missing required 'item' key")

    if "bonus" not in row:
        raise WikiGuideValidationError("Bonus row missing required 'bonus' key")

    if not isinstance(row["item"], str):
        raise WikiGuideValidationError(f"bonus row 'item' must be a string, got {type(row['item'])}")

    if not isinstance(row["bonus"], str):
        raise WikiGuideValidationError(f"bonus row 'bonus' must be a string, got {type(row['bonus'])}")

    # Optional fields validation
    if "cost" in row and row["cost"] is not None:
        if not isinstance(row["cost"], (int, float)):
            raise WikiGuideValidationError(
                f"bonus row 'cost' must be a number or null, got {type(row['cost'])}"
            )


def validate_guide(data: dict[str, Any]) -> None:
    """Validate a complete guide structure.

    This is the single entry point for validating wiki guide payloads.

    Args:
        data: Complete guide dictionary.

    Raises:
        WikiGuideValidationError: If any part of the guide is invalid.
    """
    validate_guide_root(data)

    slot_order = data["slot_order"]

    # Validate each game stage
    for stage in data["game_stages"]:
        validate_game_stage(stage, slot_order)

    # Validate each bonus row
    for row in data["bonus_table"]:
        if not isinstance(row, dict):
            raise WikiGuideValidationError(
                f"Each bonus_table row must be a dict, got {type(row)}"
            )
        validate_bonus_row(row)
