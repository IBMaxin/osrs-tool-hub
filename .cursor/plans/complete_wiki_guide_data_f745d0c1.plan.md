---
name: Complete Wiki Guide Data
overview: Curate complete gear progression data for all three combat styles (Magic, Melee, Ranged) from OSRS Wiki PDFs, populating all tiers, content-specific tables, and bonus tables to achieve full feature completion.
todos:
  - id: magic-late-end-game
    content: Curate Magic Late Game and End Game tiers + content_specific from PDF
    status: pending
  - id: magic-bonus-table
    content: Curate Magic bonus_table from PDF's comparison section
    status: pending
  - id: ranged-mid-late-end-game
    content: Curate Ranged Mid/Late/End Game tiers + content_specific from PDF
    status: pending
  - id: ranged-bonus-table
    content: Curate Ranged bonus_table from PDF's comparison section
    status: pending
  - id: melee-all-remaining
    content: Curate Melee Mid/Late/End Game tiers + content_specific + early game content_specific from PDF
    status: pending
  - id: melee-bonus-table
    content: Curate Melee bonus_table from PDF's comparison section
    status: pending
  - id: verify-all-images
    content: Test all three styles in UI, add icon_override for any broken/mismatched images
    status: pending
  - id: final-wiki-comparison
    content: Side-by-side verification with wiki pages - confirm exact match for all styles
    status: pending
isProject: false
---

# Complete OSRS Wiki Gear Progression Data Curation

## Overview

The technical implementation is complete and working. The remaining work is **data curation** - transcribing all tier loadouts, content-specific equipment tables, and bonus comparison tables from the OSRS Wiki PDFs into the three guide JSON files.

## Source References (OSRS Wiki)

Use these as the authoritative source of truth for data curation:

- **Magic Gear Progression**: https://oldschool.runescape.wiki/w/Optimal_quest_guide/Magic_progression
- **Melee Gear Progression**: https://oldschool.runescape.wiki/w/Optimal_quest_guide/Melee_progression
- **Ranged Gear Progression**: https://oldschool.runescape.wiki/w/Optimal_quest_guide/Ranged_progression

These wiki pages contain the exact tier tables, equipment interfaces, content-specific recommendations, and bonus comparisons that must be mirrored in the app.

**Note**: You also have local PDFs of these guides which may be used as offline references if needed.

## Current State

### Magic ([backend/data/wiki_progression/magic_guide.json](backend/data/wiki_progression/magic_guide.json))

- Early Game: 1 tier (Level 1) with 4 content_specific rows ✓
- Mid Game: 2 tiers (Level 20, 40) with 2 content_specific rows ✓
- Late Game: Empty (needs tiers + content_specific)
- End Game: Empty (needs tiers + content_specific)
- bonus_table: Empty (needs all comparison rows)

### Ranged ([backend/data/wiki_progression/ranged_guide.json](backend/data/wiki_progression/ranged_guide.json))

- Free-to-play: 1 tier (Level 1) with 1 content_specific row ✓
- Mid Game: Empty (needs tiers + content_specific)
- Late Game: Empty (needs tiers + content_specific)
- End Game: Empty (needs tiers + content_specific)
- bonus_table: Empty (needs all comparison rows)

### Melee ([backend/data/wiki_progression/melee_guide.json](backend/data/wiki_progression/melee_guide.json))

- Early Game: 1 tier (Level 1) with 0 content_specific rows
- Mid Game: Empty (needs tiers + content_specific)
- Late Game: Empty (needs tiers + content_specific)
- End Game: Empty (needs tiers + content_specific)
- bonus_table: Empty (needs all comparison rows)

## Data Curation Strategy

### Phase 1: Complete Magic Guide

Magic has the most progress already. Complete it first to establish the pattern:

1. **Late Game section** - Transcribe from PDF:

   - All tier loadouts (likely Level 60, 75+ tiers)
   - Content-specific equipment table rows

2. **End Game section** - Transcribe from PDF:

   - All tier loadouts (likely Level 80+ tiers)
   - Content-specific equipment table rows

