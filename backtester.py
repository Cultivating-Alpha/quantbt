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
):
    cash += entry_size * exit_price - transaction_cost
    orders[order_idx, :] = [i, -1, exit_price, entry_size, cash]
    order_idx += 1

    pnl = (exit_price - entry_price) * entry_size
    total_pnl += pnl

    trades[trade_idx, :] = [
        entry_time,
        i,
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
    prices,
    date,
    entry_signals,
    exit_signals,
    sl,
    size,
    initial_capital=100000,
    transaction_cost=None,
):
    orders = np.zeros((len(prices), 5))
    trades = np.zeros((len(prices), 6))
    cash = initial_capital
    stop_loss = 0
    total_pnl = 0.0
    final_value = cash
    in_position = False
    entry_time = 0
    order_idx = 0
    trade_idx = 0
    equity = np.zeros_like(prices)
    equity[0] = initial_capital
    entry_size = 0
    entry_price = 0

    for i in range(1, len(prices)):
        fee = calculate_fees(prices[i], size[i], transaction_cost)
        if entry_signals[i] == 1:
            if not in_position:
                # Use all available cash to buy
                size[i] = cash / prices[i]
                entry_size = size[i]
                stop_loss = sl[i]

                cash -= size[i] * prices[i] - fee
                orders[order_idx, :] = [i, 1, prices[i], size[i], cash]
                order_idx += 1
                in_position = True
                entry_time = date[i]
                entry_price = prices[i]
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
                    prices[i],
                    calculate_fees(stop_loss, entry_size, transaction_cost),
                    orders,
                    order_idx,
                    total_pnl,
                    trades,
                    trade_idx,
                    entry_time,
                )

                in_position = False
        else:
            if in_position:
                if prices[i] < stop_loss and prices[i - 1] > stop_loss:
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
                        stop_loss,
                        transaction_cost,
                        orders,
                        order_idx,
                        total_pnl,
                        trades,
                        trade_idx,
                        entry_time,
                    )

                    in_position = False

        equity[i] = cash + entry_size * prices[i]
        # if equity[i] == 0:
        #     print("==========")
        #     print(i)
        #     print(cash)
        #     print(positions[i])
        final_value = equity[i]
    return final_value, total_pnl, equity, orders[:order_idx, :], trades[:trade_idx, :]
