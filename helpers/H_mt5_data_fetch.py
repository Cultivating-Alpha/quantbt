#!/bin/python
# import the package
import time
import pytz
import pandas as pd
import numpy as np
from numba import njit
import MetaTrader5 as mt5


server = "AMPGlobalEU-Live"
password = "c2fuoysg"
login = 672814


def init():
    mt5.initialize(server=server, login=login, password=password)
    print("READ")
    # selected = mt5.symbol_select("ENQH19", True)
    # print(selected)


@njit(cache=True)
def parse_ticks(ticks):
    new_ticks = np.empty_like(ticks)

    curr = 0
    for i in range(ticks.shape[0]):
        tick = ticks[i]
        flags = tick[6]

        if (
            flags & mt5.TICK_FLAG_LAST
            or flags & mt5.TICK_FLAG_VOLUME
            or flags & mt5.TICK_FLAG_BID
            or flags & mt5.TICK_FLAG_ASK
        ):
            new_ticks[curr] = tick
            curr += 1

    return new_ticks[:curr]


def ticks_range(asset, utc_from, utc_to):
    print("==========")
    print(asset)
    print(utc_from, utc_to)
    ticks = mt5.copy_ticks_range(asset, utc_from, utc_to, mt5.COPY_TICKS_ALL)
    print(ticks)
    new_ticks = parse_ticks(ticks)
    ticks_frame = pd.DataFrame(new_ticks)
    return ticks_frame


import datetime
from datetime import timedelta

timezone = pytz.timezone("Etc/UTC")
today = datetime.datetime(2023, 3, 11, tzinfo=timezone)


def run():
    df = pd.DataFrame()
    for i in range(1, 2):
        start = today - timedelta(days=i)
        print(start)
        print(i)
        end = today - timedelta(days=i - 1)
        print(end)

        newdf = ticks_range("MNQH23", start, end)
        print(newdf)

        df = pd.concat([newdf, df])
    df.set_index("time", inplace=True)
    df.drop(columns=["flags", "volume_real", "time_msc"], inplace=True)
    df.to_hdf(f"{asset}.full.h5", key="ticks", mode="w")
    print(df)


init()
# run()
# |%%--%%| <sKPNZoT7WB|3E3u882H0E>
#
# # import pandas as pd
# #
# # df = pd.read_hdf("./src/helpers/EURUSD.full.h5", key="ticks")
# # # df = pd.read_hdf("./src/helpers/XBTUSD.full.h5", key="ticks")
# # df
#
#
# |%%--%%| <3E3u882H0E|CLlhCG1DKh>
from H_get_CME_contract import get_contract

import datetime

# timezone = pytz.timezone("Etc/UTC")
# today = datetime.datetime(2023, 3, 11, tzinfo=timezone)
# today


def run():
    df = pd.DataFrame()
    for i in range(1, 2):
        start = today - timedelta(days=i)
        print(start)
        print(i)
        end = today - timedelta(days=i - 1)
        print(end)

        newdf = ticks_range("MNQH23", start, end)
        print(newdf)


#         df = pd.concat([newdf, df])
#     df.set_index("time", inplace=True)
#     df.drop(columns=["flags", "volume_real", "time_msc"], inplace=True)
#     df.to_hdf(f"{asset}.full.h5", key="ticks", mode="w")
#     print(df)
#
#
init()
# run()
# # |%%--%%| <CLlhCG1DKh|axH77onVAm>
#
# # import pandas as pd
# #
# # df = pd.read_hdf("./src/helpers/EURUSD.full.h5", key="ticks")
# # # df = pd.read_hdf("./src/helpers/XBTUSD.full.h5", key="ticks")
# # df
#
#
# # |%%--%%| <axH77onVAm|npyoZHlYBp>
from H_get_CME_contract import get_contract

import datetime
import pytz


timezone = pytz.timezone("Etc/UTC")
start_date = datetime.datetime(2023, 3, 1, tzinfo=timezone)
end_date = datetime.datetime.now(tz=timezone)

delta = datetime.timedelta(days=1)

while start_date <= end_date:
    contract, expiration_date = get_contract(start_date)
    print(f"On {start_date}, use {contract} contract expiring on {expiration_date}")
    newdf = ticks_range(contract, start_date, start_date + delta)
    print(newdf)

    start_date += delta
