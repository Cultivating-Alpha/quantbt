from strategies.S_test import S_Test

from lib import np, timeit, pd
from lib import find_files, optimize

assets = find_files("./data/", "WBNB-BUSD")
data = pd.read_parquet(assets[0])

optimisation = optimize(
    data,
    S_Test,
    long=range(200, 300, 10),
    short=range(5, 55, 5),
    rsi=range(3, 15, 1),
    atr_distance=np.arange(0.5, 10.5, 0.5),
)

optimisation.sort_values("ratio", ascending=False).head(10)

# |%%--%%| <VxNjYXtfcf|iGQ2RvriLW>

# assets = find_files("./data/@ENQ.steps", "ENQ-10.")
# assets = find_files("./data/@ENQ.time", "3min")
# assets = find_files("./data/", "WMATIC-USDC-4h")
assets = find_files("./data/", "WBNB-BUSD")
assets
data = pd.read_parquet(assets[0])


def single():
    bt = S_Test(data)
    bt.backtest((210, 10, 12, 6))
    return bt


pf = single()
pf.stats

count = 30
execution_time = timeit.timeit(single, number=count)
print(f"Average execution time: {execution_time / count} seconds")
