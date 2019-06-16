import pytest

from ...algo import sort as SORT


class TestMergeSort(object):

    @pytest.mark.parametrize('unsorted_list', [
        pytest.param([]),
        pytest.param([1]),
        pytest.param([1, 2]),
        pytest.param([i for i in range(3, 0, -1)]),
        pytest.param([i for i in range(4, 0, -1)]),
        pytest.param([i for i in range(9, 0, -1)]),
        pytest.param([i for i in range(10, 0, -1)]),
        pytest.param([i for i in range(15, 0, -2)]),
        pytest.param([i for i in range(16, 0, -2)]),
        pytest.param([2, 1]),
        pytest.param([i for i in range(0, 3)]),
        pytest.param([i for i in range(0, 4)]),
        pytest.param([i for i in range(0, 9)]),
        pytest.param([i for i in range(0, 10)]),
        pytest.param([i for i in range(0, 15, 2)]),
        pytest.param([i for i in range(0, 16, 2)]),
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
