import pandas as pd
import itertools
from tqdm import tqdm
from . import find_files, multiprocess
from quantbt.core.enums import StrategyType


def optimize(data, strategy, strategy_settings, strategy_type, **kwargs):
    kwargs = list(kwargs.values())
    total_combinations = list(itertools.product(*kwargs))
    print("Total combinations to test: ", len(total_combinations))

    def execution(params, NUMBER_OF_CPU, iteration, *args):
        df = pd.DataFrame()

        # we use pbar to display progress bar
        pbar = tqdm(total=len(params * NUMBER_OF_CPU), ncols=40)

        for param in params:
            # stats = strategy(data, param)

            st = strategy(data, **strategy_settings)
            if strategy_type == StrategyType.FROM_SIGNALS:
                st.from_signals(param)
            stats = st.get_stats()

            df = pd.concat([df, stats])

            if iteration == 0:
                pbar.update(NUMBER_OF_CPU)
        pbar.close()
        return df

    results = multiprocess(
        total_combinations, execution, data, strategy, strategy_settings
    )
    df = pd.concat(results)
    return df
