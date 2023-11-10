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
    for trade in active_trades:  # (1)!
        # Pass if we have already moved the SL to breakeven
        if trade[Trade.EntryPrice.value] == trade[Trade.SL.value]:  # (2)!
            continue

        entry_index = trade[Trade.Index.value]  # (3)!
        trade_entry_low = data.low[int(entry_index)]  # (4)!
        trade_entry_high = data.high[int(entry_index)]

        direction = trade[Trade.Direction.value]

        if direction == OrderDirection.SHORT.value:
            if current_low < trade_entry_low:
                trade[Trade.SL.value] = trade[Trade.EntryPrice.value]  # (5)!
        else:
            if current_high > trade_entry_high:
                trade[Trade.SL.value] = trade[Trade.EntryPrice.value]


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

# |%%--%%| <CxTRvz23qs|WLPXhGe6Vt>

params = (5, 23)

"""
Run the backtester without stop to be
"""
st = MyStrategy(data, **strategy_settings)
st.from_signals(params)

"""
Run the backtester with stop to be
"""
st_with_be = MyStrategy(data, stop_to_be=stop_to_be_nb, **strategy_settings)
st_with_be.from_signals(params)


stats = st.get_stats()
stats_with_be = st_with_be.get_stats()

print("Stats without stop to BE:")
print(stats)

print()
print("Stats with stop to BE:")
print(stats_with_be)
