import numpy as np
import pandas as pd
import os
import mplfinance as mpf
from quantbt.core.backtester import Backtester
from quantbt.strategies.S_base import S_base
from quantbt.lib import find_files, plotting, optimize
from quantbt.indicators import supertrend, SMA, cross_below, cross_above
from quantbt.helpers.S_calculate_metrics import calculate_dd

assets = find_files("./data", "@ENQ")

datas = {}
for asset in assets:
    datas[asset.split(".")[1].split("/")[2]] = pd.read_parquet(asset)

data = datas["@ENQ-M1"]
data.set_index("time", inplace=True)
data = data[-1000000:]
data = data.resample("15min").agg(
    {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
    }
)
data = data.dropna()
data
# data.to_parquet("./data/@ENQ-5min.parquet")
# data = pd.read_parquet("./data/@ENQ-5min.parquet")
# data
# data = data[0:10000]

# |%%--%%| <gmjtoX5gF4|WCmcTE6VOz>


class S_futures(S_base):
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
            type="line",
        )


stats = pd.DataFrame()
INITIAL_CAPITAL = 100000
equities = []
st = S_futures(
    data,
    commission_type="fixed",
    initial_capital=INITIAL_CAPITAL,
    # commission=0.6,
    # multiplier=2,
    commission=1.2,
    multiplier=20,
    default_size=1,
)

import time

start = time.time()
st.backtest((10, 3, 570))
end = time.time()
print(end - start)
print(st.stats)

st.plot()
# trades = st.print_trades()


# |%%--%%| <WCmcTE6VOz|Qc2wMbX8H6>


st = S_futures(
    data,
    commission_type="fixed",
    initial_capital=INITIAL_CAPITAL,
    # commission=0.6,
    # multiplier=2,
    commission=1.2,
    multiplier=20,
    default_size=1,
)
st.backtest((12, 2, 570))
print(st.stats)
st.plot()

# |%%--%%| <Qc2wMbX8H6|kuSAJR2PZi>

bt = S_futures(
    data,
    commission_type="fixed",
    initial_capital=INITIAL_CAPITAL,
    # commission=0.6,
    # multiplier=2,
    commission=1.2,
    multiplier=20,
    default_size=1,
)


def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


sym = "@ENQ"
for i in range(0, 50):
    out = f"./optimisation/{sym}-super-{i}.parquet"
    if not file_exists(out):
        optimisation = optimize(
            data,
            S_futures,
            INITIAL_CAPITAL,
            # data,
            # S_futures,
            # strategy_params=("fixed", INITIAL_CAPITAL, 1.2, 20, 1),
            supert_period=range(8, 24, 1),
            supert_multiplier=range(2, 15, 1),
            ma=range(100 + i * 10, 110 + i * 10, 1),
        )
        optimisation = optimisation.sort_values("ratio", ascending=False)
        optimisation.to_parquet(f"./optimisations/{sym}-super-{i}.parquet")

# optimisation = optimisation.sort_values("ratio", ascending=False)
# optimisation.to_parquet(f"./optimisation/{sym}-RSI-{i}.parquet")


# |%%--%%| <kuSAJR2PZi|6SqqlVCaz6>
#
# st.plot()

# df = pd.DataFrame(st.equity)
# df.index = pd.to_datetime(st.data.index, unit="s")
# df.plot()
# plt.show()
#
# # |%%--%%| <6SqqlVCaz6|ufVUlUi9za>
#
# trades = st.print_trades()
# # trades["pnl"].sum()
# # st.equity
# |%%--%%| <ufVUlUi9za|7utj5xoVZm>


from quantbt.lib import pd, find_files, np, optimize
import time


def make_index_hashable(df):
    df.index = [tuple(idx) for idx in df.index]
    return df


def get_opti_files(asset):
    assets = find_files("./optimisations/", asset)
    assets
    df = pd.DataFrame()
    for asset in assets:
        newdf = pd.read_parquet(asset)
        df = pd.concat([df, newdf])

    return make_index_hashable(df)


start = time.time()
enq = get_opti_files("@ENQ")
enq
enq.sort_values("dd", ascending=True).head(30)
