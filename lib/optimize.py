import pandas as pd
import itertools
from tqdm import tqdm
from lib import find_files, multiprocess


def optimize(data, strategy, **kwargs):
    kwargs = list(kwargs.values())
    total_combinations = list(itertools.product(*kwargs))

    def execution(params, iteration, *args):
        # Load the Data File
        assets = find_files("./data/", "WBNB-BUSD")

        df = pd.DataFrame()

        # we use pbar to display progress bar
        pbar = tqdm(total=len(params), ncols=40)

        for param in params:
            bt = strategy(data)
            bt.backtest(param)

            bt.stats.index = [param]
            df = pd.concat([df, bt.stats])
            if iteration == 0:
                pbar.update(1)
        pbar.close()
        return df

    results = multiprocess(total_combinations, execution)
    df = pd.concat(results)
    return df
