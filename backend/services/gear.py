"""Gear calculator service."""
import json
from typing import Optional, List, Dict, Set
from sqlmodel import Session, select
from sqlalchemy import func, and_, or_

from backend.models import GearSet, Item, PriceSnapshot
from backend.services.wiki_client import WikiClient
from backend.services.gear_presets import GEAR_PRESETS
from backend.services.wiki_data import WIKI_PROGRESSION


class GearService:
    """Service for managing gear sets."""

    def __init__(self, session: Session) -> None:
        """Initialize gear service."""
        self.session = session
        self.wiki_client = WikiClient()

    async def create_gear_set(
        self, name: str, items: dict[int, int], description: Optional[str] = None
    ) -> GearSet:
        """
        Create a new gear set.

        Args:
            name: Name of the gear set
            items: Dict of item_id -> quantity
            description: Optional description

        Returns:
            Created gear set
        """
        # Calculate total cost
        total_cost = 0
        for item_id, quantity in items.items():
            item_info = await self.wiki_client.get_item_info(item_id)
            if item_info:
                total_cost += item_info.get("price", 0) * quantity

        gear_set = GearSet(
            name=name,
            description=description,
            items=json.dumps(items),
            total_cost=total_cost,
        )

        self.session.add(gear_set)
        self.session.commit()
        self.session.refresh(gear_set)

        return gear_set

    def get_all_gear_sets(self) -> list[GearSet]:
        """
        Get all gear sets.

        Returns:
            List of all gear sets
        """
        statement = select(GearSet).order_by(GearSet.created_at.desc())
        return list(self.session.exec(statement).all())

    def get_gear_set_by_id(self, gear_set_id: int) -> Optional[GearSet]:
        """
        Get gear set by ID.

        Args:
            gear_set_id: Gear set ID

        Returns:
            Gear set or None if not found
        """
        return self.session.get(GearSet, gear_set_id)

    def delete_gear_set(self, gear_set_id: int) -> bool:
        """
        Delete a gear set.

        Args:
            gear_set_id: Gear set ID

        Returns:
            True if deleted, False if not found
        """
        gear_set = self.session.get(GearSet, gear_set_id)
        if gear_set:
            self.session.delete(gear_set)
            self.session.commit()
            return True
        return False

    def suggest_gear(
        self,
        slot: str,
        combat_style: str = "melee",
        budget_per_slot: int = 10_000_000,
        defence_level: int = 99
    ) -> List[Dict]:
        """
        Suggest items for a specific slot based on style and budget.

        Args:
            slot: Equipment slot (head, cape, neck, etc.)
            combat_style: Combat style (melee, ranged, magic, prayer)
            budget_per_slot: Budget per slot (for future use)
            defence_level: Defence level requirement filter

        Returns:
            List of suggested items with scores
        """
        query = select(Item).where(Item.slot == slot)
        
        # Filter by requirements
        query = query.where(Item.defence_req <= defence_level)
        
        # Filter by Budget (using Value as proxy if price missing, or join PriceSnapshot)
        # For MVP, we ignore price here, assuming user checks Flip Finder
        
        items = self.session.exec(query).all()
        
        # Sort Logic
        scored_items = []
        for item in items:
            score = 0
            if combat_style == "melee":
                score = item.melee_strength * 4 + item.attack_slash
            elif combat_style == "ranged":
                score = item.ranged_strength * 4 + item.attack_ranged
            elif combat_style == "magic":
                score = item.magic_damage * 10 + item.attack_magic
            elif combat_style == "prayer":
                score = item.prayer_bonus
            
            if score > 0:
                scored_items.append({
                    "id": item.id,
                    "name": item.name,
                    "score": score,
                    "stats": {
                        "str": item.melee_strength,
                        "pray": item.prayer_bonus
                    },
                    "icon": item.icon_url
                })
                
        # Return top 10
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        return scored_items[:10]

    def _find_item_by_name(self, item_name: str) -> Optional[Item]:
        """
        Find an item by name (case-insensitive, partial match).
        
        Args:
            item_name: Item name to search for
            
        Returns:
            Item if found, None otherwise
        """
        # Try exact match first (case-insensitive) - using LOWER for SQLite compatibility
        items = self.session.exec(
            select(Item).where(func.lower(Item.name) == item_name.lower())
        ).all()
        
        if items:
            return items[0]
        
        # Try partial match (case-insensitive)
        items = self.session.exec(
            select(Item).where(func.lower(Item.name).like(f"%{item_name.lower()}%"))
        ).all()
        
        if items:
            # Return the first match (prefer shorter names for better matches)
            return min(items, key=lambda x: len(x.name))
        
        return None

    def get_preset_loadout(
        self, combat_style: str, tier: str
    ) -> Dict:
        """
        Get a full loadout for a specific combat style and tier.
        
        Args:
            combat_style: Combat style (melee, ranged, magic)
            tier: Tier level (low, mid, high)
            
        Returns:
            Dictionary with loadout information including items, stats, and total cost
        """
        # Validate inputs
        if combat_style not in GEAR_PRESETS:
            raise ValueError(f"Invalid combat style: {combat_style}. Must be one of {list(GEAR_PRESETS.keys())}")
        
        if tier not in GEAR_PRESETS[combat_style]:
            raise ValueError(f"Invalid tier: {tier}. Must be one of {list(GEAR_PRESETS[combat_style].keys())}")
        
        preset = GEAR_PRESETS[combat_style][tier]
        loadout = {
            "combat_style": combat_style,
            "tier": tier,
            "slots": {},
            "total_cost": 0,
            "missing_items": []
        }
        
        # Process each slot
        for slot, item_names in preset.items():
            if not item_names:  # Empty slot (e.g., shield for 2H weapons)
                loadout["slots"][slot] = None
                continue
            
            # Try to find the first available item from the list
            item = None
            for item_name in item_names:
                found_item = self._find_item_by_name(item_name)
                if found_item:
                    item = found_item
                    break
            
            if item:
                # Get price information
                price_snapshot = self.session.exec(
                    select(PriceSnapshot).where(PriceSnapshot.item_id == item.id)
                ).first()
                
                item_price = price_snapshot.high_price if price_snapshot else item.value or 0
                loadout["total_cost"] += item_price
                
                # Build item details
                item_data = {
                    "id": item.id,
                    "name": item.name,
                    "icon_url": item.icon_url,
                    "price": item_price,
                    "slot": item.slot,
                    "requirements": {
                        "attack": item.attack_req,
                        "strength": item.strength_req,
                        "defence": item.defence_req,
                        "ranged": item.ranged_req,
                        "magic": item.magic_req,
                        "prayer": item.prayer_req,
                        "slayer": item.slayer_req
                    },
                    "offensive_stats": {
                        "attack_stab": item.attack_stab,
                        "attack_slash": item.attack_slash,
                        "attack_crush": item.attack_crush,
                        "attack_magic": item.attack_magic,
                        "attack_ranged": item.attack_ranged
                    },
                    "strength_bonuses": {
                        "melee_strength": item.melee_strength,
                        "ranged_strength": item.ranged_strength,
                        "magic_damage": item.magic_damage,
                        "prayer_bonus": item.prayer_bonus
                    },
                    "defensive_stats": {
                        "defence_stab": item.defence_stab,
                        "defence_slash": item.defence_slash,
                        "defence_crush": item.defence_crush,
                        "defence_magic": item.defence_magic,
                        "defence_ranged": item.defence_ranged
                    }
                }
                
                loadout["slots"][slot] = item_data
            else:
                # Item not found in database
                loadout["slots"][slot] = None
                loadout["missing_items"].append({
                    "slot": slot,
                    "names": item_names
                })
        
        return loadout

    def get_progression_loadout(self, style: str, tier: str) -> Dict:
        """
        Get a progression loadout for a specific combat style and tier.
        Simplified version that returns basic item information.
        
        Args:
            style: Combat style (melee, ranged, magic)
            tier: Tier level (low, mid, high)
            
        Returns:
            Dictionary with tier, style, and loadout information
        """
        preset = GEAR_PRESETS.get(style, {}).get(tier)
        if not preset:
            return {"error": "Invalid style or tier"}
        
        loadout = {}
        for slot, item_names in preset.items():
            if not item_names:  # Empty slot (e.g., shield for 2H weapons)
                continue
            
            found_item = None
            # Fallback logic: Try 1st item, then 2nd...
            for name in item_names:
                found_item = self._find_item_by_name(name)
                if found_item:
                    break
            
            if found_item:
                loadout[slot] = {
                    "id": found_item.id,
                    "name": found_item.name,
                    "icon": found_item.icon_url,
                }
        
        return {"tier": tier, "style": style, "loadout": loadout}

    def _get_item_price(self, item: Item) -> int:
        """
        Get the current price of an item from PriceSnapshot or fallback to value.
        
        Args:
            item: Item to get price for
            
        Returns:
            Item price in GP
        """
        price_snapshot = self.session.exec(
            select(PriceSnapshot).where(PriceSnapshot.item_id == item.id)
        ).first()
        
        if price_snapshot and price_snapshot.high_price:
            return price_snapshot.high_price
        return item.value or 0

    def _meets_requirements(
        self, 
        item: Item, 
        stats: Dict[str, int],
        quests_completed: Optional[Set[str]] = None,
        achievements_completed: Optional[Set[str]] = None
    ) -> bool:
        """
        Check if item meets all requirements (stats, quests, achievements).
        
        Args:
            item: Item to check
            stats: Dict with stat levels (attack, strength, defence, ranged, magic, prayer)
            quests_completed: Set of completed quest names (optional)
            achievements_completed: Set of completed achievement names (optional)
            
        Returns:
            True if item meets all requirements
        """
        # Check stat requirements
        if stats.get("attack", 1) < item.attack_req:
            return False
        if stats.get("strength", 1) < item.strength_req:
            return False
        if stats.get("defence", 1) < item.defence_req:
            return False
        if stats.get("ranged", 1) < item.ranged_req:
            return False
        if stats.get("magic", 1) < item.magic_req:
            return False
        if stats.get("prayer", 1) < item.prayer_req:
            return False
        
        # Check quest requirement
        if item.quest_req:
            if quests_completed is None or item.quest_req not in quests_completed:
                return False
        
        # Check achievement requirement
        if item.achievement_req:
            if achievements_completed is None or item.achievement_req not in achievements_completed:
                return False
        
        return True

    def _score_item_for_style(self, item: Item, combat_style: str, attack_type: Optional[str] = None) -> float:
        """
        Score an item for a specific combat style.
        
        Args:
            item: Item to score
            combat_style: Combat style (melee, ranged, magic)
            attack_type: For melee, specify attack type (stab, slash, crush)
            
        Returns:
            Score value (higher is better)
        """
        if combat_style == "melee":
            if attack_type == "stab":
                attack_bonus = item.attack_stab
            elif attack_type == "slash":
                attack_bonus = item.attack_slash
            elif attack_type == "crush":
                attack_bonus = item.attack_crush
            else:
                # Default to best melee attack bonus
                attack_bonus = max(item.attack_stab, item.attack_slash, item.attack_crush)
            return item.melee_strength * 4 + attack_bonus
        elif combat_style == "ranged":
            return item.ranged_strength * 4 + item.attack_ranged
        elif combat_style == "magic":
            return item.magic_damage * 10 + item.attack_magic
        elif combat_style == "prayer":
            return item.prayer_bonus * 10
        return 0.0

    def calculate_dps(
        self,
        items: Dict[str, Optional[Item]],
        combat_style: str,
        attack_type: Optional[str] = None,
        player_stats: Optional[Dict[str, int]] = None
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
            return {"dps": 0.0, "max_hit": 0, "attack_speed": 0, "details": {}}
        
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
            accuracy = min(1.0, (effective_attack + total_attack) / (effective_attack + total_attack + 100))
        elif combat_style == "ranged":
            effective_ranged = player_stats.get("ranged", 99) + 8
            accuracy = min(1.0, (effective_ranged + total_attack) / (effective_ranged + total_attack + 100))
        elif combat_style == "magic":
            effective_magic = player_stats.get("magic", 99) + 8
            accuracy = min(1.0, (effective_magic + total_attack) / (effective_magic + total_attack + 100))
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
            "total_strength_bonus": total_strength if combat_style == "melee" else total_ranged_strength,
            "details": {
                "combat_style": combat_style,
                "attack_type": attack_type,
                "player_stats": player_stats
            }
        }

    def get_best_loadout(
        self,
        combat_style: str,
        budget: int,
        stats: Dict[str, int],
        attack_type: Optional[str] = None,
        quests_completed: Optional[Set[str]] = None,
        achievements_completed: Optional[Set[str]] = None,
        exclude_slots: Optional[List[str]] = None
    ) -> Dict:
        """
        Find the best loadout a player can afford/wear based on stats and budget.
        
        Args:
            combat_style: Combat style (melee, ranged, magic)
            budget: Total budget in GP
            stats: Dict with stat levels (attack, strength, defence, ranged, magic, prayer)
            attack_type: For melee, attack type (stab, slash, crush)
            quests_completed: Set of completed quest names
            achievements_completed: Set of completed achievement names
            exclude_slots: List of slots to exclude (e.g., ["shield"] for 2H weapons)
            
        Returns:
            Dict with best loadout, total cost, and DPS
        """
        if exclude_slots is None:
            exclude_slots = []
        
        # Define equipment slots
        slots = ["head", "cape", "neck", "weapon", "body", "shield", "legs", "hands", "feet", "ring", "ammo"]
        slots = [s for s in slots if s not in exclude_slots]
        
        loadout = {}
        total_cost = 0
        remaining_budget = budget
        
        # Get all items for each slot, sorted by score
        for slot in slots:
            query = select(Item).where(Item.slot == slot)
            
            # Filter by requirements
            query = query.where(
                and_(
                    Item.attack_req <= stats.get("attack", 1),
                    Item.strength_req <= stats.get("strength", 1),
                    Item.defence_req <= stats.get("defence", 1),
                    Item.ranged_req <= stats.get("ranged", 1),
                    Item.magic_req <= stats.get("magic", 1),
                    Item.prayer_req <= stats.get("prayer", 1)
                )
            )
            
            items = self.session.exec(query).all()
            
            # Filter by quest/achievement requirements and budget
            valid_items = []
            for item in items:
                if not self._meets_requirements(item, stats, quests_completed, achievements_completed):
                    continue
                
                price = self._get_item_price(item)
                if price <= remaining_budget:
                    score = self._score_item_for_style(item, combat_style, attack_type)
                    valid_items.append((item, price, score))
            
            # Sort by score descending
            valid_items.sort(key=lambda x: x[2], reverse=True)
            
            # Select best item within budget
            if valid_items:
                best_item, price, score = valid_items[0]
                loadout[slot] = best_item
                total_cost += price
                remaining_budget -= price
            else:
                loadout[slot] = None
        
        # Handle 2H weapons (exclude shield if weapon is 2H)
        if loadout.get("weapon") and loadout["weapon"].is_2h:
            loadout["shield"] = None
        
        # Calculate DPS
        dps_info = self.calculate_dps(loadout, combat_style, attack_type, stats)
        
        # Build response
        result = {
            "combat_style": combat_style,
            "total_cost": total_cost,
            "budget_used": budget - remaining_budget,
            "budget_remaining": remaining_budget,
            "dps": dps_info,
            "slots": {}
        }
        
        for slot, item in loadout.items():
            if item:
                price = self._get_item_price(item)
                result["slots"][slot] = {
                    "id": item.id,
                    "name": item.name,
                    "icon_url": item.icon_url,
                    "price": price,
                    "score": self._score_item_for_style(item, combat_style, attack_type)
                }
            else:
                result["slots"][slot] = None
        
        return result

    def get_upgrade_path(
        self,
        current_loadout: Dict[str, Optional[int]],  # slot -> item_id
        combat_style: str,
        budget: int,
        stats: Dict[str, int],
        attack_type: Optional[str] = None,
        quests_completed: Optional[Set[str]] = None,
        achievements_completed: Optional[Set[str]] = None
    ) -> Dict:
        """
        Find the next upgrade path with cost analysis.
        
        Args:
            current_loadout: Dict of slot -> item_id for current gear
            combat_style: Combat style (melee, ranged, magic)
            budget: Available budget for upgrades
            stats: Dict with stat levels
            attack_type: For melee, attack type (stab, slash, crush)
            quests_completed: Set of completed quest names
            achievements_completed: Set of completed achievement names
            
        Returns:
            Dict with upgrade recommendations per slot
        """
        upgrades = {}
        
        for slot, current_item_id in current_loadout.items():
            if current_item_id is None:
                continue
            
            current_item = self.session.get(Item, current_item_id)
            if not current_item:
                continue
            
            current_score = self._score_item_for_style(current_item, combat_style, attack_type)
            current_price = self._get_item_price(current_item)
            
            # Find better items in same slot
            query = select(Item).where(
                and_(
                    Item.slot == slot,
                    Item.attack_req <= stats.get("attack", 1),
                    Item.strength_req <= stats.get("strength", 1),
                    Item.defence_req <= stats.get("defence", 1),
                    Item.ranged_req <= stats.get("ranged", 1),
                    Item.magic_req <= stats.get("magic", 1),
                    Item.prayer_req <= stats.get("prayer", 1)
                )
            )
            
            items = self.session.exec(query).all()
            
            better_items = []
            for item in items:
                if not self._meets_requirements(item, stats, quests_completed, achievements_completed):
                    continue
                
                score = self._score_item_for_style(item, combat_style, attack_type)
                if score > current_score:
                    price = self._get_item_price(item)
                    upgrade_cost = price - current_price
                    if upgrade_cost <= budget:
                        better_items.append({
                            "item": item,
                            "score": score,
                            "price": price,
                            "upgrade_cost": upgrade_cost,
                            "score_improvement": score - current_score
                        })
            
            # Sort by score improvement per GP
            better_items.sort(
                key=lambda x: x["score_improvement"] / max(x["upgrade_cost"], 1),
                reverse=True
            )
            
            if better_items:
                best_upgrade = better_items[0]
                upgrades[slot] = {
                    "current": {
                        "id": current_item.id,
                        "name": current_item.name,
                        "score": current_score,
                        "price": current_price
                    },
                    "recommended": {
                        "id": best_upgrade["item"].id,
                        "name": best_upgrade["item"].name,
                        "icon_url": best_upgrade["item"].icon_url,
                        "score": best_upgrade["score"],
                        "price": best_upgrade["price"],
                        "upgrade_cost": best_upgrade["upgrade_cost"],
                        "score_improvement": best_upgrade["score_improvement"],
                        "efficiency": round(best_upgrade["score_improvement"] / max(best_upgrade["upgrade_cost"], 1), 4)
                    },
                    "alternatives": [
                        {
                            "id": alt["item"].id,
                            "name": alt["item"].name,
                            "icon_url": alt["item"].icon_url,
                            "score": alt["score"],
                            "price": alt["price"],
                            "upgrade_cost": alt["upgrade_cost"],
                            "score_improvement": alt["score_improvement"]
                        }
                        for alt in better_items[1:6]  # Top 5 alternatives
                    ]
                }
        
        return {
            "combat_style": combat_style,
            "upgrades": upgrades,
            "total_upgrade_cost": sum(
                upgrade["recommended"]["upgrade_cost"]
                for upgrade in upgrades.values()
            )
        }

    def get_alternatives(
        self,
        slot: str,
        combat_style: str,
        budget: Optional[int] = None,
        stats: Optional[Dict[str, int]] = None,
        attack_type: Optional[str] = None,
        quests_completed: Optional[Set[str]] = None,
        achievements_completed: Optional[Set[str]] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get alternative items for a specific slot.
        
        Args:
            slot: Equipment slot
            combat_style: Combat style (melee, ranged, magic)
            budget: Optional budget filter
            stats: Optional stat requirements filter
            attack_type: For melee, attack type (stab, slash, crush)
            quests_completed: Set of completed quest names
            achievements_completed: Set of completed achievement names
            limit: Maximum number of alternatives to return
            
        Returns:
            List of alternative items sorted by score
        """
        query = select(Item).where(Item.slot == slot)
        
        if stats:
            query = query.where(
                and_(
                    Item.attack_req <= stats.get("attack", 1),
                    Item.strength_req <= stats.get("strength", 1),
                    Item.defence_req <= stats.get("defence", 1),
                    Item.ranged_req <= stats.get("ranged", 1),
                    Item.magic_req <= stats.get("magic", 1),
                    Item.prayer_req <= stats.get("prayer", 1)
                )
            )
        
        items = self.session.exec(query).all()
        
        alternatives = []
        for item in items:
            if stats and not self._meets_requirements(item, stats, quests_completed, achievements_completed):
                continue
            
            price = self._get_item_price(item)
            if budget and price > budget:
                continue
            
            score = self._score_item_for_style(item, combat_style, attack_type)
            if score > 0:
                alternatives.append({
                    "id": item.id,
                    "name": item.name,
                    "icon_url": item.icon_url,
                    "price": price,
                    "score": score,
                    "requirements": {
                        "attack": item.attack_req,
                        "strength": item.strength_req,
                        "defence": item.defence_req,
                        "ranged": item.ranged_req,
                        "magic": item.magic_req,
                        "prayer": item.prayer_req,
                        "quest": item.quest_req,
                        "achievement": item.achievement_req
                    },
                    "stats": {
                        "melee_strength": item.melee_strength,
                        "ranged_strength": item.ranged_strength,
                        "magic_damage": item.magic_damage,
                        "prayer_bonus": item.prayer_bonus
                    }
                })
        
        # Sort by score descending
        alternatives.sort(key=lambda x: x["score"], reverse=True)
        return alternatives[:limit]

    def get_wiki_progression(self, style: str) -> dict:
        """
        Returns the exact Wiki table structure, enriched with Price/Icon data.
        
        Args:
            style: Combat style (melee, ranged, magic)
            
        Returns:
            Dictionary with enriched progression data for all slots
        """
        data = WIKI_PROGRESSION.get(style, {})
        enriched_data = {}
        
        for slot, tiers in data.items():
            enriched_tiers = []
            for tier_group in tiers:
                items_data = []
                for item_name in tier_group["items"]:
                    # Try to find item by name (case-insensitive, partial match)
                    item = self._find_item_by_name(item_name)
                    
                    if item:
                        # Get price from PriceSnapshot or fallback to value
                        price = self._get_item_price(item)
                        
                        # Generate wiki URL
                        wiki_name = item.name.replace(" ", "_").replace("'", "%27")
                        wiki_url = f"https://oldschool.runescape.wiki/w/{wiki_name}"
                        
                        items_data.append({
                            "id": item.id,
                            "name": item.name,
                            "icon": item.icon_url,
                            "price": price,
                            "wiki_url": wiki_url,
                            "requirements": {
                                "attack": item.attack_req,
                                "strength": item.strength_req,
                                "defence": item.defence_req,
                                "ranged": item.ranged_req,
                                "magic": item.magic_req,
                                "prayer": item.prayer_req,
                                "quest": item.quest_req,
                                "achievement": item.achievement_req
                            },
                            "stats": {
                                "melee_strength": item.melee_strength,
                                "ranged_strength": item.ranged_strength,
                                "magic_damage": item.magic_damage,
                                "prayer_bonus": item.prayer_bonus,
                                "attack_stab": item.attack_stab,
                                "attack_slash": item.attack_slash,
                                "attack_crush": item.attack_crush,
                                "attack_magic": item.attack_magic,
                                "attack_ranged": item.attack_ranged
                            }
                        })
                    else:
                        # Fallback if item not in DB (generate icon URL manually)
                        safe_name = item_name.replace(" ", "_").replace("'", "%27")
                        wiki_name = item_name.replace(" ", "_").replace("'", "%27")
                        items_data.append({
                            "id": None,
                            "name": item_name,
                            "icon": f"https://oldschool.runescape.wiki/images/{safe_name}_detail.png?0",
                            "price": None,
                            "wiki_url": f"https://oldschool.runescape.wiki/w/{wiki_name}",
                            "requirements": None,
                            "stats": None,
                            "not_found": True
                        })
                
                enriched_tiers.append({
                    "tier": tier_group["tier"],
                    "items": items_data
                })
            enriched_data[slot] = enriched_tiers
            
        return enriched_data
