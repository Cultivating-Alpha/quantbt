from numba import njit


@njit
def update_trades_pnl(index, active_trades, commission):
    for trade in active_trades:
        direction = trade[1]
        trade_price = trade[3]

        commission = 0
        trade_volume = trade[6]

        if direction == 1:  # LONG
            price = self.ask[index]
            pnl = (price - trade_price) * trade_volume - commission
        else:
            price = self.bid[index]
            pnl = (trade_price - price) * trade_volume - commission

        return pnl
        self.trades[int(trade[0])][7] = pnl
