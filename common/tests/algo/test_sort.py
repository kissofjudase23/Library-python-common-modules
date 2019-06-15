import pytest

from ...algo import sort as SORT


class TestMergeSort(object):

    @pytest.mark.parametrize('unsorted_list', [
        pytest.param([1]),
        pytest.param([3, 2, 1]),
        pytest.param([5, 4, 3, 2, 1]),
        pytest.param([6, 5, 4, 3, 2, 1]),
        pytest.param([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]),
    ])
    def test_fast(self, unsorted_list):
        expected = unsorted_list.copy()
        expected.sort()

        actual1 = unsorted_list.copy()
        actual2 = unsorted_list.copy()

        SORT.merge_sort(actual1)
        SORT.merge_sort_recursive(actual2)

        assert expected == actual1
        assert expected == actual2