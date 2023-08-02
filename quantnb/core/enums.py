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


# ["Index", "Direction", "EntryTime", "EntryPrice", "ExitTime", "ExitPrice", "Volume", "TP", "SL", "PNL", "Commission", "Active"]
class Trade(IntEnum):
    Index = 0
    Direction = 1
    EntryTime = 2
    EntryPrice = 3
    ExitTime = 4
    ExitPrice = 5
    Volume = 6
    TP = 7
    SL = 8
    TIME_SL = 9
    PNL = 10
    Commission = 11
    Active = 12
    Extra = 13
