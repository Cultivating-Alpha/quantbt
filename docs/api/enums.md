---
icon: 
---

# Enums

QuantBT relies on enums to streamline the namings. This is particularly useful when dealing with numba arrays.

## Note on using with numba

Numba does not recognize complex data times. While all QBT enums inherit `IntEnum`, their value must always be access using the `.value` property.
For example:

```python
trade_direction = OrderDirection.SHORT.value
```


## OrderDirection

```python
class OrderDirection(IntEnum):
    SHORT = 0
    LONG = 1
```

## TradeCloseReason

This object represents the reason a trade was closed. 

```python
class PositionCloseReason(IntEnum):
    SIGNAL = 0          # An opposing signal was placed
    SL = 1              # Stop Loss was hit
    TP = 2              # Take Profit was hit
    TIME_SL = 3         # Trade expired
    TSL = 4             # Trailing stop loss was hit
```

## Trade 

This object represents a trade

```python
class Trade(IntEnum):
    IDX = 0               # Internally Used
    Index = 1             # Index in the data OHLC
    Direction = 2         # Trade Direction. look at [OrderDirection](/api/enums/#OrderDirection)
    EntryTime = 3         
    EntryPrice = 4
    ExitTime = 5
    ExitPrice = 6
    Volume = 7
    SL = 8                # Stop Loss
    TSL = 9               # Trailing Stop Loss - if any
    TP = 10               # Take Profit
    TIME_SL = 11          # A time in the future at which the trade should be exited
    PNL = 12              # Profit & Loss of the trade
    Commission = 13
    Active = 14           # If the trade is still active, or it was closed already
    CloseReason = 15      # Trade close reason. Look at [TradeCloseReason](/api/enums/#TradeCloseReason)
    Extra = 16            # Any extra info provided
```
