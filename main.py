from quantbt.strategies.S_test import S_Test

from quantbt.lib import np, timeit, pd
from quantbt.lib import find_files, optimize

# df = pd.read_parquet("./binance-BTCUSDT-1h-RSI.parquet")
# df
#
#
# # |%%--%%| <o5y8KFNmnb|PSegVofl0P>


assets = find_files("./data/", "binance")
assets

for asset in assets:
    print(asset)
    sym = asset.split("/")[-1].split(".")[0]
    data = pd.read_parquet(asset)

    optimisation = optimize(
        data,
        S_Test,
        long=range(200, 300, 1),
        short=range(5, 55, 1),
        rsi=range(3, 15, 1),
        atr_distance=np.arange(0.5, 10.5, 0.5),
    )
    optimisation = optimisation.sort_values("ratio", ascending=False)
    optimisation.to_parquet(f"{sym}-RSI.parquet")

# |%%--%%| <PSegVofl0P|W9pyX2nkWW>

from quantbt.strategies.S_test import S_Test

from quantbt.lib import np, timeit, pd
from quantbt.lib import find_files, optimize


assets = find_files("./data/@ENQ.time", "1m")
data = pd.read_parquet(assets[0])
data

# data = data[0:500]


def single():
    bt = S_Test(data)
    bt.backtest((208, 6, 14, 10))
    return bt


import time

start = time.time()
pf = single()
end = time.time()

print(end - start)
# pf.print_trades()
# pf.plot_equity()
# pf.plot_ohlc()
# pf.stats

# |%%--%%| <W9pyX2nkWW|40lFm5vOxI>


count = 30
execution_time = timeit.timeit(single, number=count)
print(f"Average execution time: {execution_time / count} seconds")
