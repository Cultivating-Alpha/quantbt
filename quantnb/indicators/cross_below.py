import numpy as np
from numba import njit
from ..lib.get_series_values import get_series_values


def cross_below_nb(arr1, arr2):
    cross_below_mask = np.logical_and(arr1[:-1] > arr2[:-1], arr1[1:] < arr2[1:])

    cross_below_mask = np.insert(cross_below_mask, 0, False)
    return cross_below_mask

def cross_below(arr1, arr2):
    val1 = get_series_values(arr1)
    val2 = get_series_values(arr2)
    return cross_below_nb(val1, val2)
