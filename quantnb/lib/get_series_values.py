import numpy as np

def is_numpy_array(obj):
    return isinstance(obj, np.ndarray)

def get_series_values(obj):
    return obj.values if not is_numpy_array(obj) else obj
