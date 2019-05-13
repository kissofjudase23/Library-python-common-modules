import pytest

from ...data_struct.linkedlist import LinkedList, DLinkedList, Node
from ...exc import ArgError

from ...data_struct import linkedlist as linkedlist


class TestLinkedList(object):

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([1, 2], "1->2"),
        pytest.param([1, 2, 3, 4, 5], "1->2->3->4->5"),
    ])
    def test_push_back(self, datas, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)
        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([2, 1], "1->2"),
        pytest.param([5, 4, 3, 2, 1], "1->2->3->4->5"),
    ])
    def test_push_front(self, datas, expected):
        ll = LinkedList()
        ll.bulk_push_front(datas)
        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, pop_num, expected', [
        pytest.param([1, 2, 3, 4, 5], 2, "3->4->5"),
        pytest.param([1, 2, 3, 4, 5], 4, "5"),
        pytest.param([1, 2, 3, 4, 5], 5, ""),
        pytest.param([1], 1, "")
    ])
    def test_pop_front(self, datas, pop_num, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)

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
        ll.bulk_push_back(datas)

        for _ in range(pop_num):
            ll.pop_back()

        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas1, datas2', [
        pytest.param([1, 2, 3], [1, 2, 3]),
        pytest.param([1], [1])
    ])
    def test_equal(self, datas1, datas2):
        l1, l2 = LinkedList(), LinkedList()
        l1.bulk_push_back(datas1)
        l2.bulk_push_back(datas2)

        assert l1 == l2

    @pytest.mark.parametrize('datas1, datas2', [
        pytest.param([1, 2, 3], [1, 2]),
        pytest.param([1, 2, 3], [1, 2, 2]),
    ])
    def test_not_equal(self, datas1, datas2):
        l1, l2 = LinkedList(), LinkedList()
        l1.bulk_push_back(datas1)
        l2.bulk_push_back(datas2)

        assert l1 != l2

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1, 2, 3], "3->2->1"),
        pytest.param([1, 2], "2->1"),
        pytest.param([1], "1"),
        pytest.param([1, 2, 3, 4, 5, 6], "6->5->4->3->2->1"),
    ])
    def test_reverse(self, datas, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)
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
        l1.bulk_push_back(datas)
        l1.remove_duplicate()
        assert l1.__repr__() == expected

        l2 = LinkedList()
        l2.bulk_push_back(datas)
        l2.remove_duplicate_space_optimize()
        assert l2.__repr__() == expected

    @pytest.mark.parametrize('datas, k, expected', [
        pytest.param([1, 3, 5, 7, 9], 1, 1),
        pytest.param([1, 3, 5, 7, 9], 2, 3),
        pytest.param([1, 3, 5, 7, 9], 3, 5),
        pytest.param([1, 3, 5, 7, 9], 5, 9)
    ])
    def test_get_kth_from_front(self, datas, k, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)

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
        ll.bulk_push_back(datas)

        assert ll.get_kth_from_back(k) == expected
        assert ll.get_kth_from_back_iter(k) == expected
        assert ll.get_kth_from_back_recursive(k) == expected

    @pytest.mark.parametrize('datas, k', [
        pytest.param([1, 3, 5, 7, 9], 6),
        pytest.param([1, 3, 5, 7, 9], 10000000000000),
        pytest.param([1, 3, 5, 7, 9], -1)
    ])
    def test_get_kth_from_back_raise(self, datas, k):
        ll = LinkedList()
        ll.bulk_push_back(datas)

        with pytest.raises(ArgError):
            ll.get_kth_from_back(k)

        with pytest.raises(ArgError):
            ll.get_kth_from_back_iter(k)

        with pytest.raises(ArgError):
            ll.get_kth_from_back_recursive(k)

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1, 2, 3, 4], "2->1->4->3"),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8, 9], "2->1->4->3->6->5->8->7->9"),
        pytest.param([1, 2, 3, 4, 5], "2->1->4->3->5"),
        pytest.param([1], "1")
    ])
    def test_switch_nodes(self, datas, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)
        ll.switch_nodes()
        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([1, 3, 5], "1->5"),
        pytest.param([1, 2, 3, 4, 5], "1->2->4->5"),
    ])
    def test_remove_nodes(self, datas, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)
        ll.remove_middle()
        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, pivot, expected', [
        pytest.param([1, 3, 5], 5, "1->3->5"),
        pytest.param([3, 5, 8, 5, 10, 2, 1], 5, "3->2->1->5->8->5->10"),
        pytest.param([3, 5, 8, 5, 10, 2, 1], 11, "3->5->8->5->10->2->1"),
        pytest.param([3, 5, 8, 5, 10, 2, 1], 0, "3->5->8->5->10->2->1")
    ])
    def test_partition_stable(self, datas, pivot, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)
        ll.partition_stable(pivot)
        assert ll.__repr__() == expected

    @pytest.mark.parametrize('datas, pivot, expected', [
        pytest.param([1, 3, 5], 5, "3->1->5"),
        pytest.param([3, 5, 8, 5, 10, 2, 1], 5, "1->2->3->5->8->5->10"),
        pytest.param([3, 5, 8, 5, 10, 2, 1], 11, "1->2->10->5->8->5->3"),
        pytest.param([3, 5, 8, 5, 10, 2, 1], 0, "3->5->8->5->10->2->1")
    ])
    def test_partition_non_stable(self, datas, pivot, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)
        ll.partition_non_stable(pivot)
        assert ll.__repr__() == expected

    @pytest.mark.parametrize('data1, data2, expected', [
        pytest.param([7, 1, 6], [5, 9, 2], 912),
        pytest.param([9, 7, 8], [6, 8, 5], 1465),
        pytest.param([1, 0, 0], [1, 0, 0, 0, 0], 2),
        pytest.param([0, 0, 1], [0, 0, 0, 0, 1], 10100)
    ])
    def test_sum_backward(self, data1, data2, expected):
        l1, l2 = LinkedList(), LinkedList()
        l1.bulk_push_back(data1)
        l2.bulk_push_back(data2)
        actual = linkedlist.sum_backward(l1, l2)
        assert actual == expected

    @pytest.mark.parametrize('data1, data2, expected', [
        pytest.param([7, 1, 6], [5, 9, 2], 912),
        pytest.param([9, 7, 8], [6, 8, 5], 1465),
        pytest.param([1, 0, 0], [1, 0, 0, 0, 0], 2),
        pytest.param([0, 0, 1], [0, 0, 0, 0, 1], 10100)
    ])
    def test_sum_backward_recursive(self, data1, data2, expected):
        l1, l2 = LinkedList(), LinkedList()
        l1.bulk_push_back(data1)
        l2.bulk_push_back(data2)
        actual = linkedlist.sum_backward_recursive(l1, l2)
        assert actual == expected

    @pytest.mark.parametrize('data1, data2, expected', [
        pytest.param([7, 1, 6], [5, 9, 2], 1308),
        pytest.param([9, 7, 8], [6, 8, 5], 1663),
        pytest.param([1, 0, 0], [1, 0, 0, 0, 0], 10100),
        pytest.param([0, 0, 1], [0, 0, 0, 0, 1], 2)
    ])
    def test_sum_forward(self, data1, data2, expected):
        l1, l2 = LinkedList(), LinkedList()
        l1.bulk_push_back(data1)
        l2.bulk_push_back(data2)
        actual = linkedlist.sum_forward(l1, l2)
        assert actual == expected

    @pytest.mark.parametrize('data1, data2, expected', [
        pytest.param([7, 1, 6], [5, 9, 2], 1308),
        pytest.param([9, 7, 8], [6, 8, 5], 1663),
        pytest.param([1, 0, 0], [1, 0, 0, 0, 0], 10100),
        pytest.param([0, 0, 1], [0, 0, 0, 0, 1], 2)
    ])
    def test_sum_forward_recursive(self, data1, data2, expected):
        l1, l2 = LinkedList(), LinkedList()
        l1.bulk_push_back(data1)
        l2.bulk_push_back(data2)
        actual = linkedlist.sum_forward_recursive(l1, l2)
        assert actual == expected

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1, 3, 5, 3, 1], True),
        pytest.param([1, 3, 3, 1], True),
        pytest.param([1], True),
        pytest.param([1, 1], True),
        pytest.param([1, 3, 5, 3, 0], False),
        pytest.param([1, 3, 3, 0], False),
        pytest.param([1, 0], False)
    ])
    def test_is_palindrome(self, datas, expected):
        ll = LinkedList()
        ll.bulk_push_back(datas)
        assert ll.is_palindrome() is expected
        assert ll.is_palindrome_v2() is expected
        assert ll.is_palindrome_recursive() is expected

    @pytest.mark.parametrize('data1, data2, expected', [
        pytest.param([1, 2, 3], [100, 200, 300, 400], 100),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8], [100, 200, 300], 100),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8], [100, 200], 100),
        pytest.param([1, 2, 3, 4, 5, 6, 7, 8], [100], 100),
    ])
    def find_loop_beginning(self, data1, data2, expected):
        l1 = LinkedList()
        l1.bulk_push_back(data1)
        l2 = LinkedList()
        l2.bulk_push_back(data2)
        l1.tail.next = l2.head
        l2.make_circular()
        actual = linkedlist.find_loop_beginning(l1)
        assert actual is expected


