"""Flipping service for calculating profit margins."""
from typing import Dict, List, Optional
from sqlmodel import Session, select
from backend.models import Item, PriceSnapshot


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


def calculate_flip_metrics(buy_price: int, sell_price: int, limit: Optional[int]) -> Dict:
    """
    Calculate profit margins and ROI.
    Formula: Margin = (Sell Price - Tax) - Buy Price
    """
    tax = calculate_tax(sell_price)
    post_tax_revenue = sell_price - tax
    margin = post_tax_revenue - buy_price
    
    # Avoid division by zero
    roi = (margin / buy_price * 100) if buy_price > 0 else 0
    
    # Potential Profit = Margin * Limit (if limit exists)
    potential_profit = (margin * limit) if limit else None
    
    return {
        "margin": margin,
        "tax": tax,
        "roi": round(roi, 2),
        "potential_profit": potential_profit
    }


class FlippingService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_flip_opportunities(
        self, 
        max_budget: Optional[int] = None,
        min_roi: float = 1.0,
        min_volume: int = 10
    ) -> List[Dict]:
        """Find profitable flips based on filters."""
        # Join Items and PriceSnapshot (assuming snapshot is updated)
        # Note: For this MVP, we fetch all valid prices and filter in Python
        # In prod, this should be an optimized SQL query
        
        query = select(Item, PriceSnapshot).join(
            PriceSnapshot, Item.id == PriceSnapshot.item_id
        )
        
        results = self.session.exec(query).all()
        opportunities = []
        
        for item, price in results:
            # Skip items with missing price data
            if not price.low_price or not price.high_price:
                continue
            
            # 1. Budget Filter
            if max_budget and price.low_price > max_budget:
                continue
                
            # 2. Calculate Metrics
            metrics = calculate_flip_metrics(
                buy_price=price.low_price,
                sell_price=price.high_price,
                limit=item.limit
            )
            
            # 3. ROI Filter
            if metrics["roi"] < min_roi:
                continue
                
            # 4. Volume Filter (using high/low volume sum)
            total_volume = (price.high_volume or 0) + (price.low_volume or 0)
            if total_volume < min_volume:
                continue
            
            opportunities.append({
                "item_id": item.id,
                "item_name": item.name,
                "icon_url": item.icon_url,
                "buy_price": price.low_price,
                "sell_price": price.high_price,
                "limit": item.limit,
                "volume": total_volume,
                **metrics
            })
            
        # Sort by Potential Profit descending
        opportunities.sort(
            key=lambda x: x["potential_profit"] or 0, 
            reverse=True
        )
        
        return opportunities
    
    # Legacy methods for existing API endpoints
    def get_all_flips(self) -> list:
        """Get all flips (legacy method - returns empty list for now)."""
        # TODO: Implement if needed for tracking historical flips
        return []
    
    def get_flip_by_id(self, flip_id: int):
        """Get flip by ID (legacy method)."""
        # TODO: Implement if needed
        return None
    
    def delete_flip(self, flip_id: int) -> bool:
        """Delete a flip (legacy method)."""
        # TODO: Implement if needed
        return False
    
    async def calculate_flip(self, item_name: str, buy_price: int, sell_price: int):
        """Calculate flip profit (legacy method)."""
        # TODO: Implement if needed for manual flip tracking
        return None
