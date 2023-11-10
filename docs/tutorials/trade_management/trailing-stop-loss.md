---
icon: material/format-page-break
---

# Add a trailing stop loss

A trailing stop loss (TSL) is activated once the trade is in profit. It can be used instead of a fixed take profit to let winner 'run'.

In the world of QBT, a TSL is nothing but an indicator that is passed along with the strategy. It is computed once with the generated signals.
You can pass both long and short TSL values.

Find the full notebook [here](https://github.com/Cultivating-Alpha/quantbt/blob/master/examples/trailing-sl/trailing-sl.ipynb)


## The TSL calculation function

If RSI crossed above 70, add the current low as a TSL for long trades only.
If RSI crossed below 30, add the current high as a TSL for short trades only.


``` python title="Calculate the TSL values" linenums="1"
import talib
from numba import njit
from quantbt.lib import np


@njit
def calculate_trailing_exit(high, low, rsi):
    trailing_long = np.full(len(high), 0, dtype=np.float64)
    trailing_short = np.full(len(high), 0, dtype=np.float64)

    for i in range(len(rsi)):
        if rsi[i] > 70 and rsi[i - 1] < 70:
            trailing_long[i] = low[i]
        elif rsi[i] < 30 and rsi[i - 1] > 30:
            trailing_short[i] = high[i]

    return trailing_long, trailing_short
```

## Using the function with the Strategy

In order to use the above function, simple pass it to the [Base Strategy](/api/strategy) when you create it.

``` python title="Adding the TSL to the strategy" linenums="1"
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

        self.rsi = talib.RSI(data.close, timeperiod=14) # (1)!
        self.trailing_sl_long, self.trailing_sl_short = calculate_trailing_exit(
            data.high.values, data.low.values, self.rsi.values
        )
        return {
            "long_entries": self.long,
            "long_exits": self.short,
            "short_entries": self.short,
            "short_exits": self.long,
            "trailing_sl_long": self.trailing_sl_long, # (2)!
            "trailing_sl_short": self.trailing_sl_short, # (4)!
        }


strategy_settings = {
    "initial_capital": 100_000,
    "commission": 1.2,
    "commission_type": CommissionType.FIXED,
    "multiplier": 20,
    "data_type": DataType.OHLC,
    "default_trade_size": 1,
    "trade_size_type": TradeSizeType.FIXED,
    "use_trailing_sl": True, # (3)
}
```

1. Calculate the RSI using talib. Make sure it is [installed](https://quantbt.com/getting_started/installation/#install-quantbt)
2. Pass along the sl_long and sl_short to the `generate_signals` function
3. By default, the strategy's `use_trailing_sl` is set to `False`
4. Pass along the short sl. Both long and short TSL are mandatory


## Results

Here are the result using the stop to BE on a simple MA crossover
```shell
Stats without TSL:
            End Value  ROI: (%)    DD     ratio
(5, 23)  98809.007812     -1.19  1.92 -0.619792

Stats with TSL:
            End Value  ROI: (%)   DD  ratio
(5, 23)  98719.265625     -1.28  1.6   -0.8
```