3. **Bonus table** - Transcribe from PDF's final comparison section:

   - All rows with item, bonus, cost, delta, cost/delta calculations

### Phase 2: Complete Ranged Guide

1. **Mid Game section** - Transcribe from PDF:

   - All tier loadouts (likely Level 20-60 tiers)
   - Content-specific equipment table rows

2. **Late Game section** - Transcribe from PDF:

   - All tier loadouts (likely Level 60-75 tiers)
   - Content-specific equipment table rows

3. **End Game section** - Transcribe from PDF:

   - All tier loadouts (likely Level 75+ tiers)
   - Content-specific equipment table rows

4. **Bonus table** - Transcribe from PDF's final comparison section

### Phase 3: Complete Melee Guide

1. **Early Game content_specific** - Add any missing rows from PDF

2. **Mid Game section** - Transcribe from PDF:

   - All tier loadouts (likely Level 20-60 tiers)
   - Content-specific equipment table rows

3. **Late Game section** - Transcribe from PDF:

   - All tier loadouts (likely Level 60-75 tiers)
   - Content-specific equipment table rows

4. **End Game section** - Transcribe from PDF:

   - All tier loadouts (likely Level 75+ tiers)
   - Content-specific equipment table rows

5. **Bonus table** - Transcribe from PDF's final comparison section

## Critical Data Rules (Non-Negotiable)

From [.cursor/plans/wiki_guide_full_loadouts_2df51c90.plan.md](.cursor/plans/wiki_guide_full_loadouts_2df51c90.plan.md):

1. **Exact item names**: Must match OSRS Wiki page titles verbatim

   - Include suffixes: `(u)`, `(i)`, `(f)`, etc.
   - Correct: `"Iban's staff (u)"`
   - Wrong: `"Ibans staff"`

2. **icon_override only when needed**: Most items derive image URLs from name

   - Only add `icon_override` when the derived URL doesn't match the wiki icon
   - Example: `"Combat bracelet"` needs `"icon_override": "Combat_bracelet"`

3. **Slot values**: 

   - Occupied: `{ "name": "Item name" }` or `{ "name": "Item name", "icon_override": "Image_Name" }`
   - Empty: `null`

4. **All 11 slots required**: Every tier must have all slots in order:
   ```
   head, cape, neck, ammo, weapon, body, shield, legs, hands, feet, ring
   ```

5. **Costs as integers**: `total_cost`, `cost_buy`, `cost_per_hour` must be numbers (not strings)

## Data Structure Reference

### Tier Object

```json
{
  "label": "Level 60",
  "total_cost": 5000000,
  "slots": {
    "head": { "name": "Ahrim's hood" },
    "cape": { "name": "Imbued god cape" },
    "neck": { "name": "Occult necklace" },
    "ammo": { "name": "Blessing" },
    "weapon": { "name": "Trident of the seas" },
    "body": { "name": "Ahrim's robetop" },
    "shield": null,
    "legs": { "name": "Ahrim's robeskirt" },
    "hands": { "name": "Tormented bracelet" },
    "feet": { "name": "Eternal boots" },
    "ring": { "name": "Seers ring (i)" }
  }
}
```

### Content-Specific Row

```json
{
  "name": "Trident of the swamp (Barrows)",
  "equipment": "Trident of the swamp",
  "use_case": "Barrows",
  "cost_buy": 15000000,
  "cost_per_hour": 180000
}
```

### Bonus Table Row

```json
{
  "item": "Occult necklace",
  "bonus": "+10% magic damage",
  "cost": 500000,
  "delta": "+10%",
  "cost_per_delta": "500K per 10%"
}
```

## Transcription Workflow (Per Section)

For each PDF section being transcribed:

1. **Open PDF side-by-side** with the JSON file in editor
2. **Transcribe tier by tier**:

   - Copy tier label exactly (e.g., "Level 60")
   - Enter total cost from PDF
   - For each slot, enter exact item name from the equipment interface image
   - Leave slot as `null` if empty in the PDF

3. **Transcribe content_specific table**:

   - Copy each row from the "Content Specific Equipment" table
   - Match column names to JSON fields

