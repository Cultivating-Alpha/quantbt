from quantnb.lib import np, pd, time_manip
from quantnb.core.backtester import Backtester
from quantnb.core.enums import CommissionType, DataType
from quantnb.lib.output_trades import output_trades

ohlc = pd.read_parquet("./data/EURUSD.parquet")
long = pd.read_parquet("./data/long_signals.parquet")
short = pd.read_parquet("./data/short_signals.parquet")


INITIAL_CAPITAL = 10000
data = ohlc[0:15227]
data.reset_index(inplace=True)


def backtest(data, trades, initial_capital=INITIAL_CAPITAL):
    bt = Backtester(
        commission=7,
        commission_type=CommissionType.FIXED,
        initial_capital=INITIAL_CAPITAL,
        slippage=0.0000,
        data_type=DataType.BID_ASK,
        date=time_manip.convert_datetime_to_ms(data["Date"]).values,
        bid=data["EURUSD.bid"].to_numpy(dtype=np.float32),
        ask=data["EURUSD.ask"].to_numpy(dtype=np.float32),
    )
    print("running trade function")
    bt.from_trades(trades.values)

    return bt


data
time_manip.convert_ms_to_datetime(long["long_entry"])
time_manip.convert_ms_to_datetime(long["long_exit"])

print("Preparing")
bt = backtest(data, long)


# stats = calculate_stats(data, bt)
trades = output_trades(bt)
# trades

# # trades[:-1]
# #
# # # trades[:-1]["PNL"].sum()
# trades
# print(trades["PNL"].sum())
# # num = trades["PNL"].sum()
# # num
# # 10000 - 378
# # trades
# # # #
# # # trades
# # # bt.closed_trades
# # bt.active_trades
# # bt.trades
# #
# # trades
# # data
