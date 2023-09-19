import quantbt as qbt

data = qbt.data.random_data(seed=100)[0]
print(data)

# |%%--%%| <buvm7UY7E3|sER6Ds1yb6>

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
    "multiplier": 4,
    "data_type": DataType.OHLC,
    "default_trade_size": 1,
    "trade_size_type": TradeSizeType.FIXED,
}
# |%%--%%| <sER6Ds1yb6|WYW5Ijm2uh>


"""
This is how we actually backtest the strategy.
We only need to set the parameters which will be automatically passed to the st.generate_signals() function
"""
st = MyStrategy(data, **strategy_settings)

params = (5, 23)
st.from_signals(params)

# |%%--%%| <WYW5Ijm2uh|dcbhkIt8T2>

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
# |%%--%%| <IxcW591TUJ|rXAxJLw5iJ>

import os
from quantbt.lib import optimize
from quantbt.core.enums import StrategyType

param_combinations = {
    "ma_short": range(8, 100, 1),
    "ma_long": range(2, 50, 1),
}

optimisation = optimize(
    data,
    MyStrategy,
    strategy_settings,
    strategy_type=StrategyType.FROM_SIGNALS,
    **param_combinations
    # ma_short=range(8, 24, 1),
    # ma_long=range(2, 15, 1),
    # ma=range(100 + i * 10, 110 + i * 10, 1),
)
optimisation
#
# # sym = "Random Data"
# # for i in range(0, 50):
# #     out = f"./optimisation/{sym}-super-{i}.parquet"
# #     if not os.path.exists(out):
# #         optimisation = optimize(
# #             data,
# #             MyStrategy,
# #             # ma_short=range(8, 24, 1),
# #             # ma_long=range(2, 15, 1),
# #             # ma=range(100 + i * 10, 110 + i * 10, 1),
# #         )
# #         print(optimisation)
# #         # optimisation = optimisation.sort_values("ratio", ascending=False)
# #         # optimisation.to_parquet(f"./optimisations/{sym}-super-{i}.parquet")
