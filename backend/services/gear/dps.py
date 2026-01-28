"""DPS (Damage Per Second) calculation utilities."""

from typing import Dict, List, Optional

from backend.models import Item


def calculate_dps(
    items: Dict[str, Optional[Item]],
    combat_style: str,
    attack_type: Optional[str] = None,
    player_stats: Optional[Dict[str, int]] = None,
) -> Dict:
    """
    Calculate DPS (Damage Per Second) for a gear loadout.

    Args:
        items: Dict of slot -> Item (e.g., {"weapon": Item(...), "head": Item(...)})
        combat_style: Combat style (melee, ranged, magic)
        attack_type: For melee, attack type (stab, slash, crush)
        player_stats: Player combat stats (attack, strength, ranged, magic)

    Returns:
        Dict with DPS information
    """
    if player_stats is None:
        player_stats = {"attack": 99, "strength": 99, "ranged": 99, "magic": 99}

    weapon = items.get("weapon")
    if not weapon:
        return {
            "dps": 0.0,
            "max_hit": 0,
            "attack_speed": 0,
            "attack_speed_seconds": 0.0,
            "accuracy": 0.0,
            "total_attack_bonus": 0,
            "total_strength_bonus": 0,
            "details": {},
        }

    # Calculate total bonuses from all equipped items
    total_attack = 0
    total_strength = 0
    total_ranged_strength = 0
    total_magic_damage = 0

    for slot, item in items.items():
        if item is None:
            continue
        if combat_style == "melee":
            if attack_type == "stab":
                total_attack += item.attack_stab
            elif attack_type == "slash":
                total_attack += item.attack_slash
            elif attack_type == "crush":
                total_attack += item.attack_crush
            else:
                total_attack += max(item.attack_stab, item.attack_slash, item.attack_crush)
            total_strength += item.melee_strength
        elif combat_style == "ranged":
            total_attack += item.attack_ranged
            total_ranged_strength += item.ranged_strength
        elif combat_style == "magic":
            total_attack += item.attack_magic
            total_magic_damage += item.magic_damage

    # Get attack speed
    attack_speed_ticks = weapon.attack_speed or 4
    attack_speed_seconds = attack_speed_ticks * 0.6  # 1 tick = 0.6 seconds

    # Calculate max hit (simplified formula)
    if combat_style == "melee":
        effective_strength = player_stats.get("strength", 99) + 8
        max_hit = int((effective_strength * (64 + total_strength) + 320) / 640)
    elif combat_style == "ranged":
        effective_ranged = player_stats.get("ranged", 99) + 8
        max_hit = int((effective_ranged * (64 + total_ranged_strength) + 320) / 640)
    elif combat_style == "magic":
        # Magic max hit depends on spell, simplified here
        max_hit = 30  # Placeholder
    else:
        max_hit = 0

    # Calculate accuracy (simplified)
    if combat_style == "melee":
        effective_attack = player_stats.get("attack", 99) + 8
        accuracy = min(
            1.0, (effective_attack + total_attack) / (effective_attack + total_attack + 100)
        )
    elif combat_style == "ranged":
        effective_ranged = player_stats.get("ranged", 99) + 8
        accuracy = min(
            1.0, (effective_ranged + total_attack) / (effective_ranged + total_attack + 100)
        )
    elif combat_style == "magic":
        effective_magic = player_stats.get("magic", 99) + 8
        accuracy = min(
            1.0, (effective_magic + total_attack) / (effective_magic + total_attack + 100)
        )
    else:
        accuracy = 0.0

    # Average damage per hit
    avg_damage = (max_hit / 2) * accuracy

    # DPS = average damage / attack speed in seconds
    dps = avg_damage / attack_speed_seconds if attack_speed_seconds > 0 else 0.0

    return {
        "dps": round(dps, 2),
        "max_hit": max_hit,
        "attack_speed": attack_speed_ticks,
        "attack_speed_seconds": round(attack_speed_seconds, 2),
        "accuracy": round(accuracy * 100, 2),
        "total_attack_bonus": total_attack,
        "total_strength_bonus": (
            total_strength if combat_style == "melee" else total_ranged_strength
        ),
        "details": {
            "combat_style": combat_style,
            "attack_type": attack_type,
            "player_stats": player_stats,
        },
    }


def compare_dps(
    loadouts: List[Dict[str, Dict[str, Optional[Item]]]],
    combat_style: str,
    attack_type: Optional[str] = None,
    player_stats: Optional[Dict[str, int]] = None,
    target_monster: Optional[Dict] = None,
) -> List[Dict]:
    """
    Compare DPS for multiple loadouts side-by-side.

    Args:
        loadouts: List of loadout dictionaries, each with:
            - "name": Loadout name/identifier
            - "loadout": Dict of slot -> Item (e.g., {"weapon": Item(...), "head": Item(...)})
        combat_style: Combat style (melee, ranged, magic)
        attack_type: For melee, attack type (stab, slash, crush)
        player_stats: Player combat stats (attack, strength, ranged, magic)
        target_monster: Optional monster stats for more accurate calculations

    Returns:
        List of DPS results, each containing:
            - "loadout_id": Index of loadout in input list
            - "loadout_name": Name of the loadout
            - "dps": Calculated DPS
            - "max_hit": Maximum hit
            - "accuracy": Accuracy percentage
            - "attack_speed": Attack speed in ticks
            - All other fields from calculate_dps()
    """
    results = []

    for idx, loadout_data in enumerate(loadouts):
        loadout_name = loadout_data.get("name", f"Loadout {idx + 1}")
        loadout = loadout_data.get("loadout", {})

        # Calculate DPS for this loadout
        dps_result = calculate_dps(
            items=loadout,
            combat_style=combat_style,
            attack_type=attack_type,
            player_stats=player_stats,
        )

        # Add loadout identification
        result = {
            "loadout_id": idx,
            "loadout_name": loadout_name,
            **dps_result,
        }

        results.append(result)

    # Calculate marginal gains (DPS increase compared to baseline)
    if len(results) > 1:
        baseline_dps = results[0]["dps"]
        for result in results[1:]:
            dps_increase = result["dps"] - baseline_dps
            dps_increase_percent = (dps_increase / baseline_dps * 100) if baseline_dps > 0 else 0
            result["dps_increase"] = round(dps_increase, 2)
            result["dps_increase_percent"] = round(dps_increase_percent, 2)

    return results
