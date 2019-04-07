import numpy as np
import math

from .exc import ArgError


class ArrayUtils(object):

    @staticmethod
    def rotate(a, *, dtype=int):
        """  Rotate for M*N array, this is equivalent to numpy.rot90(a, 3)
        :array: M*N numpy array
        :return: rotated numpy array

        Complexity:
        Time  : O(mn)
        Space : O(mn)
        """

        if not a.all():
            raise ArgError()

        row_num, col_num = a.shape[::-1]

        rotated_array = np.empty(shape=[row_num, col_num], dtype=dtype)

        for index, v in np.ndenumerate(a):
            r, c = index
            rotated_array[c, col_num-1-r] = v

        return rotated_array

    @staticmethod
    def rotate_in_place(a):
        """  Rotate for N*N array, the result is equivalent to numpy.rot90(a, 3)
        :array: N*N numpy array
        :return: rotated numpy array

        Complexity:
        Time  : O(nn)
        Space : O(1)
        """

        # 4-way edge swap
        if not a.all():
            raise ArgError()

        row_num, col_num = a.shape

        if row_num != col_num:
            raise ArgError("only support N*N array")

        dim = row_num

        layers = math.ceil(dim/2)

        for layer in range(layers):
            start = layer
            end = dim - 1 - layer

            for offset in range(end - start):
                tmp = a[start, start + offset]
                a[start, start + offset] = a[end - offset, start]
                a[end - offset, start] = a[end, end-offset]
                a[end, end-offset] = a[start + offset, end]
                a[start + offset, end] = tmp

        return a
