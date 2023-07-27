import pandas as pd
import matplotlib.pyplot as plt


class TimeManip:
    def __init__(self):
        pass

    # ================================================================================= #
    #                        Time Manipulation Methods                                  #
    # ================================================================================= #
    def convert_ms_to_datetime(self, df):
        return pd.to_datetime(df, unit="ms")

    def convert_s_to_datetime(self, df):
        return pd.to_datetime(df, unit="s")

    def convert_datetime_to_s(self, df):
        return pd.to_datetime(df).astype(int) // 10**9

    def convert_datetime_to_ms(self, df):
        return pd.to_datetime(df).astype(int) // 10**6

    def convert_duration_to_timestamp(self, df, unit="ms"):
        return pd.to_timedelta(df, unit=unit)


time_manip = TimeManip()
