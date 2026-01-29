"""Flipping service for calculating profit margins."""

from typing import Dict, List, Optional
from sqlmodel import Session, select, text
from sqlalchemy import func
from pydantic import BaseModel
from backend.models import Item, PriceSnapshot
import logging

logger = logging.getLogger(__name__)


def calculate_tax(sell_price: int) -> int:
    """
    Calculate OSRS GE tax (updated May 2025).
    Rules:
    - 2% of sell price
    - Items under 50gp are exempt
    - Tax is capped at 5,000,000 gp
    """
    if sell_price < 50:
        return 0

    tax = int(sell_price * 0.02)
    return min(tax, 5_000_000)


class FlipOpportunity(BaseModel):
    """Pydantic model for flip opportunity results."""

    item_id: int
    item_name: str
    buy_price: int
    sell_price: int
    margin: float
    roi: float
    volume: int
    buy_volume_24h: Optional[int] = None
    sell_volume_24h: Optional[int] = None
    total_volume_24h: Optional[int] = None
    margin_x_volume: Optional[float] = None
    potential_profit: Optional[float] = None
    limit: Optional[int] = None
    tax: Optional[int] = None
    icon_url: Optional[str] = None
    wiki_url: Optional[str] = None


class FlippingService:
    def __init__(self, session: Session):
        self.session = session

    def get_flip_opportunities(
        self,
        max_budget: Optional[int] = None,
        min_roi: float = 1.0,
        min_volume: int = 10,
        limit: int = 50,
    ) -> List[Dict]:
        """
        Find profitable flips based on filters.
        Optimized to perform heavy filtering in SQL where possible.
        """
        # Start query
        query = select(Item, PriceSnapshot).join(
            PriceSnapshot,
            Item.id == PriceSnapshot.item_id,  # type: ignore[arg-type]
        )

        # Filter: Must have valid prices
        query = query.where(PriceSnapshot.high_price.is_not(None))  # type: ignore[union-attr]
        query = query.where(PriceSnapshot.low_price.is_not(None))  # type: ignore[union-attr]

        # Filter: Max Budget (using low_price as buy price)
        if max_budget is not None:
            query = query.where(PriceSnapshot.low_price <= max_budget)  # type: ignore[operator]

        # Filter: Volume (sum of high/low volume)
        # Only apply volume filter if min_volume > 0 and volume data exists
        # Since volume data may not be available, we skip this filter if min_volume is 0
        if min_volume > 0:
            total_volume = func.coalesce(PriceSnapshot.high_volume, 0) + func.coalesce(
                PriceSnapshot.low_volume, 0
            )  # type: ignore[operator]
            query = query.where(total_volume >= min_volume)  # type: ignore

        results = self.session.exec(query).all()
        opportunities = []

        for item, price in results:
            buy_price = price.low_price
            sell_price = price.high_price

            # Skip invalid prices (e.g. 0 or negative)
            if not buy_price or not sell_price or buy_price <= 0 or sell_price <= 0:
                continue

            # Calculate Tax
            tax = calculate_tax(sell_price)
            post_tax_revenue = sell_price - tax
            margin = post_tax_revenue - buy_price

            # Calculate ROI (GE Tracker style: margin / sell_price)
            roi = margin / sell_price * 100

            if roi < min_roi:
                continue

            # Volume calculations
            buy_vol_24h = price.buy_volume_24h
            sell_vol_24h = price.sell_volume_24h
            total_vol_24h = (
                (buy_vol_24h or 0) + (sell_vol_24h or 0)
                if (buy_vol_24h is not None or sell_vol_24h is not None)
                else None
            )

            # Margin x Volume (GE Tracker style)
            margin_x_volume = margin * (total_vol_24h or 0) if total_vol_24h is not None else None

            # Potential Profit - use MIN(limit, volume) since you can't flip more than available volume
            item_limit = item.limit or 0
            available_volume = (price.high_volume or 0) + (price.low_volume or 0)
            flippable_quantity = (
                min(item_limit, available_volume) if item_limit > 0 and available_volume > 0 else 0
            )
            potential_profit = margin * flippable_quantity

            opportunities.append(
                {
                    "item_id": item.id,
                    "item_name": item.name,
                    "icon_url": item.icon_url,
                    "buy_price": buy_price,
                    "sell_price": sell_price,
                    "limit": item_limit,
                    "volume": (price.high_volume or 0) + (price.low_volume or 0),
                    "buy_volume_24h": buy_vol_24h,
                    "sell_volume_24h": sell_vol_24h,
                    "total_volume_24h": total_vol_24h,
                    "margin_x_volume": margin_x_volume,
                    "margin": margin,
                    "tax": tax,
                    "roi": round(roi, 2),
                    "potential_profit": potential_profit,
                }
            )

        # Sort by Margin x Volume descending (GE Tracker style), then by potential_profit
        opportunities.sort(
            key=lambda x: (
                x["margin_x_volume"] if x["margin_x_volume"] is not None else 0,
                x["potential_profit"] or 0,
            ),
            reverse=True,
        )

        return opportunities[:limit]

    def find_best_flips(
        self, budget: int, min_roi: float, min_volume: int, exclude_members: bool = False
    ) -> List[FlipOpportunity]:
        """
        Find best flip opportunities using optimized SQL query.

        This method performs all calculations in the database layer for maximum performance.
        No Python loops - all filtering and calculations happen in SQL.

        Args:
            budget: Maximum budget in GP
            min_roi: Minimum ROI percentage
            min_volume: Minimum volume requirement
            exclude_members: If True, exclude members-only items

        Returns:
            List of FlipOpportunity models sorted by margin x volume
        """
        # Build optimized SQL query that does all calculations in the database
        # Using raw SQL for maximum performance and to avoid Python loops

        # Calculate margin_post_tax: (high_price - tax) - low_price
        # Tax is 2% of sell price, capped at 5,000,000 gp, exempt for items under 50gp
        # Formula: high_price - MIN(high_price * 0.02, 5000000) - low_price
        # For items under 50gp, tax is 0

        # Build WHERE clause conditions
        where_conditions = [
            "i.high_price IS NOT NULL",
            "i.low_price IS NOT NULL",
            "i.low_price > 0",
            "i.high_price > 0",
            "i.low_price <= :budget",
        ]

        # Add members filter if needed
        if exclude_members:
            where_conditions.append("i.members = 0")

        where_clause = " AND ".join(where_conditions)

        # Use MIN instead of LEAST for SQLite compatibility
        # Note: "limit" is a reserved keyword in SQLite, so we need to escape it with quotes
        # Tax calculation: 2% of sell price, capped at 5M, exempt for items under 50gp
        # ROI calculation: margin / sell_price * 100 (GE Tracker style)
        # Margin x Volume: margin * (buy_volume_24h + sell_volume_24h)
        sql_query = text(
            f"""
            SELECT
                i.id as item_id,
                i.name,
                i.low_price as buy_price,
                i.high_price as sell_price,
                (i.high_price - CASE
                    WHEN i.high_price < 50 THEN 0
                    WHEN i.high_price * 0.02 > 5000000 THEN 5000000
                    ELSE CAST(i.high_price * 0.02 AS INTEGER)
                END) - i.low_price as margin_post_tax,
                ((i.high_price - CASE
                    WHEN i.high_price < 50 THEN 0
                    WHEN i.high_price * 0.02 > 5000000 THEN 5000000
                    ELSE CAST(i.high_price * 0.02 AS INTEGER)
                END) - i.low_price) * 100.0 / NULLIF(i.high_price, 0) as roi,
                COALESCE(ps.high_volume, 0) + COALESCE(ps.low_volume, 0) as volume,
                COALESCE(ps.buy_volume_24h, ps.low_volume, 0) as buy_volume_24h,
                COALESCE(ps.sell_volume_24h, ps.high_volume, 0) as sell_volume_24h,
                COALESCE(ps.buy_volume_24h, ps.low_volume, 0) + COALESCE(ps.sell_volume_24h, ps.high_volume, 0) as total_volume_24h,
                COALESCE(i."limit", 0) as buy_limit,
                CASE
                    WHEN i.name IS NOT NULL THEN
                        'https://oldschool.runescape.wiki/w/' || REPLACE(i.name, ' ', '_')
                    ELSE NULL
                END as wiki_url
            FROM item i
            LEFT JOIN pricesnapshot ps ON i.id = ps.item_id
            WHERE {where_clause}
                AND (COALESCE(ps.buy_volume_24h, ps.low_volume, 0) + COALESCE(ps.sell_volume_24h, ps.high_volume, 0)) >= :min_volume
                AND ((i.high_price - CASE
                    WHEN i.high_price < 50 THEN 0
                    WHEN i.high_price * 0.02 > 5000000 THEN 5000000
                    ELSE CAST(i.high_price * 0.02 AS INTEGER)
                END) - i.low_price) * 100.0 / NULLIF(i.high_price, 0) >= :min_roi
            ORDER BY
                ((i.high_price - CASE
                    WHEN i.high_price < 50 THEN 0
                    WHEN i.high_price * 0.02 > 5000000 THEN 5000000
                    ELSE CAST(i.high_price * 0.02 AS INTEGER)
                END) - i.low_price) *
                (COALESCE(ps.buy_volume_24h, ps.low_volume, 0) + COALESCE(ps.sell_volume_24h, ps.high_volume, 0)) DESC,
                ((i.high_price - CASE
                    WHEN i.high_price < 50 THEN 0
                    WHEN i.high_price * 0.02 > 5000000 THEN 5000000
                    ELSE CAST(i.high_price * 0.02 AS INTEGER)
                END) - i.low_price) *
                CASE
                    WHEN COALESCE(i."limit", 0) < (COALESCE(ps.high_volume, 0) + COALESCE(ps.low_volume, 0))
                    THEN COALESCE(i."limit", 0)
                    ELSE (COALESCE(ps.high_volume, 0) + COALESCE(ps.low_volume, 0))
                END DESC
            LIMIT 100
        """
        )

        # Execute query with parameters using bindparams
        result = self.session.execute(
            sql_query,
            {"budget": budget, "min_roi": min_roi, "min_volume": min_volume},
        )

        opportunities = []
        for row in result.mappings():
            margin_post_tax = float(row["margin_post_tax"] or 0.0)
            roi = float(row["roi"] or 0.0)
            volume = int(row["volume"] or 0)
            buy_vol_24h = int(row["buy_volume_24h"]) if row["buy_volume_24h"] else None
            sell_vol_24h = int(row["sell_volume_24h"]) if row["sell_volume_24h"] else None
            total_vol_24h = int(row["total_volume_24h"]) if row["total_volume_24h"] else None
            margin_x_volume = (
                margin_post_tax * (total_vol_24h or 0) if total_vol_24h is not None else None
            )

            opportunities.append(
                FlipOpportunity(
                    item_id=int(row["item_id"]),
                    item_name=str(row["name"]),
                    buy_price=int(row["buy_price"]),
                    sell_price=int(row["sell_price"]),
                    margin=round(margin_post_tax, 2),
                    roi=round(roi, 2),
                    volume=volume,
                    buy_volume_24h=buy_vol_24h,
                    sell_volume_24h=sell_vol_24h,
                    total_volume_24h=total_vol_24h,
                    margin_x_volume=margin_x_volume,
                    wiki_url=str(row["wiki_url"]) if row["wiki_url"] else None,
                )
            )

        return opportunities
