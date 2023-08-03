import numpy as np
from typing import List
from quantnb.core.enums import Trade, DataType
from numba.experimental import jitclass
from quantnb.core.specs_nb import trade_specs

TRADE_ITEMS_COUNT = Trade.__len__()


# pyright: reportGeneralTypeIssues=false
@jitclass(trade_specs)
class TradeModule:
    def __init__(
        self,
        close: List[float],
        multiplier=1,
        data_type=DataType.OHLC.value,
    ) -> None:
        length: int = len(close)
        self.active_trades: List[float] = np.zeros(
            (0, TRADE_ITEMS_COUNT), dtype=np.float64
        )
        self.closed_trades: List[float] = np.zeros(
            (length, TRADE_ITEMS_COUNT), dtype=np.float64
        )
        self.last_active_trade_index: int = 0
        self.last_closed_trade_index: int = 0
        self.multiplier: int = multiplier
        self.data_type: int = data_type

    def add_trade(self, *args):
        # if self.debug:
        #     print("Adding new trade")
        if len(self.active_trades) >= 100:
            return
        self.last_active_trade_index += 1
        self.active_trades = create_new_trade(
            self.active_trades, self.last_active_trade_index, *args
        )
