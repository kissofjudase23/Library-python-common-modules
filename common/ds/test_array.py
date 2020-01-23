import pytest
import numpy as np

from common.ds.array import ArrayUtils


class TestArrayUtils(object):

    @pytest.mark.parametrize('a, expected', [
        pytest.param(np.array([[1, 2, 3]]),
                     np.array([[1],
                               [2],
                               [3]])),
        pytest.param(np.array([[1, 2, 3],
                               [4, 5, 6]]),
                     np.array([[4, 1],
                               [5, 2],
                               [6, 3]])),
        pytest.param(np.array([[1, 2, 3],
                               [4, 5, 6],
                               [7, 8, 9]]),
                     np.array([[7, 4, 1],
                               [8, 5, 2],
                               [9, 6, 3]])),
    ])
    def test_rotate(self, a, expected):
        actual = ArrayUtils.rotate(a)
        assert np.array_equal(actual, expected) is True

    @pytest.mark.parametrize('a, expected', [
        pytest.param(np.array([[1, 2, 3],
                               [4, 5, 6],
                               [7, 8, 9]]),
                     np.array([[7, 4, 1],
                               [8, 5, 2],
                               [9, 6, 3]])),

        pytest.param(np.array([[1, 2, 3, 4],
                               [5, 6, 7, 8],
                               [9, 10, 11, 12],
                               [13, 14, 15, 16]]),
                     np.array([[13, 9, 5, 1],
                               [14, 10, 6, 2],
                               [15, 11, 7, 3],
                               [16, 12, 8, 4]])),
    ])
    def test_roate_in_place(self, a, expected):
        actual = ArrayUtils.rotate_in_place(a)
        assert np.array_equal(actual, expected) is True
