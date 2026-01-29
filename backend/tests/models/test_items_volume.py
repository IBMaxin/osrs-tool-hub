"""Tests for PriceSnapshot 24h volume tracking."""

from backend.models.items import PriceSnapshot


def test_total_volume_both_none():
    """Test total_volume_24h returns None when both volumes are None."""
    snap = PriceSnapshot(buy_volume_24h=None, sell_volume_24h=None)
    assert snap.total_volume_24h is None


def test_total_volume_one_side():
    """Test total_volume_24h returns correct value when only buy volume is set."""
    snap = PriceSnapshot(buy_volume_24h=120, sell_volume_24h=None)
    assert snap.total_volume_24h == 120


def test_total_volume_sell_side():
    """Test total_volume_24h returns correct value when only sell volume is set."""
    snap = PriceSnapshot(buy_volume_24h=None, sell_volume_24h=80)
    assert snap.total_volume_24h == 80


def test_total_volume_both_present():
    """Test total_volume_24h returns sum when both volumes are set."""
    snap = PriceSnapshot(buy_volume_24h=100, sell_volume_24h=80)
    assert snap.total_volume_24h == 180


def test_total_volume_with_zeros():
    """Test total_volume_24h handles zero values correctly."""
    snap = PriceSnapshot(buy_volume_24h=0, sell_volume_24h=0)
    assert snap.total_volume_24h == 0


def test_total_volume_mixed_none_and_zero():
    """Test total_volume_24h handles mix of None and zero correctly."""
    snap = PriceSnapshot(buy_volume_24h=0, sell_volume_24h=None)
    assert snap.total_volume_24h == 0


def test_has_volume_data_with_data():
    """Test has_volume_data returns True when buy_volume_24h has data."""
    snap = PriceSnapshot(buy_volume_24h=0, sell_volume_24h=None)
    assert snap.has_volume_data()


def test_has_volume_data_with_sell_data():
    """Test has_volume_data returns True when sell_volume_24h has data."""
    snap = PriceSnapshot(buy_volume_24h=None, sell_volume_24h=100)
    assert snap.has_volume_data()


def test_has_volume_data_with_both_data():
    """Test has_volume_data returns True when both volumes have data."""
    snap = PriceSnapshot(buy_volume_24h=50, sell_volume_24h=75)
    assert snap.has_volume_data()


def test_has_volume_data_no_data():
    """Test has_volume_data returns False when both volumes are None."""
    snap = PriceSnapshot(buy_volume_24h=None, sell_volume_24h=None)
    assert not snap.has_volume_data()


def test_price_snapshot_creation_with_all_fields():
    """Test creating a PriceSnapshot with all fields including new volume fields."""
    snap = PriceSnapshot(
        item_id=4151,  # Abyssal whip
        high_price=1200000,
        low_price=1180000,
        high_volume=150,
        low_volume=120,
        buy_volume_24h=2500,
        sell_volume_24h=2200,
    )
    assert snap.item_id == 4151
    assert snap.high_price == 1200000
    assert snap.buy_volume_24h == 2500
    assert snap.sell_volume_24h == 2200
    assert snap.total_volume_24h == 4700
    assert snap.has_volume_data()


def test_volume_independent_of_price_fields():
    """Test volume fields work independently of price fields."""
    snap = PriceSnapshot(
        item_id=4151,
        high_price=None,
        low_price=None,
        buy_volume_24h=1000,
        sell_volume_24h=800
    )
    assert snap.total_volume_24h == 1800
    assert snap.has_volume_data()
    # Price fields should be None
    assert snap.high_price is None
    assert snap.low_price is None
