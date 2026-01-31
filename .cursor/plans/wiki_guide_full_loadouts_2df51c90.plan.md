---
name: Wiki Guide Exact Match
overview: "Implement OSRS Wiki Gear Progression views that exactly mirror the wiki (Magic, Melee, Ranged): slot-for-slot, tier-for-tier, item-for-item, image-for-image. Data from curated JSON only; no scraping."
todos:
  - id: canonical-json-schema
    content: Define and add canonical guide JSON with slot_order, slots as { name, icon_override? }
    status: completed
  - id: backend-load-exact
    content: Loader + GET /gear/wiki-guide/{style}; load JSON exactly, no reorder/substitute/fix
    status: completed
  - id: frontend-image-resolution
    content: "Image URL: icon_override else derive from name else fail loudly (no silent fallback)"
    status: completed
  - id: frontend-paperdoll-layout
    content: Equipment interface paperdoll layout with brown background and in-game slot positions
    status: completed
  - id: frontend-guide-view
    content: WikiGuideView with game stages, tier rows, content_specific table, bonus_table
    status: completed
  - id: curate-json-all-styles
    content: Curate full guide JSON for magic, melee, ranged from wiki/PDFs (exact names)
    status: pending
  - id: tests-and-done
    content: Tests; definition of done = side-by-side with wiki, same icons/slots/order
    status: pending
isProject: false
---

# OSRS Wiki Gear Progression — Exact Match

Implement OSRS Wiki Gear Progression views that **exactly mirror** the OSRS Wiki gear progression pages (Magic, Melee, Ranged). This is **data mirroring and rendering only** — not recommendation logic. Output must match the wiki **slot-for-slot, tier-for-tier, item-for-item, image-for-image**.

---

## Goal

- Mirror the wiki pages exactly.
- A user can open the wiki and this app side-by-side and see the **same gear icons in the same slots in the same order**.
- If any item differs, the implementation is wrong.

---

## Non-Negotiable Rules

| Rule | Meaning |
|------|---------|
| **Exact gear setups only** | Every tier is a canonical loadout from the wiki. Do not infer, optimize, substitute, or "improve" gear. If the wiki shows an item, we show that exact item. If a slot is empty on the wiki, it is empty in the UI. |
| **Wiki is source of truth** | Canonical identifier = **exact OSRS Wiki item name**. Item names must match wiki page titles verbatim (including `(i)`, `(u)`, `(f)`, etc.). Internal DB IDs, prices, or stats are secondary and must not override names. |
| **Images must match the wiki** | Use OSRS Wiki item images. Default: `https://oldschool.runescape.wiki/images/{Wiki_Image_Name}_detail.png`. Some items need explicit image overrides (expected). If the image does not match the wiki icon, it is incorrect. |
| **No scraping** | All data comes from **curated JSON**, transcribed from the wiki/PDFs. The system renders data; it does not fetch or compute it. |

---

## Data Model (Authoritative)

Each guide (magic, melee, ranged) is a **static snapshot**. Slot order is **enforced by code**, not JSON key order.

### Required Slot Order (must never change)

```
head, cape, neck, ammo, weapon, body, shield, legs, hands, feet, ring
```

### JSON Schema (canonical)

- **Never store full URLs in JSON** — only wiki image **base names** when overrides are needed.
- Slot value: `null` (empty) or `{ "name": "Exact wiki item name", "icon_override"?: "Wiki_Image_Base_Name" }`.
- `name` is mandatory when a slot is occupied. `icon_override` is optional; when present, frontend uses it to build the image URL instead of deriving from `name`.

```json
{
  "style": "magic",
  "slot_order": [
    "head", "cape", "neck", "ammo", "weapon", "body", "shield", "legs", "hands", "feet", "ring"
  ],
  "game_stages": [
    {
      "id": "early_game",
      "title": "Early Game / Free-to-play",
      "tiers": [
        {
          "label": "Level 1",
          "total_cost": 9238,
          "slots": {
            "head": { "name": "Blue wizard hat" },
            "cape": { "name": "Black cape" },
            "neck": { "name": "Amulet of magic" },
            "ammo": null,
            "weapon": { "name": "Staff of air" },
            "body": { "name": "Blue wizard robe" },
            "shield": null,
            "legs": { "name": "Zamorak monk bottom" },
            "hands": { "name": "Leather gloves" },
            "feet": { "name": "Leather boots" },
            "ring": null
          }
        }
      ],
      "content_specific": []
    }
  ],
  "bonus_table": []
}
```

### Slot Value Rules

