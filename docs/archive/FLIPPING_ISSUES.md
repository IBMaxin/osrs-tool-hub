# Flipping Service Issues Found

## Issues Identified

### 1. ✅ **Potential Profit Calculation Bug** (FIXED)
**Location**: `backend/services/flipping.py` line 96

**Problem**: 
```python
potential_profit = margin * item_limit if item_limit > 0 else 0
```

This calculates potential profit using only the GE limit, ignoring actual volume available. You cannot flip more items than the available volume, even if the limit is higher.

**Example**:
- Item has limit of 1000
- Volume available is only 50
- Current code calculates: `margin * 1000` (WRONG)
- Should calculate: `margin * min(1000, 50) = margin * 50` (CORRECT)

**Fix**: Should use `MIN(limit, volume)` like in `find_best_flips` method (line 207-209).

**Impact**: High - This causes incorrect sorting and misleading profit estimates.

---

### 2. ✅ **Missing Sell Price Validation** (FIXED)
**Location**: `backend/services/flipping.py` line 80

**Problem**:
```python
if not buy_price or not sell_price or buy_price <= 0:
    continue
```

This checks if `buy_price <= 0` but doesn't check if `sell_price <= 0`. Items with invalid sell prices (0 or negative) could slip through.

**Fix**: Add `or sell_price <= 0` to the condition.

**Impact**: Medium - Could show invalid flip opportunities.

---

### 3. ✅ **GE Tax Calculation** (CORRECT)
**Location**: `backend/services/flipping.py` lines 11-23

**Status**: Correct
- 2% of sell price ✓
- Exempt for items under 50gp ✓
- Capped at 5,000,000 gp ✓

---

### 4. ✅ **Volume Calculation** (CORRECT)
**Location**: `backend/services/flipping.py` line 105

**Status**: Correct
```python
volume = (price.high_volume or 0) + (price.low_volume or 0)
```
This correctly sums high and low volume.

---

### 5. ✅ **Price Usage** (CORRECT)
**Location**: `backend/services/flipping.py` lines 76-77

**Status**: Correct
- `buy_price = price.low_price` ✓
- `sell_price = price.high_price` ✓

---

### 6. ✅ **Inconsistent Potential Profit Calculation** (FIXED)
**Location**: Two different methods calculate differently

**Problem**: 
- `get_flip_opportunities()` uses: `margin * item_limit` (WRONG)
- `find_best_flips()` uses: `margin * MIN(limit, volume)` (CORRECT)

**Impact**: Medium - Inconsistent behavior between endpoints.

---

## Recommended Fixes

### Fix 1: Correct Potential Profit Calculation
```python
# Current (line 95-96):
item_limit = item.limit or 0
potential_profit = margin * item_limit if item_limit > 0 else 0

# Should be:
item_limit = item.limit or 0
available_volume = (price.high_volume or 0) + (price.low_volume or 0)
flippable_quantity = min(item_limit, available_volume) if item_limit > 0 and available_volume > 0 else 0
potential_profit = margin * flippable_quantity
```

### Fix 2: Add Sell Price Validation
```python
# Current (line 80):
if not buy_price or not sell_price or buy_price <= 0:
    continue

# Should be:
if not buy_price or not sell_price or buy_price <= 0 or sell_price <= 0:
    continue
```

---

## Test Cases to Add

1. Test potential profit with limit > volume
2. Test potential profit with volume > limit
3. Test items with sell_price = 0
4. Test items with sell_price < 0
5. Test items with limit = 0
6. Test items with volume = 0

---

## Fixes Applied

✅ **Fixed Issue #1**: Potential profit now correctly uses `MIN(limit, volume)` instead of just `limit`
✅ **Fixed Issue #2**: Added validation to filter out items with `sell_price <= 0`
✅ **Fixed Issue #6**: Both methods now use consistent calculation

**Test Coverage**: Added 2 new test cases to verify fixes:
- `test_potential_profit_uses_min_limit_volume` - Verifies MIN(limit, volume) calculation
- `test_invalid_sell_price_filtered` - Verifies invalid sell prices are filtered

All tests passing ✅

---

*Last Updated: 2026-01-27*
*All critical issues fixed and tested*
