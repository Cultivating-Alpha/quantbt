import pandas_ta as ta
from quantnb.lib import find_files, pd
import talib
import time
import numpy as np
from prettytable import PrettyTable
import timeit
import numpy as np
from numba import guvectorize, njit, prange


datas = {}
assets = find_files("./data", "binance")

for asset in assets:
    datas[asset.split("-")[1]] = pd.read_parquet(asset)


keys = list(datas.keys())

data = datas[keys[0]]
print(data)


# |%%--%%| <67lVNdHohg|ud493qJ1DW>


# correlation_matrix = ta_sma.corr(talib_sma)
# print(correlation_matrix)
def get_time(library, function, data=None, **args):
    start = time.time()

    def func():
        return getattr(library, function)(data, **args)

    execution_time = timeit.timeit(func, number=100)
    average_time = execution_time / 100
    return np.round(average_time, 8)


t = PrettyTable(["Method", "Pandas_TA(s)", "Talib(s)", "Improvement"])

# ================================================================================================ #
#                                               SMA                                                #
# ================================================================================================ #
pandas_time = get_time(ta, "sma", data=data["close"], length=20)
talib_time = get_time(talib, "SMA", data=data["close"], timeperiod=20)
improvement = f"{np.round((pandas_time - talib_time) / pandas_time * 100, 2)}%"
t.add_row(["SMA", pandas_time, talib_time, improvement])

# ================================================================================================ #
#                                               EMA                                                #
# ================================================================================================ #
pandas_time = get_time(ta, "ema", data=data["close"], length=20)
talib_time = get_time(talib, "EMA", data=data["close"], timeperiod=20)
improvement = f"{np.round((pandas_time - talib_time) / pandas_time * 100, 2)}%"
t.add_row(["EMA", pandas_time, talib_time, improvement])

# ================================================================================================ #
#                                               ATR                                                #
# ================================================================================================ #
pandas_time = get_time(
    ta, "atr", data=data["high"], low=data["low"], close=data["close"], length=14
)
talib_time = get_time(
    talib,
    "ATR",
    data=data["high"],
    low=data["low"],
    close=data["close"],
    timeperiod=14,
)
improvement = f"{np.round((pandas_time - talib_time) / pandas_time * 100, 2)}%"
t.add_row(["ATR", pandas_time, talib_time, improvement])


# ================================================================================================ #
#                                       Bollinger Bands                                            #
# ================================================================================================ #
pandas_time = get_time(ta, "bbands", data=data["close"], length=20)
talib_time = get_time(talib, "BBANDS", data=data["close"], timeperiod=20)
improvement = f"{np.round((pandas_time - talib_time) / pandas_time * 100, 2)}%"
t.add_row(["Bollinger Bands", pandas_time, talib_time, improvement])


# ================================================================================================ #
#                                         Print OUTPUT                                             #
# ================================================================================================ #
print(t)
# |%%--%%| <ud493qJ1DW|LVqfDb8aGN>


@guvectorize(["void(float64[:], intp[:], float64[:])"], "(n),()->(n)")
def move_mean(a, window_arr, out):
    window_width = window_arr[0]
    asum = 0.0
    count = 0
    for i in range(window_width):
        asum += a[i]
        count += 1
        out[i] = asum / count
    for i in range(window_width, len(a)):
        asum += a[i] - a[i - window_width]
        out[i] = asum / count


@njit("void(double[:], intp[:], float64[:])", nogil=True, fastmath=True, parallel=True)
def n_move_mean(a, window_arr, out):
    window_width = window_arr[0]
    asum = 0.0
    count = 0
    for i in range(window_width):
        asum += a[i]
        count += 1
        out[i] = asum / count
    # for i in range(window_width, len(a)):
    #     asum += a[i] - a[i - window_width]
    #     out[i] = asum / count
    for i in prange(window_width, len(a)):
        asum += a[i] - a[i - window_width]
        out[i] = asum / count


arr = data.open.values


def n_numba():
    return n_move_mean(arr, 20)


n_move_mean(arr, 20)
n_move_mean.parallel_diagnostics(level=4)

execution_time = timeit.timeit(n_numba, number=100)
average_time = execution_time / 100
print(f"Average execution time: {average_time:.8f} seconds")


# |%%--%%| <LVqfDb8aGN|fZKJXfm52H>


def _talib():
    return talib.SMA(arr, 200)


def g_numba():
    return move_mean(arr, 200)


def n_numba():
    return n_move_mean(arr, 200)


# Measure the execution time of the function
execution_time = timeit.timeit(_talib, number=100)
average_time = execution_time / 100
print(f"Average execution time: {average_time:.6f} seconds")

execution_time = timeit.timeit(g_numba, number=100)
average_time = execution_time / 100
print(f"Average execution time: {average_time:.6f} seconds")

execution_time = timeit.timeit(n_numba, number=100)
average_time = execution_time / 100
print(f"Average execution time: {average_time:.6f} seconds")
# |%%--%%| <fZKJXfm52H|NxiQGyvb4j>

import math
import threading
from timeit import repeat

import numpy as np
from numba import jit

nthreads = 4
size = 10**6


def func_np(a, b):
    """
    Control function using Numpy.
    """
    return np.exp(2.1 * a + 3.2 * b)


@jit("void(double[:], double[:], double[:])", nopython=True, nogil=True)
def inner_func_nb(result, a, b):
    """
    Function under test.
    """
    for i in range(len(result)):
        result[i] = math.exp(2.1 * a[i] + 3.2 * b[i])


