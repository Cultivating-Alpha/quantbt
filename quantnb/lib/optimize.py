import pandas as pd
import itertools
from tqdm import tqdm
from . import find_files, multiprocess


# def optimize(data, strategy, strategy_params=None, **kwargs):
def optimize(data, strategy, **kwargs):
    kwargs = list(kwargs.values())
    total_combinations = list(itertools.product(*kwargs))
    print("Total combinations to test: ", len(total_combinations))

    def execution(params, NUMBER_OF_CPU, iteration, *args):
        df = pd.DataFrame()

        # we use pbar to display progress bar
        pbar = tqdm(total=len(params * NUMBER_OF_CPU), ncols=40)

        for param in params:
            stats = strategy(data, param)

            df = pd.concat([df, stats])
            if iteration == 0:
                pbar.update(NUMBER_OF_CPU)
        pbar.close()
        return df

    results = multiprocess(total_combinations, execution)
    df = pd.concat(results)
    return df
