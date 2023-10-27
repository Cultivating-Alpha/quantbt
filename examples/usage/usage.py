import quantbt as qbt

data = qbt.data.random_data(seed=300)[0]
print(data)


import quantbt.indicators as ind
from quantbt.strategies.S_base import S_base
from quantbt.core.enums import CommissionType, DataType, TradeSizeType


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


"""
This is how we actually backtest the strategy.
We only need to set the parameters which will be automatically passed to the st.generate_signals() function
"""
st = MyStrategy(data, **strategy_settings)
st.set_backtester_settings()

params = (5, 23)
st.from_signals(params)

# |%%--%%| <sER6Ds1yb6|dcbhkIt8T2>

stats = st.get_stats()
print(stats)

# |%%--%%| <dcbhkIt8T2|Ap4AM4XYjW>

trades = st.get_trades()
print(trades)

# |%%--%%| <Ap4AM4XYjW|mCaJ4rxICW>

st.plot_equity()

# |%%--%%| <mCaJ4rxICW|IxcW591TUJ>

"""
Plotting the equity, adding the 2 MA lines, as well as markers for long and short entry signals
"""

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
# |%%--%%| <IxcW591TUJ|Ufsl8mlq0u>

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

# Apply the function to create the new column


# rsi_scatter_high = data['high']
# rsi_scatter_low = data['high']

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
