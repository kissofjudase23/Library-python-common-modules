import pytest

from ...data_struct.linkedlist import LinkedList


class TestLinkedList(object):

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([1, 2], "1->2"),
        pytest.param([1, 2, 3, 4, 5], "1->2->3->4->5"),
    ])
    def test_push_back(self, datas, expected):
        ll = LinkedList()
        ll.push_back_bulk(datas)
        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([2, 1], "1->2"),
        pytest.param([5, 4, 3, 2, 1], "1->2->3->4->5"),
    ])
    def test_push_front(self, datas, expected):
        ll = LinkedList()
        ll.push_front_bulk(datas)
        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, pop_num, expected', [
        pytest.param([1, 2, 3, 4, 5], 2, "3->4->5"),
        pytest.param([1, 2, 3, 4, 5], 4, "5"),
        pytest.param([1, 2, 3, 4, 5], 5, ""),
        pytest.param([1], 1, "")
    ])
    def test_pop_front(self, datas, pop_num, expected):
        ll = LinkedList()
        ll.push_back_bulk(datas)

        for _ in range(pop_num):
            ll.pop_front()

        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, pop_num, expected', [
        pytest.param([1, 2, 3, 4, 5], 2, "1->2->3"),
        pytest.param([1, 2, 3, 4, 5], 4, "1"),
        pytest.param([1, 2, 3, 4, 5], 5, ""),
        pytest.param([1], 1, "")
    ])
    def test_pop_back(self, datas, pop_num, expected):
        ll = LinkedList()
        ll.push_back_bulk(datas)

        for _ in range(pop_num):
            ll.pop_back()

        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas1, datas2', [
        pytest.param([1, 2, 3], [1, 2, 3]),
        pytest.param([1], [1])
    ])
    def test_equal(self, datas1, datas2):
        l1, l2 = LinkedList(), LinkedList()
        l1.push_back_bulk(datas1)
        l2.push_back_bulk(datas2)

        assert l1 == l2

    @pytest.mark.parametrize('datas1, datas2', [
        pytest.param([1, 2, 3], [1, 2]),
        pytest.param([1, 2, 3], [1, 2, 2]),
    ])
    def test_not_equal(self, datas1, datas2):
        l1, l2 = LinkedList(), LinkedList()
        l1.push_back_bulk(datas1)
        l2.push_back_bulk(datas2)

        assert l1 != l2

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1, 2, 3], "3->2->1"),
        pytest.param([1, 2], "2->1"),
        pytest.param([1], "1"),
        pytest.param([1, 2, 3, 4, 5, 6], "6->5->4->3->2->1"),
    ])
    def test_reverse(self, datas, expected):
        ll = LinkedList()
        ll.push_back_bulk(datas)
        ll.reverse()

        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1, 2, 3], "1->2->3"),
        pytest.param([1, 1], "1"),
        pytest.param([1, 1, 1, 1, 1], "1"),
        pytest.param([1, 2, 2, 2, 3], "1->2->3"),
        pytest.param([1, 2, 3, 3, 3], "1->2->3"),
        pytest.param([1, 1, 3, 3, 5, 5], "1->3->5"),

    ])
    def test_remove_duplicate(self, datas, expected):
        l1 = LinkedList()
        l1.push_back_bulk(datas)
        l1.remove_duplicate()
        assert l1.__repr__() == expected

    @pytest.mark.parametrize('datas, k, expected', [
        pytest.param([1, 3, 5, 7, 9], 1, 1),
        pytest.param([1, 3, 5, 7, 9], 2, 3),
        pytest.param([1, 3, 5, 7, 9], 3, 5),
        pytest.param([1, 3, 5, 7, 9], 5, 9)
    ])
    def test_get_kth_from_front(self, datas, k, expected):
        ll = LinkedList()
        ll.push_back_bulk(datas)

        actual = ll.get_kth_from_front(k)
        assert actual == expected

    @pytest.mark.parametrize('datas, k, expected', [
        pytest.param([1, 3, 5, 7, 9], 1, 9),
        pytest.param([1, 3, 5, 7, 9], 2, 7),
        pytest.param([1, 3, 5, 7, 9], 3, 5),
        pytest.param([1, 3, 5, 7, 9], 5, 1)
    ])
    def test_get_kth_from_back(self, datas, k, expected):
        ll = LinkedList()
        ll.push_back_bulk(datas)

        actual = ll.get_kth_from_back(k)
        assert actual == expected
