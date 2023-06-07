import numpy as np
import numba as nb

# |%%--%%| <dD5zPebmm8|8x4LUPPUe3>


@nb.jit(nopython=True)
def close_position(
    i,
    cash,
    entry_price,
    entry_size,
    exit_price,
    transaction_cost,
    orders,
    order_idx,
    total_pnl,
    trades,
    trade_idx,
    entry_time,
    exit_time,
):
    cash = entry_size * exit_price - transaction_cost
    orders[order_idx, :] = [i, -1, exit_price, entry_size, cash]
    order_idx += 1

    pnl = (exit_price - entry_price) * entry_size - transaction_cost
    total_pnl += pnl

    trades[trade_idx, :] = [
        entry_time,
        exit_time,
        entry_price,
        exit_price,
        pnl,
        entry_size,
    ]
    trade_idx += 1
    entry_size = 0
    return cash, order_idx, orders, pnl, total_pnl, trade_idx, trades, entry_size


@nb.jit(nopython=True)
def calculate_fees(price, size, transaction_cost):
    return price * size * transaction_cost


@nb.jit(nopython=True)
def backtest(
    close,
    low,
    open,
    date,
    entry_signals,
    exit_signals,
    sl,
    size,
    initial_capital=100000,
    transaction_cost=None,
    mode=1,
    use_sl=True,
):
    orders = np.zeros((len(close), 5))
    trades = np.zeros((len(close), 6))
    cash = initial_capital
    stop_loss = 0
    total_pnl = 0.0
    final_value = cash
    in_position = False
    entry_time = 0
    order_idx = 0
    trade_idx = 0
    equity = np.zeros_like(close)
    equity[0] = initial_capital
    entry_size = 0
    entry_price = 0

    for i in range(1, len(close)):
        if entry_signals[i] == 1:
            # print(f'========== {i}')
            if not in_position:
                # Use all available cash to buy
                size[i] = cash / close[i]
                entry_size = size[i]
                stop_loss = sl[i]

                fee = calculate_fees(close[i], size[i], transaction_cost)
                cash -= size[i] * close[i] - fee
                orders[order_idx, :] = [i, 1, close[i], size[i], cash]
                order_idx += 1
                in_position = True
                entry_time = date[i]
                entry_price = close[i]
        elif exit_signals[i] == 1:
            if in_position:
                (
                    cash,
                    order_idx,
                    orders,
                    pnl,
                    total_pnl,
                    trade_idx,
                    trades,
                    entry_size,
                ) = close_position(
                    i,
                    cash,
                    entry_price,
                    entry_size,
                    close[i],
                    calculate_fees(close[i], entry_size, transaction_cost),
                    orders,
                    order_idx,
                    total_pnl,
                    trades,
                    trade_idx,
                    entry_time,
                    date[i],
                )

                in_position = False
        if use_sl:
            if mode == 1:
                # Mode 1
                if in_position:
                    # print(f'========== {i}')
                    # print(stop_loss)
                    # print(low[i])
                    if close[i] < stop_loss:
                        (
                            cash,
                            order_idx,
                            orders,
                            pnl,
                            total_pnl,
                            trade_idx,
                            trades,
                            entry_size,
                        ) = close_position(
                            i,
                            cash,
                            entry_price,
                            entry_size,
                            open[i + 1],  # exit price
                            calculate_fees(close[i], entry_size, transaction_cost),
                            orders,
                            order_idx,
                            total_pnl,
                            trades,
                            trade_idx,
                            entry_time,
                            date[i],
                        )

                        in_position = False
            elif mode == 2:
                # Mode 2
                if in_position:
                    if low[i] < stop_loss:
                        (
                            cash,
                            order_idx,
                            orders,
                            pnl,
                            total_pnl,
                            trade_idx,
                            trades,
                            entry_size,
                        ) = close_position(
                            i,
                            cash,
                            entry_price,
                            entry_size,
                            stop_loss,  # exit price
                            calculate_fees(close[i], entry_size, transaction_cost),
                            orders,
                            order_idx,
                            total_pnl,
                            trades,
                            trade_idx,
                            entry_time,
                            date[i],
                        )

                        in_position = False
            elif mode == 3:
                # Mode 3
                if (
                    not entry_signals[i] == 1
                    and not exit_signals[i] == 1
                    and in_position
                ):
                    if low[i] < stop_loss:
                        (
                            cash,
                            order_idx,
                            orders,
                            pnl,
                            total_pnl,
                            trade_idx,
                            trades,
                            entry_size,
                        ) = close_position(
                            i,
                            cash,
                            entry_price,
                            entry_size,
                            close[i],  # exit price
                            calculate_fees(close[i], entry_size, transaction_cost),
                            orders,
                            order_idx,
                            total_pnl,
                            trades,
                            trade_idx,
                            entry_time,
                            date[i],
                        )

                        in_position = False

            elif mode == 4:
                # Mode 3
                if (
                    not entry_signals[i] == 1
                    and not exit_signals[i] == 1
                    and in_position
                ):
                    if close[i] < stop_loss:
                        (
                            cash,
                            order_idx,
                            orders,
                            pnl,
                            total_pnl,
                            trade_idx,
                            trades,
                            entry_size,
                        ) = close_position(
                            i,
                            cash,
                            entry_price,
                            entry_size,
                            close[i],  # exit price
                            calculate_fees(close[i], entry_size, transaction_cost),
                            orders,
                            order_idx,
                            total_pnl,
                            trades,
                            trade_idx,
                            entry_time,
                            date[i],
                        )

                        in_position = False

        equity[i] = cash + entry_size * close[i] - fee
        # if equity[i] == 0:
        #     print("==========")
        #     print(i)
        #     print(cash)
        #     print(positions[i])
        final_value = equity[i]

        # print(total_pnl)
    return final_value, total_pnl, equity, orders[:order_idx, :], trades[:trade_idx, :]
