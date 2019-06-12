import pytest

from ...ds.queue import Queue


class TestQueue(object):

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([1, 2], "1->2"),
        pytest.param([1, 2, 3, 4, 5], "1->2->3->4->5"),
    ])
    def test_add(self, datas, expected):
        q = Queue()
        q.bulk_add(datas)
        assert repr(q) == expected

    @pytest.mark.parametrize('datas, remove_num, expected', [
        pytest.param([1], 0, "1"),
        pytest.param([1], 1, ""),
        pytest.param([1, 2], 1, "2"),
        pytest.param([1, 2], 2, ""),
        pytest.param([1, 2, 3, 4, 5], 2, "3->4->5"),
        pytest.param([1, 2, 3, 4, 5], 5, ""),
    ])
    def test_pop(self, datas, remove_num, expected):
        q = Queue()
        q.bulk_add(datas)

        for _ in range(remove_num):
            q.remove()

        assert repr(q) == expected
