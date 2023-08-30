import numpy as np
from numba import njit
from ..lib.get_series_values import get_series_values



@njit(parallel=True, cache=True)
def cross_below_nb(arr1, arr2):
    cross_above_mask = np.full(len(arr1), False)

    for i in range(len(arr1)):  # Changed loop range
        if arr1[i] < arr2[i] and arr1[i - 1] > arr2[i - 1]:
            cross_above_mask[i] = True
        else:
            cross_above_mask[i] = False
    return cross_above_mask

def cross_below(arr1, arr2):
    val1 = get_series_values(arr1)
    val2 = get_series_values(arr2)
    return cross_below_nb(val1, val2)
