import pandas_ta as ta
from quantnb.lib import find_files, pd
import talib
import time
import numpy as np
from prettytable import PrettyTable


datas = {}
assets = find_files("./data", "binance")

for asset in assets:
    datas[asset.split("-")[1]] = pd.read_parquet(asset)


keys = list(datas.keys())

data = datas[keys[0]]
print(data)


# |%%--%%| <67lVNdHohg|ud493qJ1DW>


# correlation_matrix = ta_sma.corr(talib_sma)
# print(correlation_matrix)
def get_time(library, function, data=None, **args):
    start = time.time()
    result = getattr(library, function)(data, **args)
    end = time.time()
    ta_time = end - start
    return np.round(ta_time, 10)


t = PrettyTable(["Method", "Pandas_TA(s)", "Talib(s)", "Improvement"])

# ================================================================================================ #
#                                               SMA                                                #
# ================================================================================================ #
pandas_time = get_time(ta, "sma", data=data["close"], length=20)
talib_time = get_time(talib, "SMA", data=data["close"], timeperiod=20)
improvement = f"{np.round((pandas_time - talib_time) / pandas_time * 100, 2)}%"
t.add_row(["SMA", pandas_time, talib_time, improvement])

# ================================================================================================ #
#                                               EMA                                                #
# ================================================================================================ #
pandas_time = get_time(ta, "ema", data=data["close"], length=20)
talib_time = get_time(talib, "EMA", data=data["close"], timeperiod=20)
improvement = f"{np.round((pandas_time - talib_time) / pandas_time * 100, 2)}%"
t.add_row(["EMA", pandas_time, talib_time, improvement])

# ================================================================================================ #
#                                               ATR                                                #
# ================================================================================================ #
pandas_time = get_time(
    ta, "atr", data=data["high"], low=data["low"], close=data["close"], length=14
)
talib_time = get_time(
    talib,
    "ATR",
    data=data["high"],
    low=data["low"],
    close=data["close"],
    timeperiod=14,
)
improvement = f"{np.round((pandas_time - talib_time) / pandas_time * 100, 2)}%"
t.add_row(["ATR", pandas_time, talib_time, improvement])


# ================================================================================================ #
#                                       Bollinger Bands                                            #
# ================================================================================================ #
pandas_time = get_time(ta, "bbands", data=data["close"], length=20)
talib_time = get_time(talib, "BBANDS", data=data["close"], timeperiod=20)
improvement = f"{np.round((pandas_time - talib_time) / pandas_time * 100, 2)}%"
t.add_row(["Bollinger Bands", pandas_time, talib_time, improvement])


# ================================================================================================ #
#                                         Print OUTPUT                                             #
# ================================================================================================ #
print(t)
