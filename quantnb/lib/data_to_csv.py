import json
import numpy as np

def save_data(UI_LOCATION, df, indicators, indicators_data):
    def save_to_csv(df, path):
        array_of_arrays = df.values.tolist()
        # Write the list of lists to a CSV file
        with open(path, "w") as csv_file:
            for row in array_of_arrays:
                csv_file.write(",".join(map(str, row)) + "\n")

    save_to_csv(df, f"{UI_LOCATION}/ohlc.csv")
    save_to_csv(indicators_data, f"{UI_LOCATION}/indicators.csv")

    with open(f"{UI_LOCATION}/indicators.json", 'w') as f:
        json.dump(indicators, f)

def create_scatter_df(data, mask):
    new_df = np.empty(len(data))
    for i in range(len(data)):
        if mask[i]:
            new_df[i] = data[i]
        else:
            new_df[i] = np.nan
    return new_df

