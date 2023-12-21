import math
import time
import itertools
import numpy as np
import multiprocessing
import pandas as pd
from tqdm import tqdm
from quantbt.data.resample import resample


def optimize(
    strategy=None,
    data=None,
    backtest_vars=None,
    strategy_vars=None,
    timeframes=[],
    params=None,
):
    products = list(itertools.product(*params.values()))
    items = []
    for item in products:
        items.append(
            tuple(
                round(value, 2) if isinstance(value, float) else value for value in item
            )
        )

    for tf in timeframes:
        pbar = tqdm(total=len(items), ncols=40)
        _data = resample(data, tf)
        st = strategy(_data, strategy_vars)
        st.set_backtester_settings(**backtest_vars)
        new_df = pd.DataFrame()
        for param in items:
            st.from_signals(param, verbose=False)
            stats, t = st.get_stats()
            new_df = pd.concat([new_df, stats])
            pbar.update(1)

        new_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        new_df.dropna(inplace=True)
        print("Optimising", strategy.name, tf)
        print()
        print(new_df)

        new_df.index = new_df.index.map(lambda x: tuple(x))
        new_df.to_parquet(f"./optimisation/{strategy.name}-{tf}.parquet")
        pbar.close()


# def optimize(strategy, data, backtest_vars, strategy_vars, timeframes, params):
#     # NUMBER_OF_CPU = multiprocessing.cpu_count() - 1
#     NUMBER_OF_CPU = math.floor(multiprocessing.cpu_count() / 2)
#
#     def create_buckets(arrays):
#         # Check if at least one array is provided
#         if len(arrays) < 1:
#             raise ValueError("At least one array must be provided")
#
#         # Calculate the Cartesian product of the arrays
#         items = list(itertools.product(*arrays.values()))
#
#         # Calculate the length of each part
#         part_length = math.ceil(len(items) / NUMBER_OF_CPU)
#         divided_list = [
#             items[i : i + part_length] for i in range(0, len(items), part_length)
#         ]
#         return divided_list
#
#     buckets = create_buckets(params)
#
#     def worker(
#         all_params,
#         strategy,
#         data,
#         backtest_vars,
#         strategy_vars,
#         queue,
#         iteration,
#         total,
#     ):
#         new_df = pd.DataFrame()
#
#         # we use pbar to display progress bar
#         if iteration == 0:
#             pbar = tqdm(total=total, ncols=40)
#         queue.put(new_df)
#
#         st = strategy(data, strategy_vars)
#         st.set_backtester_settings(**backtest_vars)
#         for params in all_params:
#             st.from_signals(params, verbose=False)
#             stats, t = st.get_stats()
#             new_df = pd.concat([new_df, stats])
#
#             if iteration == 0:
#                 pbar.update(1)
#
#         if iteration == 0:
#             pbar.close()
#
#         queue.put(new_df)
#
#     # Create a queue to store the results
#     result_queue = multiprocessing.Queue()
#
#     for tf in timeframes:
#         _data = resample(data, tf)
#         processes = []
#         print("Starting on timeframe", tf)
#         for i in range(NUMBER_OF_CPU):
#             if i < len(buckets):
#                 p = multiprocessing.Process(
#                     target=worker,
#                     args=(
#                         buckets[i],
#                         strategy,
#                         _data,
#                         backtest_vars,
#                         strategy_vars,
#                         result_queue,
#                         i,
#                         len(buckets[i]),
#                     ),
#                 )
#                 processes.append(p)
#                 p.start()
#
#         # Collect the results from the queue
#         results = []
#         for _ in range(len(processes)):
#             result = result_queue.get()
#             results.append(result)
#
#         # Wait for all processes to complete
#         for p in processes:
#             p.join()
#
#         print("Done and done")
#         new_df = pd.DataFrame()
#         for df in results:
#             new_df = pd.concat([new_df, df])
#
#         print(new_df)
#         new_df.replace([np.inf, -np.inf], np.nan, inplace=True)
#         new_df.dropna(inplace=True)
#         print("Optimising", strategy.name, tf)
#         print()
#         print(new_df)
#         new_df.to_parquet(f"./optimisation/{strategy.name}-{tf}.parquet")
