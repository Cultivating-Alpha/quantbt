from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.lib import np, timeit, pd


ohlc = pd.read_parquet("./data/EURUSD.parquet")
long_signals = pd.read_parquet("./data/long_signals.parquet")
short_signals = pd.read_parquet("./data/short_signals.parquet")

long_signals
