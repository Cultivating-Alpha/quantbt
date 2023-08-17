import numpy as np
from ..lib.get_series_values import get_series_values
from numba import njit


def cross_above_nb(arr1, arr2):
    cross_above_mask = np.logical_and(arr1[:-1] < arr2[:-1], arr1[1:] > arr2[1:])
    cross_above_mask = np.insert(cross_above_mask, 0, False)
    return cross_above_mask

def cross_above(arr1, arr2):
    val1 = get_series_values(arr1)
    val2 = get_series_values(arr2)
    return cross_above_nb(val1, val2)
