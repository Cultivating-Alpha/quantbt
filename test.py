from numba import njit


@njit(cache=True)
def test(*args):
    counter = args[0]
    print("==========")
    print(counter)
    counter += 1
    print(counter)
    print("==========")
    return counter


counter = 4
counter = test(counter)


# |%%--%%| <UQnWsyn5oW|D3Yzavycmd>


# counter = 0
# print(id(counter))
# counter = test(counter)
# print(counter)
# print(id(counter))


class Main:
    def __init__(self):
        self.counter = 0

    def add(self):
        print(id(self.counter))
        test(counter=self.counter)
        print(self.counter)


# Main().add()


@njit(cache=True)
def second():
    counter = 0
    test(counter)
    print(counter)


second()


# |%%--%%| <D3Yzavycmd|CSSKodOnc4>

import numba
import numpy as np


@numba.jit(nopython=True)
def func(*arrays):
    print(arrays)
    # return np.vstack(arrays)


# print("signatures before call", func.nopython_signatures)

arr1 = np.array([1, 2])
arr2 = np.array([3, 4])
arr3 = func(arr1, arr2)
print(arr3)

# print("signatures after call", func.nopython_signatures)
# |%%--%%| <CSSKodOnc4|MEXIQeeRW5>

import numba as nb
import numpy as np
from numba.core import types, cgutils

arr = np.arange(5).astype(np.double)  # create arbitrary numpy array
print(arr)


@nb.extending.intrinsic
def address_as_void_pointer(typingctx, src):
    """returns a void pointer from a given memory address"""

    sig = types.voidptr(src)

    def codegen(cgctx, builder, sig, args):
        return builder.inttoptr(args[0], cgutils.voidptr_t)

    return sig, codegen


addr = arr.ctypes.data


@nb.njit
def modify_data():
    """a function taking the memory address of an array to modify it"""
    data = nb.carray(address_as_void_pointer(addr), arr.shape, dtype=arr.dtype)
    data += 2


modify_data()
print(arr)

# Reference:
# https://stackoverflow.com/questions/61509903/how-to-pass-array-pointer-to-numba-function
