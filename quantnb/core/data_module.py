import numpy as np
from typing import Optional, List
from quantnb.core.enums import DataType
from numba.experimental import jitclass
from quantnb.core.specs_nb import data_specs


# pyright: reportGeneralTypeIssues=false
@jitclass(data_specs)
class DataModule:
    def __init__(
        self,
        close: List[float],
        data_type=DataType.OHLC.value,
        date: Optional[List[int]] = None,
        open: Optional[List[float]] = None,
        high: Optional[List[float]] = None,
        low: Optional[List[float]] = None,
        volume: Optional[List[float]] = None,
        bid: Optional[List[float]] = None,
        ask: Optional[List[float]] = None,
        initial_capital=100000,
    ) -> None:
        if date is not None:
            self.date: List[int] = date

        # PRICE DATA
        if data_type == DataType.OHLC.value:
            if open is not None:
                self.open: List[float] = open
            if high is not None:
                self.high: List[float] = high
            if low is not None:
                self.low: List[float] = low
            if close is not None:
                self.close: List[float] = close
            print(close)
        else:
            if bid is not None:
                self.bid: List[float] = bid
            if ask is not None:
                self.ask: List[float] = ask
        self.data_type: int = data_type

        if volume is not None:
            self.volume: List[float] = volume

        # PORTFOLIO
        length = len(self.close)
        self.equity = np.empty(length, dtype=np.float32)

        self.initial_capital = initial_capital
        self.final_value = initial_capital
        self.total_pnl = 0.0
