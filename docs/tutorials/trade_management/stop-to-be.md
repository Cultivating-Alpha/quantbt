---
icon: material/format-page-break
---

# Move stop to Break-Even

Risk management might tell you to move stop loss to break even when certain conditions are met.
Doing so requires 2 simple steps:

1. Create your custom Stop-To-BE function
2. Pass that function to your strategy

Find the full notebook [here]()

## The Stop to BE function

The function will wait until a candle wicks above/below a long/short trade before moving the stop to break-env.


``` python title="Create Stop to BE function" linenums="1"
# Fill missing imports
from numba import njit
from quantbt.core.enums import Trade, OrderDirection


"""
The function will be passed 3 variables by default:
1. active_trades: A list of all the currently active trades (NOT orders)
2. data: the original OHLC or tick by tick data you have passed to the strategy
3. index: The index of the current tick iteration
"""
@njit(cache=True)
def stop_to_be_nb(active_trades, data, index):
   current_low = data.low[index]
   current_high = data.high[index]
   for trade in active_trades: # (1)!
        # Pass if we have already moved the SL to breakeven
        if trade[Trade.EntryPrice.value] == trade[Trade.SL.value]: # (2)!
            continue

        entry_index = trade[Trade.Index.value] # (3)!
        trade_entry_low = data.low[int(entry_index)] # (4)!
        trade_entry_high = data.high[int(entry_index)]

        direction = trade[Trade.Direction.value]

        if direction == OrderDirection.SHORT.value:
            if current_low < trade_entry_low:
                trade[Trade.SL.value] = trade[Trade.EntryPrice.value] # (5)!
        else:
            if current_high > trade_entry_high:
                trade[Trade.SL.value] = trade[Trade.EntryPrice.value]
```

1. The function will go over every trade one by one
2. Look at the [Trade Enum](/api/enums/#Trade) to see the different values it can take. Note that it is import to use `value` with numba functions
3. We get the index at which the trade was entered
4. We get the low/high at candle which triggered the trade
5. The Stop loss value of the trade is updated. In real trading, this would lead to a new order to update the SL of the trade, if it's supported by the engine.


## Using the function with the Strategy

In order to use the above function, simple pass it to the [Base Strategy](/api/strategy) when you create it.

``` python title="Passing Stop to BE function" linenums="1"
import quantbt as qbt
import quantbt.indicators as ind
from quantbt.strategies.S_base import S_base
from quantbt.core.enums import CommissionType, DataType, TradeSizeType

data = qbt.data.random_data(seed=300)[0]


class MyStrategy(S_base):
    def generate_signals(self):
        short_period, long_period = self.params

        self.sma_short = ind.talib_SMA(data.close, period=short_period)
        self.sma_long = ind.talib_SMA(data.close, period=long_period)
        self.long = ind.cross_above(self.sma_short, self.sma_long)
        self.short = ind.cross_below(self.sma_short, self.sma_long)

        return {
            "long_entries": self.long,
            "long_exits": self.short,
            "short_entries": self.short,
            "short_exits": self.long,
        }


strategy_settings = {
    "initial_capital": 100_000,
    "commission": 1.2,
    "commission_type": CommissionType.FIXED,
    "multiplier": 20,
    "data_type": DataType.OHLC,
    "default_trade_size": 1,
    "trade_size_type": TradeSizeType.FIXED,
}


st_with_be = MyStrategy(data, stop_to_be=stop_to_be_nb, **strategy_settings) # (1)!
params = (5, 23)
st.from_signals(params)
```

Make sure to pass the `stop_to_be_nb` created above to the strategy.

## Results

Here are the result using the stop to BE on a simple MA crossover
```shell
Stats without stop to BE:
            End Value  ROI: (%)    DD     ratio
(5, 23)  98809.007812     -1.19  1.92 -0.619792

Stats with stop to BE:
            End Value  ROI: (%)    DD     ratio
(5, 23)  99550.835938     -0.45  0.65 -0.692308
```

## Some considerations

The stop-to-be function has to be numba compiled, because it is passed to the numba compiled backtester.
The only downside is that you will be required to recompile the function everytime you update the logic. This can be a pain during development.
However, disabling numba can make that easier.
