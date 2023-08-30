import numpy as np
import pandas as pd
import mplfinance as mpf
from quantbt.core.backtester import Backtester

from quantbt.strategies.S_base import S_base
from quantbt.lib import find_files, plotting
from quantbt.indicators import supertrend, talib_SMA, cross_below, cross_above
from quantbt.helpers.S_calculate_metrics import calculate_dd
from quantbt.core.enums import DataType, CommissionType
from quantbt.lib.output_trades import output_trades
from quantbt.lib import plotting

datas = {}

# assets = find_files("./data", "quickswap")
#
# for asset in assets:
#     print(asset)
#     df = pd.read_parquet(asset)
#     df.rename(
#         {"Open": "open", "High": "high", "Low": "low", "Close": "close"},
#         axis=1,
#         inplace=True,
#     )
#     datas[asset.split("/")[2]] = df
#
# assets = find_files("./data", "uniswap_v2")
#
#
#
# for asset in assets:
#     print(asset)
#     df = pd.read_parquet(asset)
#     df.rename(
#         {"Open": "open", "High": "high", "Low": "low", "Close": "close"},
#         axis=1,
#         inplace=True,
#     )
#     datas[asset.split("/")[2]] = df
#
#
# assets = find_files("./data", "uniswap_v3-ethereum-WETH-USDC-1h")
# # (ChainId.ethereum, "uniswap-v3", "WETH", "USDC", 0.0005) # Ether-USD Coin https://tradingstrategy.ai/trading-view/ethereum/uniswap-v3/eth-usdc-fee-5#30d
#
#
# for asset in assets:
#     print(asset)
#     df = pd.read_parquet(asset)
#     df.rename(
#         {"Open": "open", "High": "high", "Low": "low", "Close": "close"},
#         axis=1,
#         inplace=True,
#     )
#     datas[asset.split("/")[2]] = df
#

assets = find_files("./data", "binance")

for asset in assets:
    datas[asset.split("-")[1]] = pd.read_parquet(asset)


keys = list(datas.keys())
keys


#|%%--%%| <QOLZRGlTWs|8Ff7T6o8dm>


class S_basket(S_base):
    def generate_signals(self):
        supert_period, supert_multiplier, sma_period = self.params
        df = self.data
        supert = supertrend(
            df.High.values,
            df.Low.values,
            df.Close.values,
            period=supert_period,
            multiplier=supert_multiplier,
        )[0]
        sma = talib_SMA(df.Close.values, period=sma_period)

        self.supert = supert
        self.sma = sma
        self.entries = np.logical_and(
            cross_above(df.Close, supert), df.Close> sma
        )
        self.exits = cross_below(df.Close, supert)

        return {
            'long_entries' : self.entries,
            'long_exits' : self.exits,
            'short_entries' : self.exits,
            'short_exits' : self.entries,
            'long_entry_price' : df.Close.values,
            'short_entry_price' : df.Close.values,
            'default_size': 0.99
        }

        return 

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


MAIN_OFFSET = -1
print(f"Data length is {MAIN_OFFSET}")


def backtest(datas, key, offset, params):
    stats = pd.DataFrame()
    initial_capital = 10000
    # data = datas["ETHUSDT"]
    # data = data[49000:]

    # data[27468:]
    # data
    data = datas[key]
    # data = data[offset:]
    data = data[-MAIN_OFFSET:]

    st = S_basket(data, 
                  commission=0.0005, 
                  commission_type=CommissionType.PERCENTAGE,
                  data_type=DataType.OHLC,
                  initial_capital=initial_capital
                  )
    st.from_signals(params)
    return st


key = keys[0]
print("========================", key)
st = backtest(datas, key, 0, (10, 3, 200))
print(st.stats())
st.plot_equity()

# trades = st.trades()


print()
key = keys[1]
print("========================", key)
st = backtest(datas, key, 3050, (10, 3, 200))
print(st.stats())
st.plot_equity()


print()
key = keys[2]
print("========================", key)
st = backtest(datas, key, 27448, (10, 3, 200))
print(st.stats())
st.plot_equity()


# print()
# key = keys[3]
# print("========================", key)
# bnb_bt = backtest(datas, key, 27448, (10, 3, 200))
# bnb_bt.stats()


# |%%--%%| <8Ff7T6o8dm|tyKjQNkEFs>


#
quick = datas[keys[0]][-MAIN_OFFSET:]
uni = datas[keys[1]][-MAIN_OFFSET:]
v3 = datas[keys[2]][-MAIN_OFFSET:]
bnb = datas[keys[3]][-MAIN_OFFSET:]
#
correlation_matrix = quick.corrwith(uni)

uni.corrwith(bnb)


df = pd.DataFrame(
    {
        "uni": uni.close.values,
        "bnb": bnb.close.values,
        "quick": quick.close.values,
        "v3": v3.close.values,
    }
)
df.tail()


# plotting.mpf_plot(quick, [])
plotting.mpf_plot(
    bnb,
    [
        plotting.add_line_plot(bnb_bt.supert, color="red"),
        # plotting.add_line_plot(bnb_bt.sma, color="red"),
        # plotting.add_line_plot(uni.close.values, color="gray"),
        plotting.add_line_plot(uni_bt.supert, color="black"),
        # plotting.add_line_plot(uni_bt.sma, color="orange"),
    ],
    type="line",
)
# plotting.mpf_plot(bnb, [])


# |%%--%%| <tyKjQNkEFs|UaV6o1ZohE>

INITIAL_CAPITAL = 1000 * 13
initial_capital = INITIAL_CAPITAL / len(datas.keys())
equities = []

for key in datas:
    data = datas[key]
    st = S_basket(data, commission=0.0005, initial_capital=initial_capital)
    st.backtest((10, 3, 200))
    df = pd.DataFrame(st.equity, index=data.index)
    equities.append(df)
    stats = pd.concat([stats, st.stats])
stats.index = datas.keys()


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
