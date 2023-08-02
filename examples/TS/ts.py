from quantnb.lib import pd, find_files, np, optimize
from quantnb.strategies.S_test import S_Test
import os

# from quantnb.strategies.S_MACD import S_MACD

# |%%--%%| <NaCTS8fbAy|96njygS0NI>


assets = find_files("./data/", "binance")
assets


def test(asset_index=0):
    data = pd.read_parquet(assets[asset_index])
    print(data)
    data = data[303:]
    params = (116, 27, 3, 6.5)
    bt = S_Test(data, commission=0.0005)
    bt.backtest(params)
    print(bt.stats)


assets[1]
# test(0)  # BTC
# test(1)  # ETH

# pf = single((113, 35, 3, 0.5), use_sl=False)
# pf.print_trades()
# pf.plot_equity()

# |%%--%%| <96njygS0NI|OlIp3y1SNo>

# data = data[0:500]


# pf = single((208, 6, 14, 10), use_sl=False)
# # pf.print_trades()
# # pf.plot_equity()
# print(pf.stats)

# pf = single((2, 200, 14, 17, 99, 16, 26, 9), use_sl=False)
# pf.stats

from quantnb.lib import pd, find_files, np, optimize
from quantnb.strategies.S_test import S_Test
import os


def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


assets = find_files("./data/", "arbitrum")
assets = [assets[1]]
assets
for asset in assets:
    sym = asset.split("/")[-1].split(".")[0]
    data = pd.read_parquet(asset)
    print(asset)
    print(data)

    for i in range(0, 9):
        print(i)
        out = f"./optimisation/{sym}-RSI-{i}.parquet"
        if not file_exists(out):
            optimisation = optimize(
                data,
                S_Test,
                long=range(100 + i * 50, 150 + i * 50, 1),
                short=range(5, 55, 1),
                rsi=range(3, 15, 1),
                atr_distance=np.arange(0.5, 10.5, 0.5),
            )
            optimisation = optimisation.sort_values("ratio", ascending=False)
            optimisation.to_parquet(f"./optimisation/{sym}-RSI-{i}.parquet")

# |%%--%%| <OlIp3y1SNo|fyEEXxs4h1>


from quantnb.lib import pd, find_files, np, optimize
import time


def make_index_hashable(df):
    df.index = [tuple(idx) for idx in df.index]
    return df


def get_opti_files(asset):
    assets = find_files("./optimisation/", asset)
    assets
    df = pd.DataFrame()
    for asset in assets:
        newdf = pd.read_parquet(asset)
        df = pd.concat([df, newdf])

    return make_index_hashable(df)


start = time.time()
eth = get_opti_files("WETH")
btc = get_opti_files("WBTC")
end = time.time()
print(end - start)
btc.to_parquet("./optimisation/BTC.parquet")
eth.to_parquet("./optimisation/ETH.parquet")
btc


# merged_df = pd.merge(eth["ratio"], btc["ratio"], left_index=True, right_index=True)
# merged_df
# |%%--%%| <fyEEXxs4h1|rg0QhpEN2e>


btc = make_index_hashable(pd.read_parquet("./optimisation/BTC.parquet"))
eth = make_index_hashable(pd.read_parquet("./optimisation/ETH.parquet"))
btc = btc.sort_values(by=["ratio"], ascending=False)
eth = eth.sort_values(by=["ratio"], ascending=False)
print(btc)
print(eth)

# merged_df = pd.merge(eth["ratio"], btc["ratio"], left_index=True, right_index=True)
# merged_df
#
# df = merged_df[merged_df["ratio_x"] > 3]
# df = merged_df[merged_df["ratio_y"] > 3]
# df = df.sort_values(by=["ratio_x", "ratio_y"], ascending=False)
# df.head(50)

# merged_df["ratio_y"].sort_values(ascending=False)
# merged_df.sort_values(by=["ratio_x", "ratio_y"], ascending=False)
# |%%--%%| <rg0QhpEN2e|b7vsCmozbi>


btc = pd.read_parquet("./optimisation/BTC.parquet")

df = btc[btc["ratio"] > 3]
df.columns
df = df[df["total_return"] > 20]
df
# |%%--%%| <b7vsCmozbi|vfMWmlVgNK>

eth = pd.read_parquet("./optimisation/ETH.parquet")
df = eth[eth["ratio"] > 3]
# df.columns
df = df[df["total_return"] > 20]
df.sort_values(by=["dd"], ascending=True)

# |%%--%%| <vfMWmlVgNK|FfNJZ4eSQj>

import datetime

start_at = datetime.datetime(2021, 11, 30)
end_at = datetime.datetime(2023, 6, 4)
# Get the number of years between 2 start_at and end_at
years = (end_at - start_at).days / 365


df["annualized"] = ((df["final_value"] / 10000) ** (1 / years) - 1) * 100
df["new R"] = df["annualized"] / df["dd"]
df.sort_values(by=["new R"], ascending=False)

# |%%--%%| <FfNJZ4eSQj|4MpZvaZ27f>

df = pd.read_parquet("./data/uniswap_v3-arbitrum-WBTC-USDC-4h.parquet")
df = pd.read_parquet("./data/uniswap_v3-arbitrum-WETH-USDC-4h.parquet")
df.reset_index(inplace=True)
df["Date"].iloc[-1] - df["Date"].iloc[0]
# |%%--%%| <4MpZvaZ27f|6Pxufe7CMX>


import numpy as np


def calculate_cagr(beginning_value, ending_value, num_years):
    cagr = (ending_value / beginning_value) ** (1 / num_years) - 1
    return cagr


# Example calculation
beginning_value = 100
ending_value = 200
num_years = 2

cagr = calculate_cagr(beginning_value, ending_value, num_years)
print(f"CAGR: {cagr:.2%}")
