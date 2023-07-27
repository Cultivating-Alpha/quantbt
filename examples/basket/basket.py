import numpy as np
import pandas as pd
import mplfinance as mpf
from quantnb.core.backtester import Backtester
from quantnb.strategies.S_base import S_base
from quantnb.lib import find_files, plotting
from quantnb.indicators import supertrend, SMA, cross_below, cross_above
from quantnb.helpers.S_calculate_metrics import calculate_dd

assets = find_files("./data", "binance")

datas = {}
for asset in assets:
    datas[asset.split("-")[1]] = pd.read_parquet(asset)


# |%%--%%| <h1NJ8eCQd7|s4tvHELefh>

data = datas["BTCUSDT"]
# data = data[0:3000]


class S_basket(S_base):
    def generate_signals(self, params=(10, 3, 200)):
        supert_period, supert_multiplier, sma_period = params
        df = self.data
        supert = supertrend(
            df.High.values,
            df.Low.values,
            df.Close.values,
            period=supert_period,
            multiplier=supert_multiplier,
        )[0]
        sma = SMA(df.Close.values, period=sma_period)

        self.supert = supert
        self.sma = sma

        self.entries = np.logical_and(
            cross_above(df.Close.values, supert), data.close > sma
        ).values
        self.exits = cross_below(df.Close.values, supert)

    def get_signals(self, params):
        self.generate_signals(params)

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


stats = pd.DataFrame()
INITIAL_CAPITAL = 1000 * 13
initial_capital = INITIAL_CAPITAL / len(datas.keys())
equities = []
data = datas["BTCUSDT"]
st = S_basket(data, commission=0.0005, initial_capital=initial_capital)
st.backtest((10, 3, 200))

# |%%--%%| <s4tvHELefh|UaV6o1ZohE>
for key in datas:
    data = datas[key]
    st = S_basket(data, commission=0.0005, initial_capital=initial_capital)
    st.backtest((10, 3, 200))
    df = pd.DataFrame(st.equity, index=data.index)
    equities.append(df)
    stats = pd.concat([stats, st.stats])
stats.index = datas.keys()

stats

eq = pd.DataFrame()
for index, key in enumerate(datas):
    eq[key] = equities[index]
eq["sum"] = eq.sum(axis=1)

final_value = eq["sum"].iloc[-1]


total_return = ((final_value / INITIAL_CAPITAL) - 1) * 100
dd = calculate_dd(eq["sum"])
ratio = total_return / abs(dd)

stats = pd.DataFrame(
    {
        "initial_value": INITIAL_CAPITAL,
        "final_value": final_value,
        "dd": dd,
        "total_return": total_return,
        "ratio": ratio,
        # "buy_and_hold": buy_and_hold,
    },
    index=[0],
)
stats

# eq["sum"].plot()
# plt.show()
