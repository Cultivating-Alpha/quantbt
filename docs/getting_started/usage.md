---
icon: material/chart-scatter-plot-hexbin
---

# Usage

## Generate Random Data
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
        self.long = ind.cross_above(self.sma_short, self.sma_long)
        self.short = ind.cross_below(self.sma_short, self.sma_long)

        return {
            "long_entries": self.long,
            "long_exits": self.short,
            "short_entries": self.short,
            "short_exits": self.long,
        }


st = MyStrategy(
    data,
    commission=1.2,
    commission_type=CommissionType.FIXED,
    multiplier=4,
    data_type=DataType.OHLC,
    initial_capital=100000,
    default_trade_size=1,
    trade_size_type=TradeSizeType.FIXED,
)
```

1. You can use talib indicators, or you can use some of our custom [indicators](/features/indicators)

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

## All in one


