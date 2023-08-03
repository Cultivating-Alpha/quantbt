from quantnb.core.trade_module import TradeModule
from quantnb.core.data_module import DataModule
from quantnb.core.trade_create_new_trade import create_new_trade
from quantnb.indicators.random_data import random_data
from quantnb.lib.output_trades import output_trades
from quantnb.core.enums import (
    DataType,
    CommissionType,
    OrderDirection,
    Trade,
    OrderType,
)
import numpy as np


date, open, high, low, close, ohlc = random_data(2)

COMMISSION = 4
MAX_ACTIVE_TRADES = 3
SLIPPAGE = 0.2
INITIAL_CAPITAL = float(10000.0)


class TestCalculatePrice:
    trade_module = TradeModule(
        data_type=DataType.BID_ASK,
        multiplier=2,
        commission=COMMISSION,
        max_active_trades=MAX_ACTIVE_TRADES,
    )
    data_module = DataModule(
        close=close,
        data_type=DataType.OHLC,
        bid=low,
        ask=high,
        date=date,
        slippage=SLIPPAGE,
        initial_capital=INITIAL_CAPITAL,
    )

    def add_trade(self, direction=OrderDirection.LONG, index=300):
        entry_price = self.data_module.get_entry_price(index, direction)  # index
        self.trade_module.add_trade(
            index,  # index
            direction.value,  # direction
            OrderType.MARKET,  # order_type
            date[index],  # entry_time
            entry_price,  # entry_price
            1,  # volume
        )

    def test_add_trade(self, direction=OrderDirection.LONG):
        index = 300
        entry_price = self.data_module.get_entry_price(index, direction)  # index
        self.add_trade(direction, index)
        assert self.trade_module.last_trade_index == 1
        last_trade = self.trade_module.trades[self.trade_module.last_trade_index - 1]

        assert last_trade[Trade.Index] == index
        assert last_trade[Trade.Direction] == direction.value
        assert last_trade[Trade.EntryTime] == date[index]
        assert last_trade[Trade.EntryPrice] == entry_price
        assert last_trade[Trade.Volume] == 1
        assert last_trade[Trade.ExitTime] == -1
        assert last_trade[Trade.ExitPrice] == -1
        assert last_trade[Trade.TP] == 0
        assert last_trade[Trade.SL] == 0
        assert last_trade[Trade.TIME_SL] == np.inf
        assert last_trade[Trade.PNL] == COMMISSION * -1
        assert last_trade[Trade.Commission] == COMMISSION
        assert last_trade[Trade.Active] == True
        assert last_trade[Trade.Extra] == -1

    def test_add_multiple_trades(self, direction=OrderDirection.LONG):
        for index in range(300, 325):
            self.data_module.update_equity(
                index, self.trade_module.closed_pnl, self.trade_module.floating_pnl
            )
            if index == 312:
                self.add_trade(direction, index)
            elif index == 324:
                self.add_trade(direction, index)
            self.trade_module.update_trades_pnl(self.data_module.close[index], 0, 0)

        index = 325
        # UPDATE PNL
        self.trade_module.update_trades_pnl(self.data_module.close[index], 0, 0)

        # CURRENT
        _sum = 0
        for trade in self.trade_module.active_trades:
            _sum += trade[Trade.PNL]
        # print(_sum)

        current = self.data_module.close[index]
        initial_trade = self.data_module.close[300]
        first_trade_entry = self.data_module.close[312]
        second_trade_entry = self.data_module.close[324]
        pnl0 = (current - initial_trade - SLIPPAGE) - COMMISSION
        pnl1 = (current - first_trade_entry - SLIPPAGE) - COMMISSION
        pnl2 = (current - second_trade_entry - SLIPPAGE) - COMMISSION
        # print(pnl1)
        # print(pnl2)
        expected_pnl = pnl0 + pnl1 + pnl2
        # print(expected_pnl)

        trades = output_trades(self.trade_module)
        # print(trades)
        assert np.round(expected_pnl, 6) == np.round(_sum, 6)

    def test_equity(self):
        expected = INITIAL_CAPITAL + self.trade_module.floating_pnl
        assert self.data_module.equity[324] == expected


# TestCalculatePrice().test_add_multiple_trades()
