import numpy as np


def cross_above_nb(arr1, arr2):
    cross_above_mask = np.logical_and(arr1[:-1] < arr2[:-1], arr1[1:] > arr2[1:])
    cross_above_mask = np.insert(cross_above_mask, 0, False)
    return cross_above_mask


def cross_above(arr1, arr2):
    return cross_above_nb(arr1.values, arr2.values)
