import quantbt as qbt

data = qbt.data.random_data(seed=100)[0]
data = data[0:100]
print(data)

# |%%--%%| <buvm7UY7E3|sER6Ds1yb6>

import quantbt.indicators as ind
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

# |%%--%%| <sER6Ds1yb6|W54lGn76sg>


params = (5, 23)
st.from_signals(params)

# |%%--%%| <W54lGn76sg|kyNcaksumQ>

stats = st.get_stats()
trades = st.get_trades()

trades
st.plot_equity()


# |%%--%%| <kyNcaksumQ|hXyNLgp1ap>


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

# |%%--%%| <hXyNLgp1ap|KDyH6XJazs>

plotting.add_markers(st.long, data.close)