def timefunc(correct, s, func, *args, **kwargs):
    """
    Benchmark *func* and print out its runtime.
    """
    print(s.ljust(20), end=" ")
    # Make sure the function is compiled before the benchmark is
    # started
    res = func(*args, **kwargs)
    # if correct is not None:
    #     assert np.allclose(res, correct), (res, correct)
    # time it
    print(
        "{:>5.0f} ms".format(
            min(repeat(lambda: func(*args, **kwargs), number=5, repeat=2)) * 1000
        )
    )
    return res


def make_singlethread(inner_func):
    """
    Run the given function inside a single thread.
    """

    def func(*args):
        length = len(args[0])
        result = np.empty(length, dtype=np.float64)
        inner_func(result, *args)
        return result

    return func


def make_multithread(inner_func, numthreads):
    """
    Run the given function inside *numthreads* threads, splitting
    its arguments into equal-sized chunks.
    """

    def func_mt(*args):
        length = len(args[0])
        result = np.empty(length, dtype=np.float64)
        args = (result,) + args
        chunklen = (length + numthreads - 1) // numthreads
        # Create argument tuples for each input chunk
        chunks = [
            [arg[i * chunklen : (i + 1) * chunklen] for arg in [args[0]]]
            for i in range(numthreads)
        ]
        print(len(chunks))
        # # Spawn one thread per chunk
        # threads = [threading.Thread(target=inner_func, args=chunk) for chunk in chunks]
        # for thread in threads:
        #     thread.start()
        # for thread in threads:
        #     thread.join()
        # return result

    return func_mt


@jit("void(double[:], double[:], intp)", nopython=True, nogil=True)
def mean_nb(result, a, b):
    """
    Function under test.
    """
    a = 4
    # for i in range(len(result)):
    #     result[i] = math.exp(2.1 * a[i] + 3.2 * b[i])


# func_nb = make_singlethread(inner_func_nb)
# func_nb_mt = make_multithread(inner_func_nb, nthreads)
func_nb = make_singlethread(mean_nb)
func_nb_mt = make_multithread(mean_nb, nthreads)

a = np.random.rand(size)
# b = np.random.rand(size)
# a = arr
b = 200
result = np.empty(len(a), dtype=np.float64)
mean_nb(result, a, b)

correct = timefunc(None, "numpy (1 thread)", func_np, a, b)
timefunc(correct, "numba (1 thread)", func_nb, a, b)
timefunc(correct, "numba (%d threads)" % nthreads, func_nb_mt, a, b)
# |%%--%%| <NxiQGyvb4j|0G5ZGAXBGo>


@njit(parallel=True)
def test(x):
    n = x.shape[0]
    a = np.sin(x)
    b = np.cos(a * a)
    acc = 0
    for i in prange(n - 2):
        for j in prange(n - 1):
            acc += b[i] + b[j + 1]
    return acc


test(np.arange(10))

test.parallel_diagnostics(level=4)
# |%%--%%| <0G5ZGAXBGo|WhM8iERzAr>
import timeit
import numpy as np
from numba import jit, guvectorize

# both functions take an (m x n) array as input, compute the row sum, and return the row sums in a (m x 1) array


@guvectorize(
    ["void(float64[:], float64[:])"], "(n) -> ()", target="parallel", nopython=True
)
def row_sum_gu(input, output):
    # output[0] = np.sum(input)
    m, n = input_array.shape
    for i in range(m):
        output[i] = np.sum(input_array[i, :])


@jit(nopython=True)
def row_sum_jit(input_array, output_array):
    m, n = input_array.shape
    for i in range(m):
        output_array[i] = np.sum(input_array[i, :])


rows = int(64)  # broadcasting (= supposed parallellization) dimension for guvectorize
columns = int(1e6)
input_array = np.ones((rows, columns))
output_array = np.zeros((rows))
output_array2 = np.zeros((rows))

print(input_array)

# the first run includes the compile time
row_sum_jit(input_array, output_array)
row_sum_gu(input_array, output_array2)

# run each function 100 times and record the time
print(
    "jit time:",
    timeit.timeit(
        "row_sum_jit(input_array, output_array)",
        "from __main__ import row_sum_jit, input_array, output_array",
        number=100,
    ),
)
print(
    "guvectorize time:",
    timeit.timeit(
        "row_sum_gu(input_array, output_array2)",
        "from __main__ import row_sum_gu, input_array, output_array2",
        number=100,
    ),
)
# |%%--%%| <WhM8iERzAr|PN9DH2TV0p>

from math import sqrt
from numba import njit, jit, guvectorize
import timeit
import numpy as np


@njit
def square_sum(arr):
    a = 0.0
    for i in range(arr.size):
        a = sqrt(a**2 + arr[i] ** 2)  # sqrt and square are cpu-intensive!
    return a


@guvectorize(
    ["void(float64[:], float64[:])"], "(n) -> ()", target="parallel", nopython=True
)
def row_sum_gu(input, output):
    output[0] = square_sum(input)


@jit(nopython=True)
def row_sum_jit(input_array, output_array):
    m, n = input_array.shape
    for i in range(m):
        output_array[i] = square_sum(input_array[i, :])
    return output_array

rows = int(64)
columns = int(1e6)

input_array = np.random.random((rows, columns))
output_array = np.zeros((rows))

# Warmup an check that they are equal 
np.testing.assert_equal(row_sum_jit(input_array, output_array), row_sum_gu(input_array, output_array2))
%timeit row_sum_jit(input_array, output_array.copy())  # 10 loops, best of 3: 130 ms per loop
%timeit row_sum_gu(input_array, output_array.copy())   # 10 loops, best of 3: 35.7 ms per loop
