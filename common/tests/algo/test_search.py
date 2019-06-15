import pytest

from ...algo import search


@pytest.fixture(scope='class')
def sorted_list():
    yield [1, 2, 3, 4, 5]


class TestBinarySearch(object):

    @pytest.mark.parametrize('target, expected', [
        pytest.param(1, 0),
        pytest.param(2, 1),
        pytest.param(3, 2),
        pytest.param(4, 3),
        pytest.param(5, 4),
        pytest.param(100, -1),
        pytest.param(-100, -1),
    ])
    def test_fast(self, sorted_list, target, expected):
        assert expected == search.binary_search(sorted_list, target)
        assert expected == search.binary_search_recursive(sorted_list, target)

    @pytest.mark.parametrize('sorted_list, target, expected', [
        pytest.param([0], 0, 0),
        pytest.param([0, 1], 0, 0),
        pytest.param([0, 1], 1, 1),
    ])
    def test_toft(self, sorted_list, target, expected):
        assert expected == search.binary_search(sorted_list, target)
        assert expected == search.binary_search_recursive(sorted_list, target)
