import numpy as np
import itertools
import pandas as pd

long_range = range(200, 300, 1)
short_range = range(5, 55, 1)
rsi_cutt_range = range(3, 15, 1)
atr_distance_range = np.arange(0.5, 10.5, 0.5)


total_combinations = list(
    itertools.product(long_range, short_range, rsi_cutt_range, atr_distance_range)
)
total_combinations[0]

NUMBER_OF_CPU = 24

# Calculate the length of each part
part_length = len(total_combinations) // NUMBER_OF_CPU

# Divide the list into 12 equal parts
divided_list = [
    total_combinations[i : i + part_length]
    for i in range(0, len(total_combinations), part_length)
]

import multiprocessing
from strategies.S_rsi import S_rsi

from tqdm import tqdm


def my_function(asset, asset_short, args, iteration):
    bt = S_rsi(asset)

    df = pd.DataFrame()
    pbar = tqdm(total=len(args), ncols=40)
    for i in range(len(args)):
        result = bt.backtest(args[i])

        newdf = pd.DataFrame(result, index=[0])
        df = pd.concat([df, newdf])
        # print(f"{ i } / {len(args)}")

        if iteration == 0:
            pbar.update(1)
    df.to_parquet(f"./optimisation/{asset_short}-optimisation-{iteration}.parquet")
    pbar.close()


processes = []

# Spawn 20 processes
asset = "./data/uniswap_v3-ethereum-WETH-USDC-4h.parquet"
asset_short = "WETH-USDC"

# asset = "./data/uniswap_v3-polygon-WMATIC-USDC-4h.parquet"
# asset_short = "WMATIC-USDC"
for i in range(NUMBER_OF_CPU):
    p = multiprocessing.Process(
        target=my_function, args=(asset, asset_short, divided_list[i], i)
    )
    processes.append(p)
    p.start()

# Wait for all processes to complete
for p in processes:
    p.join()
