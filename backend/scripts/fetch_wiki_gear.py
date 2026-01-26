"""Fetch gear progression data from OSRS Wiki using MediaWiki API."""
import httpx
import mwparserfromhell
import asyncio
import json
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

WIKI_API = "https://oldschool.runescape.wiki/api.php"
PAGE_TITLE = "Guide:Melee_gear_progression"

# User agent matching the project config
USER_AGENT = "OSRSToolHub/1.0 (contact: your@email.com)"


def extract_slot_table_data(wikicode: mwparserfromhell.wikicode.Wikicode) -> Dict[str, List[str]]:
    """
    Extract gear items from SlotTable templates.
    
    SlotTable format: {{SlotTable|slot=Head|item1=Helm of neitiznot|item2=Berserker helm|...}}
    
    Args:
        wikicode: Parsed wikitext
        
    Returns:
        Dictionary mapping slots to lists of item names
    """
    gear_data: Dict[str, List[str]] = {}
    
    # Find all SlotTable templates
    for template in wikicode.filter_templates():
        if template.name.strip().lower() == "slottable":
            slot, items = extract_slot_table_items(template)
            if slot and items:
                gear_data[slot.lower()] = items
    
    return gear_data


def clean_item_name(wiki_text: str) -> str:
    """
    Clean wiki text to extract plain item name.
    
    Handles:
    - [[Item Name]] -> Item Name
    - [[Item Name|Display Name]] -> Item Name
    - {{Item Name}} -> Item Name
    - Plain text -> Plain text
    
    Args:
        wiki_text: Raw wiki text
        
    Returns:
        Cleaned item name
    """
    # Remove wiki link formatting [[Item|Display]] -> Item
    wiki_text = re.sub(r'\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]', r'\1', wiki_text)
    
    # Remove template formatting {{Item}} -> Item
    wiki_text = re.sub(r'\{\{([^\}]+)\}\}', r'\1', wiki_text)
    
    # Remove HTML tags
    wiki_text = re.sub(r'<[^>]+>', '', wiki_text)
    
    # Remove extra whitespace
    wiki_text = ' '.join(wiki_text.split())
    
    return wiki_text.strip()


def extract_tier_sections(wikicode: mwparserfromhell.wikicode.Wikicode) -> Dict[str, Dict[str, List[str]]]:
    """
    Extract gear progression organized by tier (Low, Mid, High).
    
    Args:
        wikicode: Parsed wikitext
        
    Returns:
        Dictionary with tier -> slot -> items structure
    """
    tier_data: Dict[str, Dict[str, List[str]]] = {}
    current_tier: Optional[str] = None
    
    # Look for tier headings (== Low ==, == Mid ==, == High ==)
    # Also check for variations like "Low level", "Mid level", etc.
    for node in wikicode.nodes:
        if isinstance(node, mwparserfromhell.nodes.heading.Heading):
            heading_text = str(node.title).strip().lower()
            # Check for tier keywords in heading
            for tier_keyword in ["low", "mid", "high", "bis", "best"]:
                if tier_keyword in heading_text:
                    # Normalize tier name
                    if "low" in heading_text:
                        current_tier = "low"
                    elif "mid" in heading_text or "medium" in heading_text:
                        current_tier = "mid"
                    elif "high" in heading_text or "end" in heading_text:
                        current_tier = "high"
                    elif "bis" in heading_text or "best" in heading_text:
                        current_tier = "high"  # Treat BIS as high tier
                    
                    if current_tier and current_tier not in tier_data:
                        tier_data[current_tier] = {}
                    break
        
        # If we're in a tier section, look for SlotTable templates
        # Also check for templates nested in other structures
        elif current_tier:
            # Handle direct template nodes
            if isinstance(node, mwparserfromhell.nodes.template.Template):
                if node.name.strip().lower() == "slottable":
                    slot, items = extract_slot_table_items(node)
                    if slot and items:
                        tier_data[current_tier][slot] = items
            
            # Handle templates within text nodes
            elif hasattr(node, 'nodes'):
                for subnode in node.nodes:
                    if isinstance(subnode, mwparserfromhell.nodes.template.Template):
                        if subnode.name.strip().lower() == "slottable":
                            slot, items = extract_slot_table_items(subnode)
                            if slot and items:
                                tier_data[current_tier][slot] = items
    
    return tier_data


def extract_slot_table_items(template: mwparserfromhell.nodes.template.Template) -> Tuple[Optional[str], List[str]]:
    """
    Extract slot and items from a SlotTable template.
    
    Args:
        template: SlotTable template node
        
    Returns:
        Tuple of (slot_name, list_of_items)
    """
    slot = None
    items: List[str] = []
    
    for param in template.params:
        param_name = param.name.strip().lower()
        param_value = param.value.strip()
        
        if param_name == "slot":
            slot = param_value.lower()
        elif param_name.startswith("item"):
            item_name = clean_item_name(param_value)
            if item_name:
                items.append(item_name)
    
    return slot, items