- Occupied slot: `{ "name": "Exact wiki title" }` or `{ "name": "...", "icon_override": "Wiki_Image_Name" }` when the derived image would not match the wiki.
- Empty slot: `null`.
- **Never** store full URLs in JSON — only wiki image base names for `icon_override`.

---

## Backend Responsibilities

- **Load curated JSON exactly as written.**
- **Expose:** `GET /gear/wiki-guide/{style}` returning the guide payload unchanged in structure and slot identity.
- **Do not:** Reorder slots, substitute items, or "fix" names.
- **Optional enrichment:** Prices, stats, or extra fields may be added **without mutating** slot identity (e.g. append only; never replace `name` or slot presence with DB data).

**Files:** [backend/services/wiki_data.py](backend/services/wiki_data.py) (or dedicated guide loader), [backend/api/v1/gear/routes/progression.py](backend/api/v1/gear/routes/progression.py), [backend/data/wiki_progression/](backend/data/wiki_progression/) (curated `melee.json`, `ranged.json`, `magic.json` or `*_guide.json`).

---

## Frontend Responsibilities

### Rendering Model - OSRS Equipment Interface

- **Equipment interface paperdoll layout** — match the in-game equipment screen visual style.
- **Brown equipment interface background** (the actual OSRS equipment screen UI).
- **Slots positioned exactly as in-game:**
  - Head (top center)
  - Cape (left), Neck (center), Ammo (right) — second row
  - Weapon (left), Body (center), Shield (right) — third row
  - Legs (center) — fourth row
  - Hands (left), Feet (center), Ring (right) — bottom row
- **Side-by-side columns** for each tier (not table rows).
- **Gold coin icon + cost** displayed below each equipment setup.
- Each slot shows: wiki image; tooltip with **exact item name**; empty slots = empty slot graphic or transparent.
- **Tier columns** laid out horizontally (Level 20 | Level 40 | Level 60, etc.) with equipment interface for each.

### Image Resolution Logic

Frontend **owns** image URL derivation:

1. If `icon_override` exists → use it to build `https://oldschool.runescape.wiki/images/{icon_override}_detail.png`.
2. Else derive from `name` (spaces → `_`, `'` → `%27`, etc.) → same URL pattern.
3. Else **fail loudly** — no silent fallback to a different image or placeholder.

### Components

- **WikiGuideView:** Style tabs (Melee / Ranged / Magic); for each game stage, section heading + tier columns (equipment interfaces side-by-side) + content_specific table when present; bonus_table at end.
- **EquipmentInterface:** OSRS paperdoll layout with background and positioned slots; displays one full loadout with gold coin + cost below.
- **TierRow:** Container for multiple EquipmentInterface components displayed side-by-side (one per tier in that section).
- **ContentSpecificTable**, **BonusTable** as per guide structure.

**Files:** [frontend/src/features/gear/](frontend/src/features/gear/) — WikiGuideView, tier table component, ContentSpecificTable, BonusTable; [frontend/src/lib/api/gear.ts](frontend/src/lib/api/gear.ts), hooks, types; [frontend/src/features/gear/Gear.tsx](frontend/src/features/gear/Gear.tsx).

---

## Explicit Non-Goals

- No gear optimization.
- No DPS calculation.
- No "best alternative" or recommendations.
- No auto-selection from item DB.
- No deviation from wiki layouts or gear choices.

---

## Definition of Done

A user can:

1. Open the OSRS Wiki gear progression page (Magic, Melee, or Ranged).
2. Open this app and select the same style.
3. Compare tier rows side-by-side.
4. See the **same gear icons** in the **same slots** in the **same order**.

**If any item differs, the implementation is wrong.**

---

## Implementation Order

1. **Canonical JSON:** Add `slot_order` and adopt slot values as `{ name, icon_override? }`; add one full example guide (e.g. Magic Early Game) with exact wiki names. ✅
2. **Backend:** Loader that reads JSON as-is; `GET /gear/wiki-guide/{style}`; no mutation of slots or names. ✅
3. **Frontend:** Image resolution (icon_override → derive from name → fail loudly) ✅; **equipment interface paperdoll layout** with brown background and in-game slot positions; side-by-side tier columns; WikiGuideView with game stages, equipment interfaces, content_specific, bonus_table.
4. **Data:** Curate full guide JSON for all three styles from wiki/PDFs (exact item names; icon_override only where needed).
5. **Tests and verification:** Backend returns exact structure; frontend renders equipment interfaces; manual or automated check that side-by-side with wiki matches.
