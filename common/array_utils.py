import numpy as np

from .exc import ArgError


class ArrayUtils(object):

    @staticmethod
    def rotate(a, *, dtype=int):
        """  Rotate for M*N array
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