async def fetch_gear_guide() -> Dict:
    """
    Fetch and parse the Melee gear progression guide from OSRS Wiki.
    
    Returns:
        Dictionary containing parsed gear progression data
    """
    params = {
        "action": "parse",
        "page": PAGE_TITLE,
        "prop": "wikitext",
        "format": "json"
    }
    
    headers = {"User-Agent": USER_AGENT}
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.get(WIKI_API, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e}")
            raise
        except Exception as e:
            print(f"Error fetching wiki page: {e}")
            raise
    
    if "parse" not in data or "wikitext" not in data["parse"]:
        raise ValueError("Unexpected API response format")
    
    wikitext = data["parse"]["wikitext"]["*"]
    wikicode = mwparserfromhell.parse(wikitext)
    
    # Try to extract tier-based structure first
    tier_data = extract_tier_sections(wikicode)
    
    # If tier extraction didn't work well, fall back to simple SlotTable extraction
    if not tier_data:
        print("Warning: Could not extract tier structure, using simple SlotTable extraction")
        slot_data = extract_slot_table_data(wikicode)
        # Organize into a single tier structure
        tier_data = {"all": slot_data}
    
    return {
        "page_title": PAGE_TITLE,
        "tiers": tier_data,
        "raw_wikitext_preview": wikitext[:1000]  # First 1000 chars for debugging
    }


def convert_to_gear_presets_format(
    tier_data: Dict[str, Dict[str, List[str]]], combat_style: str = "melee"
) -> Dict[str, Dict[str, List[str]]]:
    """
    Convert extracted tier data to gear_presets.py format.
    
    Args:
        tier_data: Dictionary with tier -> slot -> items structure
        combat_style: Combat style name (melee, ranged, magic)
        
    Returns:
        Dictionary in gear_presets.py format
    """
    # Map slot names to standard slot names used in gear_presets.py
    slot_mapping = {
        "head": ["head", "helmet", "helm"],
        "cape": ["cape"],
        "neck": ["neck", "necklace", "amulet"],
        "weapon": ["weapon", "main hand"],
        "ammo": ["ammo", "ammunition", "ammunition slot"],
        "body": ["body", "chest", "torso"],
        "shield": ["shield", "off-hand"],
        "legs": ["legs", "leg"],
        "hands": ["hands", "gloves", "gauntlets"],
        "feet": ["feet", "boots", "foot"],
        "ring": ["ring"]
    }
    
    def normalize_slot(slot_name: str) -> Optional[str]:
        """Normalize slot name to standard format."""
        slot_lower = slot_name.lower()
        for standard_slot, variants in slot_mapping.items():
            if slot_lower in variants:
                return standard_slot
        return None
    
    result: Dict[str, Dict[str, List[str]]] = {}
    
    for tier, slots in tier_data.items():
        normalized_tier = tier.lower()
        if normalized_tier not in ["low", "mid", "high", "bis"]:
            continue
        
        result[normalized_tier] = {}
        
        for slot, items in slots.items():
            normalized_slot = normalize_slot(slot)
            if normalized_slot:
                result[normalized_tier][normalized_slot] = items
    
    return result


async def main():
    """Main entry point."""
    print(f"Fetching gear progression data from: {PAGE_TITLE}")
    print(f"Wiki API: {WIKI_API}\n")
    
    try:
        data = await fetch_gear_guide()
        
        # Print summary
        print("Extracted gear progression data:")
        print(f"  Tiers found: {list(data['tiers'].keys())}")
        for tier, slots in data["tiers"].items():
            print(f"  {tier.upper()}: {len(slots)} slots")
            for slot, items in slots.items():
                print(f"    - {slot}: {len(items)} items")
        
        # Save raw data to JSON file
        output_path = Path(__file__).parent.parent / "gear_progression_raw.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\nRaw data saved to: {output_path}")
        
        # Convert to gear_presets format
        if data["tiers"]:
            preset_format = convert_to_gear_presets_format(data["tiers"], "melee")
            preset_path = Path(__file__).parent.parent / "gear_progression_preset.json"
            with open(preset_path, "w", encoding="utf-8") as f:
                json.dump({"melee": preset_format}, f, indent=2, ensure_ascii=False)
            
            print(f"Preset format saved to: {preset_path}")
            print("\nPreview of preset format:")
            print(json.dumps({"melee": preset_format}, indent=2, ensure_ascii=False)[:800])
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
