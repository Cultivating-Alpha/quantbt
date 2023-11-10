---
icon: material/chart-scatter-plot-hexbin
---

# Usage
## Notebook and Source
You can jump right into the Jupyter notebook [here](https://github.com/Cultivating-Alpha/quant.bt/blob/master/examples/usage/usage.ipynb).

----

## Code
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


```shell
                  open        high         low       close
date                                                      
2023-01-01   97.029659   97.862781   95.676128   96.509250
2023-01-02   96.509250   97.194830   92.974539   93.660119
2023-01-03   93.660119   93.717696   91.819744   91.877321
2023-01-04   91.877321   95.166148   90.110821   93.399648
2023-01-05   93.399648   93.441865   91.959917   92.002133
...                ...         ...         ...         ...
2025-09-20  107.731634  107.845037  105.606316  105.719719
2025-09-21  105.719719  107.410297  103.777499  105.468077
2025-09-22  105.468077  106.318677  104.659829  105.510429
2025-09-23  105.510429  106.464046  103.718701  104.672318
2025-09-24  104.672318  104.681652  103.439853  103.449187

[998 rows x 4 columns]
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
    "multiplier": 20, # (6)
    "data_type": DataType.OHLC, # (7)! 
    "default_trade_size": 1, # (8)!
    "trade_size_type": TradeSizeType.FIXED, # (9)!
}

st = MyStrategy(data, **strategy_settings)

```

1. You can use talib indicators, or you can use some of our custom [indicators](/features/indicators)
2. We use the built in [cross above](/api/indicators/#cross-above) indicator which is numba powered and parallelized.
3. Define the initial capital. In USD
4. Set the commission amount in USD to be paid. More info [here](/api/strategy/#commissions)
5. Set the commission type. More info [here](/api/strategy/#commissions)
6. Use the multiplier to reflect leverage. This example uses $NQ Futures, where each point is worth 20$
7. Set the Datatype. There are 2 modes: OHLC and Tick. Read moe [here](/api/strategy/#datatype)
8. This means that no matter what, the backtester will always only take 1 contract per trade
9. 2 Trade size types are supported: `Fixed` and `Percentage` . Read more [here](/api/strategy/#tradesize)

## Backtest signals

``` python title="Backtest signals" linenums="1"
# We will be doing a 5-SMA and 23-SMA crossover
params = (5, 23)
st.from_signals(params)
```

This will run the backtest using 5 and 23 as periods for the 2 moving averages

## View Stats

``` python title="View Stats" linenums="1"
stats = st.get_stats()
print(stats)
```

```shell
           End Value  ROI: (%)   DD  ratio
(5, 23)  99618.40625     -0.38  0.5  -0.76
```

## View Trades

``` python title="View Trades" linenums="1"
trades = st.get_trades()
print(trades)
```

```shell
     IDX  Index  Direction  EntryTime  EntryPrice  ...         PNL  Commission  Active  CloseReason  Extra
0    0.0   24.0        0.0 2023-01-25   95.543045  ... -132.172492         2.4     0.0       SIGNAL   -1.0
1    1.0   25.0        1.0 2023-01-26  102.031670  ...  -17.529395         2.4     0.0       SIGNAL   -1.0
2    2.0   32.0        0.0 2023-02-02  101.275200  ...  -68.733008         2.4     0.0       SIGNAL   -1.0
3    3.0   33.0        1.0 2023-02-03  104.591850  ...  317.843378         2.4     0.0       SIGNAL   -1.0
4    4.0   90.0        0.0 2023-04-01  120.604019  ...    0.620630         2.4     0.0       SIGNAL   -1.0
..   ...    ...        ...        ...         ...  ...         ...         ...     ...          ...    ...
57  57.0  886.0        1.0 2025-06-05  108.097717  ...  133.575037         2.4     0.0       SIGNAL   -1.0
58  58.0  916.0        0.0 2025-07-05  114.896469  ...   54.565790         2.4     0.0       SIGNAL   -1.0
59  59.0  934.0        1.0 2025-07-23  112.048180  ... -139.441321         2.4     0.0       SIGNAL   -1.0
60  60.0  937.0        0.0 2025-07-26  105.196114  ...  120.635431         2.4     0.0       SIGNAL   -1.0
61  61.0  972.0        1.0 2025-08-30   99.044342  ...  110.159509         2.4     1.0          NaN   -1.0

[62 rows x 17 columns]
```

## Plot Equity

``` python title="Plot Equity" linenums="1"
st.plot_equity()
```


<figure markdown>
  ![Image title](/assets/usage-plot_equity.jpeg){ width="600" }
  <figcaption>Equity Plot</figcaption>
</figure>

## Plot Data with indicators and signals

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

<figure markdown>
  ![Plot Strategy](/assets/usage-plot_indicators_signals.jpeg){ width="600" }
  <figcaption>Strategy with Indicators and signals</figcaption>
</figure>


## Advanced Plotting using UI

``` python title="Plot results"` linenums="1"
import pandas as pd
from quantbt.lib import time_manip
from quantbt.lib.data_to_csv import save_data, create_scatter_df


data["Date"] = time_manip.convert_datetime_to_ms(data.index)
time_manip.convert_datetime_to_ms(data["Date"])

"""
Create the dataframes needed for the UI
"""
df = pd.DataFrame(
    {
        "date": data["Date"],
        "open": data.open,
        "high": data.high,
        "low": data.low,
        "close": data.close,
        "long": st.long,
        "short": st.short,
        "equity": st.bt.data_module.equity,
    }
)
df.index = df["date"]

indicators_data = pd.DataFrame(
    {"ma1": st.sma_long, "ma2": st.sma_short, "equity": st.bt.data_module.equity}
)

"""
Create the configuration that tells the UI which indicators to draw
"""
indicators = [
    {"name": "EMA Long", "type": "line", "panel": 0, "dataIndex": 0},
    {"name": "MA Short", "type": "line", "color": "black", "panel": 0, "dataIndex": 1},
    {"name": "Equity", "type": "line", "color": "black", "panel": 1, "dataIndex": 2},
]


"""
Save the data and config to the location of the UI
"""
UI_LOCATION = "/home/alpha/workspace/cultivating-alpha/candles-ui/public"

save_data(
    UI_LOCATION, df, indicators, indicators_data, st.bt.trade_module.closed_trades
)
```

You can view the output live [here](https://candles-ui.vercel.app/)



## Optimize the parameters

*TODO: WIP*

## All in one

---- 

# Next steps

QuantBT is much more than just a cross over signal tester. 
It can create [multiple trades](/tutorials/trade_management/simultaneous-trades/), [move stop to to Break-env](/tutorials/trade_management/stop-to-be/), add a [trailing Stop Loss](/tutorials/trade_management/trailing-stop-loss/) and much more that you can find [here](/tutorials/trade_management/)

On top of that, you can also deploy your backtested strategies straight into a [live trading environment](/features/live-trading/)