class TestDoublyLinkedList(object):
    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([1, 2], "1<->2"),
        pytest.param([1, 2, 3, 4, 5], "1<->2<->3<->4<->5"),
    ])
    def test_push_back(self, datas, expected):
        dll = DLinkedList()
        dll.bulk_push_back(datas)
        assert dll.__repr__() == expected

    @pytest.mark.parametrize('datas, expected', [
        pytest.param([1], "1"),
        pytest.param([1, 2], "2<->1"),
        pytest.param([1, 2, 3, 4, 5], "5<->4<->3<->2<->1"),
    ])
    def test_push_front(self, datas, expected):
        dll = DLinkedList()
        dll.bulk_push_front(datas)
        assert dll.__repr__() == expected

    @pytest.mark.parametrize('datas, pop_cnt, expected', [
        pytest.param([1], 1, ""),
        pytest.param([1, 2, 3, 4, 5], 1, "1<->2<->3<->4"),
        pytest.param([1, 2, 3, 4, 5], 3, "1<->2"),
        pytest.param([1, 2, 3, 4, 5], 4, "1"),
        pytest.param([1, 2, 3, 4, 5], 5, ""),
    ])
    def test_pop_back(self, datas, pop_cnt, expected):
        dll = DLinkedList()
        dll.bulk_push_back(datas)

        for _ in range(pop_cnt):
            dll.pop_back()

        assert dll.__repr__() == expected

    @pytest.mark.parametrize('datas, pop_cnt, expected', [
        pytest.param([1], 1, ""),
        pytest.param([1, 2, 3, 4, 5], 1, "2<->3<->4<->5"),
        pytest.param([1, 2, 3, 4, 5], 3, "4<->5"),
        pytest.param([1, 2, 3, 4, 5], 4, "5"),
        pytest.param([1, 2, 3, 4, 5], 5, ""),
    ])
    def test_pop_front(self, datas, pop_cnt, expected):
        dll = DLinkedList()
        dll.bulk_push_back(datas)

        for _ in range(pop_cnt):
            dll.pop_front()

        assert dll.__repr__() == expected

    def test_remove_nodes(self):
        dll = DLinkedList()

        nodes = [Node(0), Node(1), Node(2)]

        for node in nodes:
            dll.push_back_by_node(node)
        assert dll.__repr__() == "0<->1<->2"

        dll.revmoe_node(nodes[1])  # remove Node(1)
        assert dll.__repr__() == "0<->2"

        dll.revmoe_node(nodes[0])  # remove Node(0)
        assert dll.__repr__() == "2"

        dll.revmoe_node(nodes[2])  # remove Node(2)
        assert dll.__repr__() == ""
