"""Trade service for logging and tracking user buy/sell transactions."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

from sqlmodel import Session, select

from backend.models import Trade, Item


class TradeService:
    """Service for managing user trades."""

    def __init__(self, session: Session):
        """
        Initialize trade service.

        Args:
            session: Database session
        """
        self.session = session

    def log_trade(
        self,
        user_id: str,
        item_id: int,
        buy_price: int,
        quantity: int,
        sell_price: Optional[int] = None,
        status: str = "bought",
    ) -> Trade:
        """
        Log a trade transaction.

        Args:
            user_id: User identifier
            item_id: OSRS item ID
            buy_price: Price per item when bought
            quantity: Quantity of items
            sell_price: Optional price per item when sold
            status: Trade status ('bought', 'sold', 'cancelled')

        Returns:
            Created Trade object

        Raises:
            ValueError: If status is invalid or required fields are missing
        """
        if status not in ("bought", "sold", "cancelled"):
            raise ValueError(f"Invalid status: {status}. Must be 'bought', 'sold', or 'cancelled'")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if buy_price <= 0:
            raise ValueError("Buy price must be greater than 0")

        # Get item name from database
        item = self.session.get(Item, item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found")

        item_name = item.name

        # Create trade entry
        trade = Trade(
            user_id=user_id,
            item_id=item_id,
            item_name=item_name,
            buy_price=buy_price,
            sell_price=sell_price,
            quantity=quantity,
            status=status,
        )

        # Calculate profit if sold
        if status == "sold" and sell_price is not None:
            trade.profit = trade.calculate_profit()

        trade.updated_at = datetime.now(trade.created_at.tzinfo)

        self.session.add(trade)
        self.session.commit()
        self.session.refresh(trade)

        return trade

    def get_trade_history(
        self,
        user_id: str,
        status: Optional[str] = None,
        item_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Trade]:
        """
        Get user's trade history with optional filters.

        Args:
            user_id: User identifier
            status: Optional filter by status ('bought', 'sold', 'cancelled')
            item_id: Optional filter by item ID
            start_date: Optional filter by start date
            end_date: Optional filter by end date
            limit: Maximum number of results to return

        Returns:
            List of Trade objects sorted by created_at descending
        """
        query = select(Trade).where(Trade.user_id == user_id)

        # Apply filters
        if status:
            if status not in ("bought", "sold", "cancelled"):
                raise ValueError(f"Invalid status: {status}")
            query = query.where(Trade.status == status)

        if item_id:
            query = query.where(Trade.item_id == item_id)

        if start_date:
            query = query.where(Trade.created_at >= start_date)

        if end_date:
            query = query.where(Trade.created_at <= end_date)

        # Order by created_at descending (most recent first)
        query = query.order_by(Trade.created_at.desc())

        # Apply limit
        query = query.limit(limit)

        trades = self.session.exec(query).all()
        return list(trades)

    def get_trade_stats(self, user_id: str, days: Optional[int] = None) -> Dict:
        """
        Get aggregate statistics for user's trades.

        Args:
            user_id: User identifier
            days: Optional number of days to look back (None = all time)

        Returns:
            Dictionary with aggregate stats:
            - total_profit: Total profit across all sold trades
            - total_trades: Total number of trades
            - sold_trades: Number of sold trades
            - profit_per_hour: Average profit per hour (if applicable)
            - best_items: List of top 5 most profitable items
            - profit_by_item: Profit breakdown by item
        """
        query = select(Trade).where(Trade.user_id == user_id)

        # Filter by date range if specified
        if days:
            cutoff_date = datetime.now(
                tz=datetime.now().tzinfo or datetime.utcnow().tzinfo
            ) - timedelta(days=days)
            query = query.where(Trade.created_at >= cutoff_date)

        trades = self.session.exec(query).all()
        trades_list = list(trades)

        if not trades_list:
            return {
                "total_profit": 0,
                "total_trades": 0,
                "sold_trades": 0,
                "profit_per_hour": 0.0,
                "best_items": [],
                "profit_by_item": {},
            }

        # Calculate stats
        sold_trades = [t for t in trades_list if t.status == "sold"]
        total_profit = sum(t.profit for t in sold_trades)
        total_trades = len(trades_list)
        sold_count = len(sold_trades)

        # Calculate profit per hour
        # Use time span from first to last trade
        profit_per_hour = 0.0
        if sold_trades and len(sold_trades) > 1:
            first_trade = min(sold_trades, key=lambda t: t.created_at)
            last_trade = max(sold_trades, key=lambda t: t.updated_at)
            time_span = (last_trade.updated_at - first_trade.created_at).total_seconds() / 3600
            if time_span > 0:
                profit_per_hour = total_profit / time_span

        # Group profit by item
        profit_by_item: Dict[str, int] = {}
        for trade in sold_trades:
            item_name = trade.item_name
            if item_name not in profit_by_item:
                profit_by_item[item_name] = 0
            profit_by_item[item_name] += trade.profit

        # Get top 5 most profitable items
        best_items = sorted(
            [{"item_name": name, "profit": profit} for name, profit in profit_by_item.items()],
            key=lambda x: int(x["profit"]),
            reverse=True,
        )[:5]

        return {
            "total_profit": total_profit,
            "total_trades": total_trades,
            "sold_trades": sold_count,
            "profit_per_hour": round(profit_per_hour, 2),
            "best_items": best_items,
            "profit_by_item": profit_by_item,
        }
