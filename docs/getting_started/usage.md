---
icon: material/chart-scatter-plot-hexbin
---

# Usage

The following page will illustrate a very basic example where we will:

1. Generate random OHLC data
2. Generate a MA crossover signal 
3. Backtest the signal 
4. Plot the results
5. Optimize the parameters

## Generate Random OHLC Data
There are multiple ways to generate data that will be used in your code, but for this example we will generate random data.

``` python title="Generate random data" hl_lines="3"  linenums="1"

import quantbt as qbt

data = qbt.data.random_data(100)[0] # (1)!
```

1.  You do not have to use the seed, however setting one allows to have the same output every time you run the code.

You can also read your own data files, or download binance data. More info [here](/features/data)

---- 

## Generate MA cross over signals

``` python title="Generate signals" linenums="1"
import quantbt.indicators as ind # (1)!
from quantbt.strategies.S_base import S_base
from quantbt.core.enums import CommissionType, DataType, TradeSizeType


class MyStrategy(S_base):
    def generate_signals(self):
        short_period, long_period = params

        self.sma_short = ind.talib_SMA(data.close, period=short_period)
        self.sma_long = ind.talib_SMA(data.close, period=long_period)
        self.long = ind.cross_above(self.sma_short, self.sma_long) # (2)!
        self.short = ind.cross_below(self.sma_short, self.sma_long)

        return {
            "long_entries": self.long,
            "long_exits": self.short,
            "short_entries": self.short,
            "short_exits": self.long,
        }

strategy_settings = {
    "initial_capital": 100_000, # (3)!
    "commission": 1.2, # (4)!
    "commission_type": CommissionType.FIXED, # (5)!
    "multiplier": 4, # (6)
    "data_type": DataType.OHLC, # (7)! 
    "default_trade_size": 1, # (8)!
    "trade_size_type": TradeSizeType.FIXED, # (9)!
}

st = MyStrategy(
    data,
    commission=1.2, # (3)!
    commission_type=CommissionType.FIXED, # (4)!
    multiplier=4, # (5)!
    data_type=DataType.OHLC, # (6)!
    initial_capital=100000, # (7)!
    default_trade_size=1, # (8)!
    trade_size_type=TradeSizeType.FIXED, # (9)!
)
```

1. You can use talib indicators, or you can use some of our custom [indicators](/features/indicators)
2. We use the built in [cross above](/api/indicators/#cross-above) indicator which is numba powered and parallelized.
3. Define the initial capital. In USD
4. Set the commission amount in USD to be paid. More info [here](/api/strategy/#commissions)
5. Set the commission type. More info [here](/api/strategy/#commissions)
6. Set the Datatype. There are 2 modes: OHLC and Tick. Read moe [here](/api/strategy/#data-type)

## Backtest signals

``` python title="Backtest signals" linenums="1"
# We will be doing a 5-SMA and 23-SMA crossover
params = (5, 23)
st.from_signals(params)
```

## Plot results

``` python title="Plot results"` linenums="1"
import matplotlib

plotting = qbt.lib.plotting
subplots = [
    plotting.add_line_plot(st.sma_short),
    plotting.add_line_plot(st.sma_long),
    plotting.add_markers(
        st.long, data.close, color="green", marker_type=matplotlib.markers.CARETUP
    ),
    plotting.add_markers(st.short, data.close, color="red"),
]


qbt.lib.plotting.mpf_plot(data, subplots=subplots)
```

## Optimize the parameters

## All in one

---- 

# Next steps

QuantBT is much more than just a cross over signal tester. 
It can create [multiple trades](/tutorials/trade_management/simultaneous-trades/), [move to stop to Break-env](/tutorials/trade_management/stop-to-be/), add a [trailing Stop Loss](/tutorials/trade_management/trailing-stop-loss/) and much more that you can find [here](/tutorials/trade_management/)

On top of that, you can also deploy your backtested strategies straight into a [live trading environment](/features/live-trading/)
