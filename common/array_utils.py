import numpy as np
import sys

from .exc import ArgError


class ArrayUtils(object):

    @staticmethod
    def rotate(a: np.array, *, dtype=int):
        """  Rotate for M*N array, this is equivalent to numpy.rot90(a, 3)
        :array: M*N numpy array
        :return: rotated numpy array

        Complexity:
        Time  : O(rc)
        Space : O(rc)
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
    def rotate_v2(a):
        """
        non-np version

        Complexity:
        Time  : O(rc)
        Space : O(rc)
        """
        row_num = len(a)
        col_num = len(a[0])

        rotated_array = [[None for _ in range(row_num)] for _ in range(col_num)]

        for r in range(row_num):
            for c in range(col_num):
                rotated_array[c][row_num-1-r] = a[r][c]

        return rotated_array

    @staticmethod
    def rotate_in_place_v2(a):
        """  Rotate for N*N array, the result is equivalent to numpy.rot90(a, 3)
        :array: non np array
        :return: rotated  array

        Complexity:
        Time  : O(rc)
        Space : O(rc)
        """
        row_num = len(a)
        col_num = len(a[0])

        if row_num != col_num:
            raise ArgError()

        dim = row_num

        layers = row_num // 2

        for layer in range(layers):
            start = layer
            end = dim - 1 - layer

            for offset in range(end-start):
                tmp = a[start][start+offset]
                a[start][start+offset] = a[end-offset][start]
                a[end-offset][start] = a[end][end-offset]
                a[end][end-offset] = a[start+offset][end]
                a[start+offset][end] = tmp

        return a

    @staticmethod
    def rotate_in_place(a: np.array):
        """  Rotate for N*N array, the result is equivalent to numpy.rot90(a, 3)
        :array: N*N numpy array
        :return: rotated numpy array

        Complexity:
        Time  : O(rc)
        Space : O(rc)
        """

        # 4-way edge swap
        if not a.all():
            raise ArgError()

        row_num, col_num = a.shape

        if row_num != col_num:
            raise ArgError("only support N*N array")

        dim = row_num

        layers = dim // 2

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


def main():
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    r = ArrayUtils.rotate_in_place_v2(a)
    print(r)


if __name__ == "__main__":
    sys.exit(main())
