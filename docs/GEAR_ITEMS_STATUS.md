# Gear Items Status Report

## Summary

**Total Items in Database:** 4,509  
**Items with Equipment Stats:** 1,892  
**Items without Stats:** 2,617 (non-equipable items like consumables, materials, etc.)

## Items by Slot (with stats)

- **Weapon:** 379 items
- **Head:** 297 items  
- **Body:** 227 items
- **Legs:** 227 items
- **Cape:** 91 items
- **Neck:** 80 items
- **Ring:** 37 items
- **Hands:** 80 items
- **Feet:** 87 items
- **Shield:** 107 items
- **Ammo:** 160 items

## Common Items Status

**Found:** 109/162 commonly used items (67%)  
**Missing:** 29 items  
**Missing Stats:** 24 items (exist but need stats populated)

## Known Issues

### Missing Items
Some items are not in the database, likely because:
- They have different names in the Wiki API vs game
- They are newer items not yet in the mapping
- They are quest/achievement rewards with special names

Examples:
- Abyssal tentacle (may be named differently)
- Trident of the swamp (may be "Toxic trident" or variant)
- Fighter torso (quest reward, may have different name)
- Fire cape, Infernal cape (may be named differently)
- Ava's accumulator/assembler (may have different names)

### Items Without Stats
Some items exist but don't have equipment stats populated. These are typically:
- Newer items (Torva, Masori, Virtus, new rings)
- Variant items (uncharged, inactive, empty versions)
- Items that OSRSBox database may not have updated yet

Examples:
- Torva full helm, platebody, platelegs
- Masori mask, body, chaps
- Virtus mask, robe top, robe bottom
- Ultor ring, Bellator ring, Venator ring, Magus ring
- Tumeken's shadow (uncharged)
- Toxic blowpipe (empty)

## Solutions

### Automatic Sync
The application now automatically:
1. Syncs items from Wiki API on first startup (if DB is empty)
2. Imports equipment stats from OSRSBox after items are synced
3. Checks for items without stats and imports them on startup

### Manual Sync
To manually sync item stats:
```bash
# Via API endpoint
POST /api/v1/admin/sync-stats

# Or via script
poetry run python backend/scripts/sync_all_items.py
```

### Verification
To check item status:
```bash
poetry run python backend/scripts/check_gear_items.py
```

## Recommendations

1. **For Missing Items:** Check Wiki API for exact names - some items may have variant names (e.g., "Blade of saeldor (inactive)" instead of "Blade of saeldor")

2. **For Items Without Stats:** 
   - Run the sync-stats endpoint periodically to catch new items
   - Some newer items may not be in OSRSBox yet - these will be added as OSRSBox updates

3. **Item Picker:** The item picker now shows all items with stats, sorted by relevance. Users can search by name to find items even if they have variant names.

4. **DPS Calculation:** Works with all items that have equipment stats. Items without stats won't appear in suggestions but won't break the system.

## Current Coverage

The database has good coverage of commonly used items:
- ✅ Most melee weapons (whips, scimitars, godswords, etc.)
- ✅ Most ranged weapons (bows, crossbows, blowpipe variants)
- ✅ Most magic weapons (staves, tridents, wands)
- ✅ Most armor sets (Bandos, Armadyl, Ancestral, etc.)
- ✅ Most accessories (capes, amulets, rings, boots, gloves)

The system is functional for DPS calculations and gear comparisons with the items that have stats populated.
