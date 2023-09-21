import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


class TimeManip:
    def __init__(self):
        pass

    def format_index(self, df):
        row = df.index
        if "Date" in df.columns:
            row = df["date"].values
            df.drop("date", axis=1, inplace=True)
        elif "date" in df.columns:
            row = df["date"].values
            df.drop("date", axis=1, inplace=True)
        elif "time" in df.columns:
            row = df["time"].values
            df.drop("time", axis=1, inplace=True)

        # print(type(row[0]))
        if type(row[0]) == np.int64:
            if row[0] < 10_000_000_000:
                # print("Timestamp is likely in seconds")
                row = time_manip.convert_s_to_datetime(row)
            else:
                # print("Timestamp might be in milliseconds")
                row = time_manip.convert_ms_to_datetime(row)
        df["date"] = row
        return df

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

    # ================================================================================= #
    #                             Resample Methods                                      #
    # ================================================================================= #
    def hours_ago(self, df, hours=0):
        today = df.index.values[-1]
        hours_ago = today - pd.DateOffset(hours=hours)

        return df[df.index >= hours_ago]

    def months_ago(self, df, months=0):
        today = df.index.values[-1]
        months_ago = today - pd.DateOffset(months=months)

        return df[df.index >= months_ago]


time_manip = TimeManip()
