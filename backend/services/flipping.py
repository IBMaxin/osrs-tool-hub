"""Flipping service for calculating profit margins."""
from typing import Dict, List, Optional
from sqlmodel import Session, select, col
from sqlalchemy import func
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

class FlippingService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_flip_opportunities(
        self, 
        max_budget: Optional[int] = None,
        min_roi: float = 1.0,
        min_volume: int = 10,
        limit: int = 50
    ) -> List[Dict]:
        """
        Find profitable flips based on filters.
        Optimized to perform heavy filtering in SQL where possible.
        """
        # Start query
        query = select(Item, PriceSnapshot).join(
            PriceSnapshot, Item.id == PriceSnapshot.item_id
        )
        
        # Filter: Must have valid prices
        query = query.where(PriceSnapshot.high_price.is_not(None))
        query = query.where(PriceSnapshot.low_price.is_not(None))
        
        # Filter: Max Budget (using low_price as buy price)
        if max_budget:
            query = query.where(PriceSnapshot.low_price <= max_budget)
        
        # Filter: Volume (sum of high/low volume)
        # Only apply volume filter if min_volume > 0 and volume data exists
        # Since volume data may not be available, we skip this filter if min_volume is 0
        if min_volume > 0:
            total_volume = func.coalesce(PriceSnapshot.high_volume, 0) + func.coalesce(PriceSnapshot.low_volume, 0)
            query = query.where(total_volume >= min_volume)
        
        results = self.session.exec(query).all()
        opportunities = []
        
        for item, price in results:
            buy_price = price.low_price
            sell_price = price.high_price
            
            # Skip invalid prices (e.g. 0)
            if not buy_price or not sell_price or buy_price <= 0:
                continue

            # Calculate Tax
            tax = calculate_tax(sell_price)
            post_tax_revenue = sell_price - tax
            margin = post_tax_revenue - buy_price
            
            # Calculate ROI
            roi = (margin / buy_price * 100)
            
            if roi < min_roi:
                continue
                
            # Potential Profit
            item_limit = item.limit or 0
            potential_profit = margin * item_limit if item_limit > 0 else 0
            
            opportunities.append({
                "item_id": item.id,
                "item_name": item.name,
                "icon_url": item.icon_url,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "limit": item_limit,
                "volume": (price.high_volume or 0) + (price.low_volume or 0),
                "margin": margin,
                "tax": tax,
                "roi": round(roi, 2),
                "potential_profit": potential_profit
            })
            
        # Sort by Potential Profit descending
        opportunities.sort(
            key=lambda x: x["potential_profit"] or 0, 
            reverse=True
        )
        
        return opportunities[:limit]
