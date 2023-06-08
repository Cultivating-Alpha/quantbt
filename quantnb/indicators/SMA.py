import talib


def SMA(data, period):
    return talib.MA(data, timeperiod=period, matype=talib.MA_Type.SMA)
