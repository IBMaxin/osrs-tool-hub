"""Trade models for tracking user buy/sell transactions."""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Trade(SQLModel, table=True):
    """Trade model for tracking user buy/sell transactions."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, description="User identifier (UUID from localStorage)")
    item_id: int = Field(index=True, description="OSRS item ID")
    item_name: str = Field(description="Item name for display")
    buy_price: int = Field(description="Price per item when bought")
    sell_price: Optional[int] = Field(default=None, description="Price per item when sold")
    quantity: int = Field(gt=0, description="Quantity of items traded")
    profit: int = Field(
        default=0, description="Calculated profit: (sell_price - buy_price) * quantity - tax"
    )
    status: str = Field(
        default="bought",
        description="Trade status: 'bought', 'sold', or 'cancelled'",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def calculate_profit(self) -> int:
        """
        Calculate profit for this trade.

        Profit = (sell_price - buy_price) * quantity - tax
        Tax is 2% of sell_price, capped at 5M, exempt for items under 50gp.

        Returns:
            Calculated profit in GP
        """
        if self.status != "sold" or self.sell_price is None:
            return 0

        # Calculate tax (2% of sell price, capped at 5M, exempt under 50gp)
        if self.sell_price < 50:
            tax = 0
        else:
            tax = int(self.sell_price * 0.02)
            tax = min(tax, 5_000_000)

        # Total tax for the quantity
        total_tax = tax * self.quantity

        # Profit = (sell - buy) * quantity - tax
        profit = (self.sell_price - self.buy_price) * self.quantity - total_tax
        return profit
