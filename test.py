from quantnb.lib import pd, find_files, np, optimize
from quantnb.strategies.S_test import S_Test
import os

# from quantnb.strategies.S_MACD import S_MACD


# # assets = find_files("./data/@ENQ.time", "1h")
# assets = find_files("./data/", "arbitrum")
#
# assets = [assets[0]]
# assets
#
# data = pd.read_parquet(assets[0])
# data


def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


def test_btc():
    assets = find_files("./data/", "arbitrum")
    data = pd.read_parquet(assets[0])
    data = data[303:]
    params = (113, 35, 3, 0.5)
    bt = S_Test(data, commission=0.0005)
    bt.backtest(params)
    print(bt.stats)


test_btc()


# |%%--%%| <NaCTS8fbAy|DDM84Pf7qj>


def test_eth():
    assets = find_files("./data/", "arbitrum")
    data = pd.read_parquet(assets[1])
    print(data)
    data = data[303:]
    params = (116, 27, 3, 6.5)
    bt = S_Test(data, commission=0.0005)
    bt.backtest(params)
    print(bt.stats)


test_eth()

# data
# pf = single((113, 35, 3, 0.5), use_sl=False)
# pf.print_trades()
# pf.plot_equity()

# |%%--%%| <DDM84Pf7qj|OlIp3y1SNo>

# data = data[0:500]


# pf = single((208, 6, 14, 10), use_sl=False)
# # pf.print_trades()
# # pf.plot_equity()
# print(pf.stats)

# pf = single((2, 200, 14, 17, 99, 16, 26, 9), use_sl=False)
# pf.stats

for asset in assets:
    print(asset)
    sym = asset.split("/")[-1].split(".")[0]
    data = pd.read_parquet(asset)

    for i in range(0, 9):
        out = f"./optimisation/{sym}-RSI-{i}.parquet"
        if not file_exists(out):
            print(i)
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

btc = pd.read_parquet("./optimisation/uniswap_v3-arbitrum-WBTC-USDC-4h-RSI.parquet")
btc
eth = pd.read_parquet("./optimisation/uniswap_v3-arbitrum-WETH-USDC-4h-RSI.parquet")
eth


# btc = btc[btc["ratio"] > 3]
# eth = eth[eth["ratio"] > 3]
# btc
# btc.index
# eth


eth = make_index_hashable(eth)
btc = make_index_hashable(btc)
# |%%--%%| <fyEEXxs4h1|3c8AUijbdp>


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
btc
btc.to_parquet("./optimisation/BTC.parquet")
eth.to_parquet("./optimisation/ETH.parquet")


# merged_df = pd.merge(eth["ratio"], btc["ratio"], left_index=True, right_index=True)
# merged_df
# |%%--%%| <3c8AUijbdp|rg0QhpEN2e>


btc = make_index_hashable(pd.read_parquet("./optimisation/BTC.parquet"))
eth = make_index_hashable(pd.read_parquet("./optimisation/ETH.parquet"))
btc = btc.sort_values(by=["ratio"], ascending=False)
eth = eth.sort_values(by=["ratio"], ascending=False)
print(btc)
print(eth)

merged_df = pd.merge(eth["ratio"], btc["ratio"], left_index=True, right_index=True)
merged_df

df = merged_df[merged_df["ratio_x"] > 3]
df = merged_df[merged_df["ratio_y"] > 3]
df = df.sort_values(by=["ratio_x", "ratio_y"], ascending=False)
df.head(50)

# merged_df["ratio_y"].sort_values(ascending=False)
# merged_df.sort_values(by=["ratio_x", "ratio_y"], ascending=False)
