from quantnb.indicators import talib_SMA as SMA
from quantnb.indicators.random_data import random_data
from quantnb.lib import pd, np
from quantnb.lib.data_to_csv import save_data, create_scatter_df
import talib

data = random_data(seed=42)[0]


rsi = talib.RSI(data.close, timeperiod=14)
sma = SMA(data.close, 14)

"""
Create the entry and exit signal
"""
entries = rsi < 30
exits = rsi > 70


# Apply the function to create the new column
rsi_scatter_high = create_scatter_df(data['high'] * 1.01, exits)
rsi_scatter_low = create_scatter_df(data['low'] * 0.99, entries)

#|%%--%%| <9dYaZhxcfT|DtKrqPsRfU>


"""
Create the dataframes needed for the UI
"""
df = pd.DataFrame({
    'date': data.index,
    'open': data.open,
    'high': data.high,
    'low': data.low,
    'close': data.close,
    'entries': entries,
    'exits': exits,
})

indicators_data = pd.DataFrame({
    'sma': sma,
    'rsi': rsi,
    'rsi_scatter_high': rsi_scatter_high,
    'rsi_scatter_low': rsi_scatter_low,
})

"""
Create the configuration that tells the UI which indicators to draw
"""
indicators = [{
    "name": "Donchian",
    "type": "line",
    "panel": 0,
    "dataIndex": 0
  }, {
    "name": "RSI",
    "type": "line",
    "panel": 1,
    "dataIndex": 1
  }, {
    "name": "RSI Scatter High",
    "type": "scatter",
    "panel": 0,
    "dataIndex": 2
  }, {
    "name": "RSI Scatter Low",
    "type": "scatter",
    "panel": 0,
    "dataIndex": 3
  }
]

#|%%--%%| <DtKrqPsRfU|vlAMStIg3O>


"""
Save the data and config to the location of the UI
"""
UI_LOCATION = "/home/alpha/workspace/cultivating-alpha/candles-ui/public"

save_data(UI_LOCATION, df, indicators, indicators_data)
