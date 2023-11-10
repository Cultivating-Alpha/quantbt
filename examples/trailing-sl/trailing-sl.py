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


# |%%--%%| <hHQyI1cQTZ|CxTRvz23qs>


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

        self.rsi = talib.RSI(data.close, timeperiod=14)
        self.trailing_sl_long, self.trailing_sl_short = calculate_trailing_exit(
            data.high.values, data.low.values, self.rsi.values
        )
        return {
            "long_entries": self.long,
            "long_exits": self.short,
            "short_entries": self.short,
            "short_exits": self.long,
            "trailing_sl_long": self.trailing_sl_long,
            "trailing_sl_short": self.trailing_sl_short,
        }


strategy_settings = {
    "initial_capital": 100_000,
    "commission": 1.2,
    "commission_type": CommissionType.FIXED,
    "multiplier": 20,
    "data_type": DataType.OHLC,
    "default_trade_size": 1,
    "trade_size_type": TradeSizeType.FIXED,
    "use_trailing_sl": False,
}

# |%%--%%| <CxTRvz23qs|WLPXhGe6Vt>

params = (5, 23)

"""
Run the backtester without stop to be
"""
st = MyStrategy(data, **strategy_settings)
st.from_signals(params)
stats = st.get_stats()
print(stats)


# Change the value of trailing_sl to TRUE
strategy_settings["use_trailing_sl"] = True
st_tsl = MyStrategy(data, **strategy_settings)
st_tsl.from_signals(params)
stats = st_tsl.get_stats()
print(stats)
