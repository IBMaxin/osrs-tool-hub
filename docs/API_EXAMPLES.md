# API Usage Examples

Comprehensive examples for all OSRS Tool Hub API endpoints with request/response formats and common use cases.

## Base URL

```
Local Development: http://localhost:8000/api/v1
Production: https://api.osrs-tool-hub.com/api/v1
```

## Table of Contents

- [Flipping Endpoints](#flipping-endpoints)
- [Gear Endpoints](#gear-endpoints)
- [Slayer Endpoints](#slayer-endpoints)
- [Health Endpoints](#health-endpoints)

---

## Flipping Endpoints

### Get Flip Opportunities

Find profitable flipping opportunities with customizable filters.

**Endpoint:** `GET /flips/opportunities`

**Query Parameters:**
- `budget` (optional): Maximum GP to invest (default: 10M)
- `min_margin` (optional): Minimum profit margin % (default: 5)
- `min_volume` (optional): Minimum daily trade volume (default: 100)
- `limit` (optional): Number of results (default: 20, max: 100)

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/flips/opportunities?budget=50000000&min_margin=10&limit=10"
```

**Example Response:**
```json
{
  "opportunities": [
    {
      "item_id": 2,
      "name": "Cannonball",
      "buy_price": 195,
      "sell_price": 205,
      "margin": 6,
      "roi": 3.08,
      "volume": 50000,
      "tax": 4,
      "profit_after_tax": 6,
      "buy_limit": 11000,
      "potential_profit": 66000,
      "updated_at": "2026-01-29T20:15:00Z"
    }
  ],
  "count": 10,
  "filters": {
    "budget": 50000000,
    "min_margin": 10,
    "min_volume": 100
  }
}
```

**Use Cases:**
- Find flips within your budget
- Filter high-volume items for quick turnover
- Identify high-margin flips for maximum profit

---

### GE Flip Scanner

GE Tracker-style scanner with detailed flip analysis.

**Endpoint:** `GET /flipping/scanner`

**Query Parameters:**
- `budget` (optional): Maximum GP (default: 10M)
- `min_roi` (optional): Minimum ROI % (default: 2)
- `max_price` (optional): Maximum item price
- `limit` (optional): Results limit (default: 50)

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/flipping/scanner?budget=100000000&min_roi=5"
```

**Example Response:**
```json
{
  "flips": [
    {
      "item_id": 11802,
      "name": "Armadyl godsword",
      "buy_price": 21500000,
      "sell_price": 22000000,
      "margin": 70000,
      "roi": 2.33,
      "volume": 150,
      "tax": 430000,
      "profit": 70000,
      "buy_limit": 8
    }
  ],
  "total": 15
}
```

---

### Log Trade

Record buy or sell transactions for profit tracking.

**Endpoint:** `POST /trades`

**Request Body:**
```json
{
  "item_id": 2,
  "item_name": "Cannonball",
  "trade_type": "buy",
  "quantity": 10000,
  "price_per_item": 195,
  "total_price": 1950000,
  "timestamp": "2026-01-29T20:00:00Z"
}
```

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/trades" \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 2,
    "item_name": "Cannonball",
    "trade_type": "buy",
    "quantity": 10000,
    "price_per_item": 195,
    "total_price": 1950000
  }'
```

**Example Response:**
```json
{
  "id": 1,
  "item_id": 2,
  "item_name": "Cannonball",
  "trade_type": "buy",
  "quantity": 10000,
  "price_per_item": 195,
  "total_price": 1950000,
  "timestamp": "2026-01-29T20:00:00Z",
  "created_at": "2026-01-29T20:00:05Z"
}
```

---

### Get Trade History

Retrieve trade history with filters.

**Endpoint:** `GET /trades`

**Query Parameters:**
- `item_id` (optional): Filter by item
- `trade_type` (optional): "buy" or "sell"
- `start_date` (optional): ISO 8601 timestamp
- `end_date` (optional): ISO 8601 timestamp
- `limit` (optional): Max results (default: 100)

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/trades?item_id=2&trade_type=buy&limit=50"
```

---

### Get Trade Statistics

Aggregate statistics for tracked trades.

**Endpoint:** `GET /trades/stats`

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/trades/stats"
```

**Example Response:**
```json
{
  "total_trades": 245,
  "total_profit": 45600000,
  "avg_roi": 4.2,
  "total_volume_traded": 1200000000,
  "most_profitable_item": {
    "item_id": 11802,
    "item_name": "Armadyl godsword",
    "profit": 5600000
  },
  "period": "all_time"
}
```

---

## Gear Endpoints

### Get Gear Progression

Retrieve Wiki-based gear progression for combat styles.

**Endpoint:** `GET /gear/progression/{style}`

**Path Parameters:**
- `style`: "melee", "ranged", or "magic"

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/gear/progression/melee"
```

**Example Response:**
```json
{
  "style": "melee",
  "tiers": [
    {
      "tier": "Early",
      "level_range": "1-40",
      "slots": {
        "head": {"item_id": 1155, "name": "Leather cowl"},
        "body": {"item_id": 1129, "name": "Leather body"},
        "weapon": {"item_id": 1277, "name": "Iron scimitar"}
      }
    }
  ]
}
```

---

### Get Gear Suggestions

Get item suggestions for a specific equipment slot.

**Endpoint:** `GET /gear/suggestions`

**Query Parameters:**
- `slot`: Equipment slot ("head", "body", "legs", "weapon", etc.)
- `combat_style`: "melee", "ranged", or "magic"
- `max_price` (optional): Maximum price per item
- `level` (optional): Player combat level

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/gear/suggestions?slot=weapon&combat_style=melee&max_price=100000000&level=75"
```

**Example Response:**
```json
{
  "slot": "weapon",
  "suggestions": [
    {
      "item_id": 4151,
      "name": "Abyssal whip",
      "price": 1800000,
      "requirements": {"attack": 70},
      "stats": {"attack_slash": 82, "strength": 82}
    },
    {
      "item_id": 11806,
      "name": "Saradomin godsword",
      "price": 35000000,
      "requirements": {"attack": 75},
      "stats": {"attack_slash": 132, "strength": 132}
    }
  ]
}
```

---

### Calculate DPS

Calculate damage per second for a gear loadout.

**Endpoint:** `POST /gear/dps`

**Request Body:**
```json
{
  "gear": {
    "weapon": 4151,
    "body": 10551,
    "legs": 4087,
    "head": 11128
  },
  "stats": {
    "attack": 75,
    "strength": 80,
    "defence": 70
  },
  "target": "Vorkath",
  "prayers": ["piety"]
}
```

**Example Response:**
```json
{
  "dps": 6.45,
  "max_hit": 31,
  "accuracy": 0.85,
  "attack_speed": 4,
  "effective_stats": {
    "attack": 98,
    "strength": 104
  }
}
```

---

### Calculate Best Loadout

Find the optimal gear within budget constraints.

**Endpoint:** `POST /gear/best-loadout`

**Request Body:**
```json
{
  "budget": 50000000,
  "combat_style": "melee",
  "target": "General Graardor",
  "player_stats": {
    "attack": 90,
    "strength": 90,
    "defence": 85
  },
  "constraints": {
    "ironman": false,
    "required_items": [4151]
  }
}
```

**Example Response:**
```json
{
  "loadout": {
    "weapon": {"id": 4151, "name": "Abyssal whip", "price": 1800000},
    "body": {"id": 10551, "name": "Fighter torso", "price": 0},
    "legs": {"id": 4087, "name": "Dragon platelegs", "price": 160000}
  },
  "total_cost": 45800000,
  "dps": 7.2,
  "budget_remaining": 4200000
}
```

---

### Boss BiS Calculator

Get best-in-slot recommendations for specific bosses.

**Endpoint:** `POST /gear/bis/{boss_name}`

**Path Parameters:**
- `boss_name`: Boss identifier ("vorkath", "zulrah", "toa", "bandos", etc.)

**Request Body:**
```json
{
  "budget": 500000000,
  "player_stats": {
    "attack": 99,
    "strength": 99,
    "ranged": 99,
    "magic": 99
  },
  "owned_items": [4151, 11802],
  "ironman": false
}
```

---

## Slayer Endpoints

### Get Slayer Masters

List all slayer masters with requirements.

**Endpoint:** `GET /slayer/masters`

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/slayer/masters"
```

**Example Response:**
```json
{
  "masters": [
    {
      "id": "duradel",
      "name": "Duradel",
      "location": "Shilo Village",
      "requirements": {
        "combat_level": 100,
        "slayer_level": 50
      },
      "specialty": "High-level, high-XP tasks"
    }
  ]
}
```

---

### Get Tasks by Master

Retrieve task list for a specific slayer master.

**Endpoint:** `GET /slayer/tasks/{master}`

**Path Parameters:**
- `master`: Master identifier ("duradel", "nieve", "konar", etc.)

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/slayer/tasks/duradel"
```

**Example Response:**
```json
{
  "master": "duradel",
  "tasks": [
    {
      "task_id": 1,
      "name": "Abyssal demons",
      "weight": 12,
      "amount": "130-200",
      "slayer_level": 85,
      "slayer_xp": 150,
      "recommendation": "DO"
    }
  ]
}
```

---

### Get Task Advice

Get detailed advice for a specific task.

**Endpoint:** `GET /slayer/advice/{task_id}`

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/slayer/advice/1"
```

**Example Response:**
```json
{
  "task_id": 1,
  "name": "Abyssal demons",
  "recommendation": "DO",
  "reasons": [
    "High Slayer XP (150 per kill)",
    "Good GP/hr from drops",
    "Fast task completion"
  ],
  "best_location": "Catacombs of Kourend",
  "gear_recommendation": "Melee with high strength bonus",
  "estimated_time": "20-30 minutes",
  "gp_per_hour": 800000,
  "alternatives": ["Slayer Tower", "Abyssal Nexus"]
}
```

---

### Get Task Locations

Get detailed location information for a task.

**Endpoint:** `GET /slayer/location/{task_id}`

**Example Response:**
```json
{
  "task_id": 1,
  "locations": [
    {
      "name": "Catacombs of Kourend",
      "requirements": {"quest": "None"},
      "benefits": ["Prayer restore", "Superior chance"],
      "how_to_get_there": "Kourend teleport → North to entrance",
      "map_link": "https://oldschool.runescape.wiki/..."
    }
  ]
}
```

---

### Get Slayer Gear Suggestions

Get gear recommendations for a specific slayer task.

**Endpoint:** `POST /gear/slayer-gear`

**Request Body:**
```json
{
  "task_name": "Abyssal demons",
  "budget": 20000000,
  "player_stats": {
    "attack": 80,
    "strength": 85,
    "defence": 75
  }
}
```

---

## Health Endpoints

### Health Check

Check API and database connectivity.

**Endpoint:** `GET /health`

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/health"
```

**Example Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "wiki_api": "accessible",
  "timestamp": "2026-01-29T20:30:00Z",
  "version": "0.1.0"
}
```

---

## Error Responses

All endpoints return consistent error formats:

**400 Bad Request:**
```json
{
  "detail": "Invalid budget value: must be between 1 and 100000000000"
}
```

**404 Not Found:**
```json
{
  "detail": "Item with ID 999999 not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "An unexpected error occurred",
  "error_id": "abc123-def456"
}
```

---

## Rate Limiting

- **Rate Limit:** 100 requests per minute per IP
- **Headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **429 Response:** When rate limit exceeded

---

## Authentication

Currently, no authentication is required. Future versions will support:
- API key authentication
- User-specific trade tracking
- Watchlist persistence
