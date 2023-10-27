from numba import njit
from quantbt.lib.plotting import plotting
from quantbt.lib.time_manip import time_manip
from quantbt.lib import np, timeit, pd, find_files
from quantbt.lib.calculate_stats import calculate_stats
from quantbt.lib.output_trades import output_trades
from quantbt.core.enums import CommissionType, DataType, TradeSizeType
from quantbt.lib import pd, find_files, np, optimize
from quantbt.lib.data_to_csv import save_data, create_scatter_df

import quantbt as qnb

import talib

# import pandas_ta as ta

from quantbt.strategies.S_base import S_base
from quantbt.core.backtester import Backtester
from quantbt.strategies.S_bid_ask import S_bid_ask
from quantbt.core.place_orders_on_ohlc import place_orders_on_ohlc
import matplotlib

import quantbt.indicators as ind

# ==================================================================== #
#                                                                      #
# ==================================================================== #
# ohlc = pd.read_parquet("./data/binance-BTCUSDT-1h.parquet")
# ohlc.reset_index(inplace=True)


datas = {}
assets = find_files("./data/", "@ENQ")
assets
for asset in assets:
    datas[asset.split("/")[2].split(".")[0]] = pd.read_parquet(asset)

data = datas["@ENQ-M1"].copy()
data["Date"] = time_manip.convert_s_to_datetime(data["time"])
data.drop(["time"], inplace=True, axis=1)
data

data = data[-1000:-950]

# |%%--%%| <1tMhyNzPrG|7W30XJ9kt4>

import os
from quantbt.lib import np, timeit, pd, find_files
from quantbt.indicators import cross_above, cross_below


class S_signals(S_base):
    def generate_signals(self):
        long, short, cutoff = params
        close = data.close

        # self.ma_long = ta.sma(close, length=long)
        # self.ma_short = ta.sma(close, length=short)
        self.ma_short = talib.SMA(close, length=short)
        self.ma_long = talib.SMA(close, length=long)

        self.long = cross_above(self.ma_short, self.ma_long)
        self.short = cross_below(self.ma_short, self.ma_long)

        return {
            "long_entries": self.long,
            "long_exits": self.short,
            "short_entries": self.short,
            "short_exits": self.long,
            # 'long_entries' : np.full(self.long.shape, False),
            # 'long_exits' : np.full(self.long.shape, False),
            # 'short_entries' : np.full(self.long.shape, False),
            # 'short_exits' : np.full(self.long.shape, False),
        }

    def plot(self):
        data = self.data.copy()
        data.index = pd.to_datetime(data.index, unit="s")
        plotting.mpf_plot(
            data,
            [
                plotting.add_line_plot(self.supert, color="teal"),
                plotting.add_line_plot(self.equity, color="teal", panel=1),
                plotting.add_line_plot(self.sma, color="blue"),
                plotting.add_markers(self.entries, data, color="green"),
                plotting.add_markers(self.exits, data, color="red"),
            ],
        )


st = S_signals(
    data,
    commission=1.2,
    commission_type=CommissionType.FIXED,
    multiplier=4,
    data_type=DataType.OHLC,
    initial_capital=100_000,
    default_trade_size=1,
    trade_size_type=TradeSizeType.FIXED,
)

params = (10, 5, 4)
st.from_signals(params)

st.stats()
trades = st.trades()
trades.drop(
    ["IDX", "TIME_SL", "SL", "TP", "Direction", "CloseReason", "Extra"],
    inplace=True,
    axis=1,
)

df = pd.DataFrame({"entry": st.long, "exit": st.short}, index=data["Date"])
# df.index = time_manip.convert_datetime_to_ms(df.index)
df[df["exit"]]
df.reset_index(inplace=True)

# data['Date'][df[df['exit']]]
# trades['EntryTime'] = time_manip.convert_datetime_to_ms(trades['EntryTime'])
# print((15681.5 - 15683.5 ) * 4  - 1.2 * 2)
trades["PNL"].sum()
trades


# |%%--%%| <7W30XJ9kt4|Ufsl8mlq0u>


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
df
data
time_manip.convert_datetime_to_ms(data["Date"])

# Apply the function to create the new column


# rsi_scatter_high = data['high']
# rsi_scatter_low = data['high']

indicators_data = pd.DataFrame(
    {"ma1": st.ma_long, "ma2": st.ma_short, "equity": st.bt.data_module.equity}
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

save_data(UI_LOCATION, df, indicators, indicators_data)
