import json
import numpy as np
import pandas as pd
from numba import njit
from quantbt.core.enums import Trade


def create_equity_on_close(ohlc, trades, equity):
    equity_on_close = np.full(len(equity), 0)
    equity_on_close[0] = equity[0]
    for trade in trades:
        index = ohlc.index.get_loc(trade[Trade.ExitTime]) + 1
        if index == len(equity):
            index -= 1
        equity_on_close[index] = equity[index]

    for i in range(len(equity)):
        if equity_on_close[i] == 0:
            equity_on_close[i] = equity_on_close[i - 1]
    return equity_on_close


def create_trade_arrows(ohlc, trades):
    data = []
    for trade in trades:
        color = "teal" if trade[Trade.PNL] > 0 else "red"
        data.append(
            [
                {
                    "name": np.round(trade[Trade.PNL], 2),
                    "coord": [
                        ohlc.index.get_loc(trade[Trade.EntryTime]),
                        trade[Trade.EntryPrice],
                    ],
                    "lineStyle": {"color": color},
                },
                {
                    "coord": [
                        ohlc.index.get_loc(trade[Trade.ExitTime]),
                        trade[Trade.ExitPrice],
                    ]
                },
            ]
        )

    return data


@njit(cache=True, parallel=True)
def format_array_to_tick(array, tick_size):
    for i in range(len(array)):
        array[i] = round(array[i] / tick_size) * tick_size
    return array


def save_data(UI_LOCATION, df, indicators, indicators_data, trades):
    trade_arrows = create_trade_arrows(df, trades)

    def save_to_csv(df, path):
        array_of_arrays = df.values.tolist()
        # Write the list of lists to a CSV file
        with open(path, "w") as csv_file:
            for row in array_of_arrays:
                csv_file.write(",".join(map(str, row)) + "\n")

    save_to_csv(df, f"{UI_LOCATION}/ohlc.csv")
    save_to_csv(indicators_data, f"{UI_LOCATION}/indicators.csv")

    with open(f"{UI_LOCATION}/indicators.json", "w") as f:
        json.dump(indicators, f)

    with open(f"{UI_LOCATION}/trade_arrows.json", "w") as f:
        json.dump(trade_arrows, f)


def create_scatter_df(data, mask):
    new_df = np.empty(len(data))
    for i in range(len(data)):
        if mask[i]:
            new_df[i] = data[i]
        else:
            new_df[i] = np.nan
    return new_df


def create_trades_array(trades, data):
    entries = pd.DataFrame({"date": trades["EntryTime"], "price": trades["EntryPrice"]})
    exits = pd.DataFrame({"date": trades["ExitTime"], "price": trades["ExitPrice"]})
    exits = exits[exits["price"] > 0]

    @njit
    def combine_trades(date, trade_date, trade_price):
        _trades = np.full(len(date), np.nan)
        last_trade = 0
        for i in range(len(date)):
            if date[i] == trade_date[last_trade]:
                _trades[i] = trade_price[last_trade]
                last_trade += 1
        return _trades

    entry_trades = combine_trades(
        data.index.values, entries["date"].values, entries["price"].values
    )
    exit_trades = combine_trades(
        data.index.values, exits["date"].values, exits["price"].values
    )
    return entry_trades, exit_trades


def create_fixed_lines(values):
    data = []
    for index, val in enumerate(values):
        data.append(
            {
                "symbol": "none",
                "name": val["name"] if "name" in val else f"Fixed line {index}",
                "yAxis": val["value"],
                "lineStyle": {
                    "color": val["color"] if "color" in val else "#000000",
                },
            }
        )
    return {"data": data}