4. **Add icon_override only if needed**:

   - After initial entry, test the UI to see if images load
   - Add `icon_override` for any broken/wrong images

5. **Save and verify**:

   - Refresh the UI to see the new tier(s)
   - Compare side-by-side with PDF
   - Verify images match exactly

## Verification Checklist

After completing each style's data:

- [ ] All game stage sections have tiers (no empty `"tiers": []`)
- [ ] All tiers have exactly 11 slots in canonical order
- [ ] All item names are exact matches to wiki page titles
- [ ] All costs are integers (no strings, no `null` where cost exists)
- [ ] Content-specific tables populated where PDF shows them
- [ ] Bonus table populated from PDF's comparison section
- [ ] Open app side-by-side with PDF - equipment interfaces match slot-for-slot
- [ ] All item images load correctly (add icon_override where needed)
- [ ] No console errors about missing/invalid items

## Definition of Done

A user can:

1. Open any OSRS Wiki gear progression page (Magic, Melee, or Ranged)
2. Open the app and select the same style
3. See ALL tiers from the wiki represented as equipment interfaces
4. Compare equipment slots side-by-side - same items in same slots
5. See content-specific equipment tables matching the wiki
6. See bonus comparison tables matching the wiki

The app becomes a **complete mirror** of the wiki guides with the superior equipment interface visual layout.

## Code Quality Principles (Already Implemented)

The existing implementation follows strict modularity and maintainability standards:

### Separation of Concerns

- **Data Layer** ([backend/data/wiki_progression/](backend/data/wiki_progression/)): Pure JSON, no logic
- **Service Layer** ([backend/services/wiki_data.py](backend/services/wiki_data.py)): Loads and exposes data without mutation
- **API Layer** ([backend/api/v1/gear/routes/progression.py](backend/api/v1/gear/routes/progression.py)): Thin routes, no business logic
- **Frontend Data** ([frontend/src/lib/api/](frontend/src/lib/api/)): Typed API client, single source of truth for types
- **Frontend UI** ([frontend/src/features/gear/](frontend/src/features/gear/)): Component-based, single responsibility

### Modular Component Architecture

Each component has a single, clear purpose:

- `EquipmentInterface.tsx` - Renders one equipment paperdoll (11 slots + cost)
- `ContentSpecificTable.tsx` - Renders content-specific equipment table
- `BonusTable.tsx` - Renders bonus comparison table  
- `WikiGuideView.tsx` - Orchestrates layout (tabs, accordions, component composition)

### Type Safety

- **Backend**: Type hints everywhere, mypy strict mode
- **Frontend**: TypeScript strict mode, no `any`, typed API contracts
- **Shared contracts**: API types defined once, consumed by frontend

### Testability

- API endpoint has dedicated test suite ([backend/tests/api/v1/gear/routes/test_wiki_guide.py](backend/tests/api/v1/gear/routes/test_wiki_guide.py))
- Tests verify exact JSON structure (no mutation)
- Tests verify slot order enforcement

### Maintainability Features

1. **Single source of truth for slot order**: Defined once in JSON, enforced by code
2. **Explicit image resolution logic**: `getSlotImageUrl` fails loudly on errors (no silent fallbacks)
3. **No magic constants**: Colors, sizes, layout rules documented in components
4. **Clear error boundaries**: Backend/frontend errors are explicit, not swallowed
5. **Minimal diffs**: Changes touch only what's needed (follows AGENTS.md)

**No code changes needed** - the architecture is already clean, modular, and maintainable. Data curation work is isolated to JSON files only.

## Estimated Scope

Based on typical OSRS Wiki progression guides:

- **Magic**: ~8-12 remaining tiers + content_specific rows + bonus_table
- **Ranged**: ~12-16 remaining tiers + content_specific rows + bonus_table
- **Melee**: ~12-16 remaining tiers + content_specific rows + bonus_table

Total: ~35-45 tier loadouts + all supplementary tables

This is primarily **data entry work** - the code is complete and ready to render all data once curated.