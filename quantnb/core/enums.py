from enum import IntEnum


class OrderDirection(IntEnum):
    SHORT = 0
    LONG = 1


class CommissionType(IntEnum):
    FIXED = 0
    PERCENTAGE = 1


class SlippageType(IntEnum):
    FIXED = 0
    PERCENTAGE = 1


class DataType(IntEnum):
    OHLC = 0
    BID_ASK = 1


class OrderType(IntEnum):
    MARKET = 0
    LIMIT = 1
    STOP_LIMIT = 2


class PositionCloseReason(IntEnum):
    SIGNAL = 0
    SL = 1
    TP = 2
    TIME_SL = 3


# ["Index", "Direction", "EntryTime", "EntryPrice", "ExitTime", "ExitPrice", "Volume", "TP", "SL", "PNL", "Commission", "Active"]
class Trade(IntEnum):
    IDX = 0
    Index = 1
    Direction = 2
    EntryTime = 3
    EntryPrice = 4
    ExitTime = 5
    ExitPrice = 6
    Volume = 7
    TP = 8
    SL = 9
    TIME_SL = 10
    PNL = 11
    Commission = 12
    Active = 13
    CloseReason = 14
    Extra = 15
