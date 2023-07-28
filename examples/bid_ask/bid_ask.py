from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.strategies.S_base import S_base
from quantnb.lib import np, timeit, pd, time_manip, calculate_stats
from quantnb.core.backtester import Backtester
from numba import njit
from quantnb.lib.output_trades import output_trades


ohlc = pd.read_parquet("./data/EURUSD.parquet")
long = pd.read_parquet("./data/long_signals.parquet")
short = pd.read_parquet("./data/short_signals.parquet")

# |%%--%%| <U8YDjUSDd1|H1CABp95z6>

INITIAL_CAPITAL = 10000
data = ohlc[0:2000015]
data.reset_index(inplace=True)


def backtest(data, trades, initial_capital=INITIAL_CAPITAL):
    bt = Backtester(
        commission=7,
        commission_type="fixed",
        initial_capital=initial_capital,
        slippage=0.0002,
    )
    bt.set_bid_ask_data(
        time_manip.convert_datetime_to_ms(data["Date"]).values,
        data["EURUSD.bid"].values,
        data["EURUSD.ask"].values,
    )

    bt.from_trades(trades.values)

    return bt


bt = backtest(data, long)

stats = calculate_stats(data, bt)
trades = output_trades(bt)
# trades[:-1]
#
# # trades[:-1]["PNL"].sum()
trades
print(trades["PNL"].sum())
# num = trades["PNL"].sum()
# num
# 10000 - 378
# trades
# # #
# # trades
# # bt.closed_trades
# bt.active_trades
# bt.trades
#
# trades
# data


# |%%--%%| <H1CABp95z6|uqfPit33s4>

entry_price = 1.21144
exit_price = 1.21080

pnl = (exit_price - entry_price) * 100000 - 7
pnl
