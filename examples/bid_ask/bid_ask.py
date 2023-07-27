from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.strategies.S_base import S_base
from quantnb.lib import np, timeit, pd
from numba import njit


ohlc = pd.read_parquet("./data/EURUSD.parquet")
long_signals = pd.read_parquet("./data/long_signals.parquet")
short_signals = pd.read_parquet("./data/short_signals.parquet")

long_signals


class S_bid_ask(S_base):
    def set_signals(self, long_entries, long_exits):
        self.entries = long_entries
        self.exits = long_exits

    def get_signals(self, params):
        pass


def single():
    bt = S_bid_ask(ohlc)
    bt.set_signals(long_signals["long_entry"], long_signals["long_exit"])
    bt.backtest(())
    return bt


from quantnb.core.backtester import Backtester

bt = Backtester(commissions=0.002, initial_capital=100000)
data = pd.DataFrame(
    {
        "Date": ohlc.index.astype(np.int64) // 10**6,
        "Bid": ohlc["EURUSD.bid"].values,
        "Ask": ohlc["EURUSD.ask"].values,
    }
)
data["Volume"] = 1
data["Date"].values

data = data.astype({"Date": np.int64, "Volume": np.float32})  # Set data types
# data["Date"]
# data.dtypes


# data = data[0:500000]


# single()

####====================================================================================================================####

####====================================================================================================================####


@njit
def find_first_occurrence(main_array, array2, vol):
    new_array = np.zeros((main_array.shape[0], 2), dtype=np.float32)

    last_trade_index = 0
    total_trades = len(array2)

    for i in range(len(main_array) - 1):
        tick = main_array[i]
        next_tick = main_array[i + 1]

        last_trade = array2[last_trade_index]
        if tick <= last_trade <= next_tick:
            new_array[i] = [1, vol[last_trade_index]]
            last_trade_index += 1

        if last_trade < tick:
            print("Skippped tick", last_trade_index, last_trade, tick)
            new_array[i - 1] = [1, vol[last_trade_index]]
            last_trade_index += 1

        # if last_trade_index > total_trades:
        #     break

    # print(last_trade_index)
    # print(array2[last_trade_index])
    return new_array


class CreateSignalArray:
    # If there entries and exits happening on the same timestamp, we need to aggregate them
    def get_aggregated_signals(sefl, df, column_name):
        entries = pd.DataFrame({"date": df[column_name], "volume": df["volume"]})
        entries.date = pd.to_datetime(entries.date, unit="s")

        merged_df = entries.groupby("date").agg({"volume": "sum"}).reset_index()
        return merged_df

    def create_entries_array(self, dates, array, column_name):
        ent = array["date"].values.astype(np.int64) // 10**6
        vol = array["volume"].values.astype(np.float32)

        return find_first_occurrence(dates.values, ent, vol)

    def create_signal_array(self, dates, array, column_name):
        agg = self.get_aggregated_signals(array, column_name)
        signals = self.create_entries_array(dates, agg, column_name)
        df = pd.DataFrame(
            {"date": dates, "signal": signals[:, 0], "volume": signals[:, 1]}
        )
        self.df = df
        return df

    def print_df(self, df):
        print(df[df["signal"] == 1])


create = CreateSignalArray()


long_entries = create.create_signal_array(data["Date"], long_signals, "long_entry")
long_exits = create.create_signal_array(data["Date"], long_signals, "long_entry")
#
short_entries = create.create_signal_array(data["Date"], short_signals, "short_entry")
short_exits = create.create_signal_array(data["Date"], short_signals, "short_exit")
#

# create.print_df(long_entries)
# create.print_df(long_exits)
# #
# create.print_df(short_entries)
# create.print_df(short_exits)


####====================================================================================================================####

####====================================================================================================================####


bt.set_bid_ask_data(
    data["Date"].values, data["Bid"].values, data["Ask"].values, data["Volume"].values
)

VOLUME_MULTIPLIER = 10000

entries = long_entries.signal.values
volume_entry = long_entries.volume.values * VOLUME_MULTIPLIER


exits = long_exits.signal.values
volume_exit = long_exits.volume.values * VOLUME_MULTIPLIER

data
import time

start = time.time()
bt.backtest_bid_ask(entries, exits, volume_entry, volume_exit)
end = time.time()
print(end - start)

df = pd.DataFrame(bt.equity)
print(df)
# df.plot()
# plt.show()

# |%%--%%| <UBHzhf2SfU|QFk3nIW721>

VOLUME_MULTIPLIER = 10000

entries = short_entries.signal.values
volume_entry = short_entries.volume.values * VOLUME_MULTIPLIER


exits = short_entries.signal.values
volume_exit = short_entries.volume.values * VOLUME_MULTIPLIER

bt.backtest_bid_ask(entries, exits, volume_entry, volume_exit)

df = pd.DataFrame(bt.equity)
print(df)
df.plot()
plt.show()
# |%%--%%| <QFk3nIW721|U8YDjUSDd1>

trades = [10.5, 12.2, 11.8, 13.5, 12.9]
volumes = [100, 150, 200, 120, 180]

# Calculate the weighted average position price
total_volume = sum(volumes)
weighted_sum = sum(trade * volume for trade, volume in zip(trades, volumes))
average_position_price = weighted_sum / total_volume

print(average_position_price)

new_trade_price = 11.3
new_trade_volume = 150
# Calculate the new totals
new_total_volume = total_volume + new_trade_volume
new_weighted_sum = weighted_sum + (new_trade_price * new_trade_volume)

# Calculate the new average price
average_price = new_weighted_sum / new_total_volume
print(average_price)
