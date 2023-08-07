import talib


def talib_EMA(data, period):
    return talib.MA(data, timeperiod=period, matype=talib.MA_Type.EMA)
