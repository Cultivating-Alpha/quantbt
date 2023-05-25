import numba as nb
import numpy as np

arr = np.random.rand(1000000)


@nb.jit(nopython=True)
def f(x):
    return x * 4 + 6 / 40

@nb.jit(nopython=True)
def g(func, arr):
    out = []
    for i in range(len(arr)):
        out.append(func(arr[i]))
    out = nb.typed.List.empty_list(nb.float64)
    return out

%timeit -n 10 -r 5 g(f, arr)
