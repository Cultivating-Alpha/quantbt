import pandas as pd


def convert_signal_to_marker(markers_mask, data, index):
    return pd.DataFrame({"entry": data[markers_mask]}, index=index)
