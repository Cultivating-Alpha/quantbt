import pandas as pd
import numpy as np
from quantbt.core.enums import CommissionType, Trade, PositionCloseReason
from quantbt.lib.time_manip import time_manip


TRADE_ITEMS_COUNT = Trade.__len__()

all_names = [trade.name for trade in Trade]

enum_mapping = {member.value: member.name for member in PositionCloseReason}


def output_trades(bt, unit="ms", close_active_trades=False):
    data_module = bt.data_module

    trade_module = bt.trade_module
    trades = np.concatenate((trade_module.closed_trades, trade_module.active_trades))
    trades = pd.DataFrame(
        trades,
        columns=all_names,
    )

    trades["CloseReason"] = trades["CloseReason"].map(enum_mapping)
    trades["EntryTime"] = time_manip.convert_ms_to_datetime(trades["EntryTime"])
    trades["ExitTime"] = pd.to_datetime(trades["ExitTime"], unit=unit)
    # trades["TIME_SL"] = pd.to_datetime(trades["TIME_SL"], unit=unit)

    # Force close active trades to show on charts
    if close_active_trades:
        last_time = time_manip.convert_ms_to_datetime(data_module.date)[-1]
        last_price = data_module.close[-1]
        for index, row in trades.iterrows():
            if row["Active"] == 1:
                trades.at[index, "ExitTime"] = last_time
                trades.at[index, "ExitPrice"] = last_price

    closed_trades = trades[trades["Active"] == 0]
    active_trades = trades[trades["Active"] == 1]
    return trades, closed_trades, active_trades
