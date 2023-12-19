import re
import pandas as pd
from quantbt.lib import find_files


def find_optimisations(strategy_name, directory="./optimisation"):
    def extract_time(file_name):
        # Use regular expression to extract the time information
        match = re.search(r"-(\d+)(min|h)\.parquet$", file_name)
        if match:
            time_value, time_unit = match.groups()
            return int(time_value) if time_unit == "min" else int(time_value) * 60
        return float("inf")  # Return a large value for files with no time information

    # Sort the file list based on the extracted time
    files = sorted(find_files(directory, strategy_name), key=extract_time)
    opti = {}
    for file in files:
        tf = file.split("-")[1].split(".")[0]
        df = pd.read_parquet(file)
        opti[tf] = df
    return opti
