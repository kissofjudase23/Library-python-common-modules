import pytest

from ...algo import sort as SORT


class TestSorting(object):

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

        sorting_algorithms = [SORT.merge_sort,
                              SORT.merge_sort_recursive,
                              SORT.quick_sort,
                              SORT.quick_sort_recursive,
                              SORT.insertion_sort,
                              SORT.insertion_sort_recursive,
                              SORT.selection_sort,
                              SORT.selection_sort_recursive,
                              SORT.bubble_sort,
                              SORT.bubble_sort_resursive]

        for algo in sorting_algorithms:
            actual = unsorted_list.copy()
            algo(actual)
            assert expected == actual
