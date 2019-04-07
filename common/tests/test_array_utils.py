import pytest
import numpy as np

from ..array_utils import ArrayUtils


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
    def test_is_unique_char(self, a, expected):
        actual = ArrayUtils.rotate(a)
        assert np.array_equal(actual, expected) is True
