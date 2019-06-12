import pytest

from ...ds.stack import Stack


class TestStack(object):

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([1, 2], "2->1"),
        pytest.param([1, 2, 3, 4, 5], "5->4->3->2->1"),
    ])
    def test_push(self, datas, expected):
        s = Stack()
        s.bulk_push(datas)

        assert repr(s) == expected

    @pytest.mark.parametrize('datas, pop_num, expected', [
        pytest.param([1], 0, "1"),
        pytest.param([1], 1, ""),
        pytest.param([1, 2], 1, "1"),
        pytest.param([1, 2], 2, ""),
        pytest.param([1, 2, 3, 4, 5], 2, "3->2->1"),
        pytest.param([1, 2, 3, 4, 5], 5, ""),
    ])
    def test_pop(self, datas, pop_num, expected):
        s = Stack()
        s.bulk_push(datas)

        for _ in range(pop_num):
            s.pop()

        assert repr(s) == expected
