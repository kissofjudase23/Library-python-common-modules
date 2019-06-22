import sys
import math
from abc import ABC, abstractmethod

from ..exc import ArgError


class Node(object):

    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

    def __repr__(self):
        return str(self.data)


class CacheNode(Node):
    def __init__(self, key=None, data=None, prev=None, next=None):
        super().__init__(data=data, prev=prev, next=next)
        self.key = key

    def __repr__(self):
        return f'{self.key}:{self.data}'


def is_equal(l1, l2):
    """ O(n)
    """

    if l1.len != l2.len:
        return False

    for v1, v2 in zip(l1, l2):
        if v1 != v2:
            return False

    return True


def is_palindrome(l):
    """
    time:  O(n)
    space: O(n)
    use mid to control flow
    """
    len = l.len
    if len == 0:
        return False
    if len == 1:
        return True

    stack = list()
    odd = True if len % 2 == 1 else False
    mid = int(math.ceil(float(len/2)))
    cnt = 0

    for v in l:
        cnt += 1
        if cnt < mid:
            stack.append(v)
        elif cnt == mid:
            if odd:
                continue  # skip the middle node
            else:
                stack.append(v)   # do not have middle node
        else:
            if v != stack.pop():
                return False
    return True


def is_palindrome_v2(l):
    """
    time:  O(n)
    space: O(n)
    use fast and flow runner to control flow
    """

    len = l.len
    if len == 0:
        return False
    if len == 1:
        return True

    odd = True if len % 2 == 1 else False
    stack = list()
    slow_runner = fast_runner = l.head

    while fast_runner:
        stack.append(slow_runner.data)
        fast_runner = fast_runner.next
        if fast_runner:   # forward 2-steps if possible
            fast_runner = fast_runner.next
        slow_runner = slow_runner.next

    if odd:
        stack.pop()

    while slow_runner:
        if slow_runner.data != stack.pop():
            return False
        slow_runner = slow_runner.next

    return True


def find_loop_beginning(l):
    slow_runner = fast_runner = l.head
    while True:
        fast_runner = fast_runner.next.next
        slow_runner = slow_runner.next
        if fast_runner is slow_runner:
            break

    target_runner = l.head
    while True:
        slow_runner = slow_runner.next
        target_runner = target_runner.next
        if target_runner is slow_runner:
            break

    return target_runner.data


def is_palindrome_recursive(l):
    """
    time:  O(n)
    space: O(n)
    """
    def is_palindrome(head, len):
        # stop point, when the length is 0 or 1 means middle node
        if len == 1:   # odd
            return True, head.next
        elif len == 0:  # even
            return True, head

        ret, compare = is_palindrome(head.next, len-2)
        if not ret:
            return False, None
        if head.data == compare.data:
            # compare in next round
            return True, compare.next

        return False, None

    len = l.len
    if len == 0:
        return False
    if len == 1:
        return True

    ret, _ = is_palindrome(l.head, len)
    return ret


def sum_backward(l1, l2):
    """
    time:  O(len(l1) + len(l2))
    space: O(1)
    l1 = 7->1->6 = 617
    l2 = 5->9->2 = 295
    return 617 + 295 = 912
    """

    def _sum_backward(l):
        """
        7->1->6 = 617
        7 + 10 + 600 = 617
        """
        if l.len < 1:
            return 0

        val = 0
        base = 1
        for i in l:
            val += (base * i)
            base *= 10
        return val
    return _sum_backward(l1) + _sum_backward(l2)


def sum_backward_recursive(l1, l2):
    """
    time:  O(len(l1) + len(l2))
    space: O(max(len(l1), len(l2)))

    l1 = 7->1->6 = 617
    l2 = 5->9->2 = 295
    return 617 + 295 = 912
    """

    def _sum_backward(node, base=1):
        """
        7->1->6 = 617
        7 + 10 + 600 = 617
        """
        if not node:
            return 0

        cur = node.data * base
        prev = _sum_backward(node.next, base * 10)
        return cur + prev

    return _sum_backward(l1.head) + _sum_backward(l2.head)


def sum_forward(l1, l2):
    """
    time:  O(len(l1) + len(l2))
    space: O(1)

    l1 = 7->1->6 = 716
    l2 = 5->9->2 = 592
    return 716 + 592 = 1308
    """

    def _sum_forward(l):
        """
        7->1->6 = 716
        700 + 10 + 6 = 716
        """
        if l.len < 1:
            return 0

        val = 0
        for i in l:
            val = (val * 10) + i

        return val

    return _sum_forward(l1) + _sum_forward(l2)


def sum_forward_recursive(l1, l2):
    """
    time:  O(len(l1) + len(l2))
    space: O(max(len(l1), len(l2)))

    l1 = 7->1->6 = 716
    l2 = 5->9->2 = 592
    return 716 + 592 = 1308
    """

    def _sum_forward(node, prev=0):
        """
        7->1->6 = 716
        700 + 10 + 6 = 716
        """
        if not node:
            return prev

        cur = prev * 10 + node.data
        return _sum_forward(node.next, cur)

    return _sum_forward(l1.head) + _sum_forward(l2.head)


class LinkedListABC(ABC):

    def __init__(self):
        self._len = 0
        self.head = None
        self.tail = None

    def __iter__(self):
        """ O(n) """
        runner = self.head
        while runner:
            yield runner.data
            runner = runner.next

    def __eq__(self, other):
        """ O(n) """
        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        return is_equal(self, other)

    def __ne__(self, other):
        """ O(n) """
        return not self.__eq__(other)

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, val):
        self._len = val

    def bulk_push_back(self, input_list: list):
        """ O(n) """
        for i in input_list:
            self.push_back(i)

    def bulk_push_front(self, input_list: list):
        """ O(n^2) """
        for i in input_list:
            self.push_front(i)

    @abstractmethod
    def push_front_by_node(self, new):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def push_back_by_node(self, new):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def push_front(self, data):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def push_back(self, data):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def pop_front(self):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def pop_back(self):
        raise NotImplementedError('please implemet this method')


class LinkedList(LinkedListABC):
    """Singly Linked List
       push_back : O(1)
       push_front: O(1)
       remove    : O(n)
    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        """ O(n) """
        if self.len == 0:
            return ''

        d_list = list()
        runner = self.head
        while runner:
            d_list.append(repr(runner))
            runner = runner.next

        return '->'.join(d_list)

    def push_front_by_node(self, new):
        if self.len == 0:
            self.head = self.tail = new
        else:
            new.next = self.head
            self.head = new

        self.len += 1

    def push_back_by_node(self, new):
        if self.len == 0:
            self.head = self.tail = new
        else:
            self.tail.next = new
            self.tail = new

        self.len += 1

    def push_front(self, data):
        """ O(1) """
        new = Node()
        new.data = data
        self.push_front_by_node(new)

    def push_back(self, data):
        """ O(1) """
        new = Node()
        new.data = data
        self.push_back_by_node(new)

    def pop_front(self):
        """ O(1) """
        if self.len == 0:
            return None

        ret_d = self.head.data
        if self.len == 1:
            self.head = self.tail = None
        else:  # >=2
            self.head = self.head.next

        self.len -= 1
        return ret_d

    def pop_back(self):
        """ O(N) """
        if self.len == 0:
            return None

        if self.len == 1:
            ret_d = self.tail.data
            self.head, self.tail = None, None
            self.len -= 1
            return ret_d

        runner = self.head
        while runner:
            if runner.next is self.tail:
                ret_d = self.tail.data
                self.tail = runner
                self.tail.next = None
                self.len -= 1
                return ret_d
            else:
                runner = runner.next

    def remove(self, target):
        """ O(n) """
        prev = None
        runner = self.head
        while runner:
            if runner.data == target:
                self.len -= 1
                if prev:
                    prev.next = runner.next
                if runner is self.head:
                    self.head = runner.next
                if runner is self.tail:
                    self.tail = prev
            else:
                prev = runner
                runner = runner.next

        if prev:
            self.tail = prev

    def remove_middle(self):
        """ time:  O(n)
            space: O(n)
        """
        if self.len <= 1:
            return

        fast_runner, slow_runner = self.head, self.head
        prev = None
        while fast_runner and fast_runner.next:
            fast_runner = fast_runner.next
            # forward 2 steps if possible
            if fast_runner:
                fast_runner = fast_runner.next

            prev = slow_runner
            slow_runner = slow_runner.next

        if prev:
            prev.next = slow_runner.next

    def remove_duplicate(self):
        """ time:  O(n)
            space: O(n)
        """
        if self.len <= 1:
            return

        hash_table = dict()
        prev = None
        cur = self.head
        while cur:
            if cur.data in hash_table:
                if prev:
                    prev.next = cur.next

            else:
                hash_table[cur.data] = True
                prev = cur

            cur = cur.next

        if prev:
            self.tail = prev

    def remove_duplicate_space_optimize(self):
        """ time:  O(n^2) <--- poor performance
            space: O(1)
        """
        if self.len <= 1:
            return

        slow_runner = self.head

        while slow_runner and slow_runner.next:
            target = slow_runner.data
            prev = slow_runner
            fast_runner = slow_runner.next
            while fast_runner:
                if fast_runner.data == target:
                    prev.next = fast_runner.next
                else:
                    prev = fast_runner
                fast_runner = fast_runner.next

            slow_runner = slow_runner.next

        if prev:
            self.tail = prev

    def get_kth_from_front(self, k):
        """ O(n) """
        if k <= 0:
            raise ArgError('k must be greater than 1')

        if k > self.len:
            raise ArgError('out of range')

        runner = self.head
        for _ in range(k-1):
            runner = runner.next

        return runner.data

    def get_kth_from_back(self, k):
        """ O(n) """
        if k <= 0:
            raise ArgError('k must be greater than 1')

        if k > self.len:
            raise ArgError('out of range')

        forward = self.len - (k - 1)
        return self.get_kth_from_front(forward)

    def get_kth_from_back_iter(self, k):
        """ Time: O(n)
            Space: O(1)
            Assume that self.len is unknown
        """
        if k <= 0:
            raise ArgError('k must be greater than 1')

        fast_runner = self.head
        for _ in range(k):
            if not fast_runner:
                raise ArgError('ouf of range')
            fast_runner = fast_runner.next

        slow_runner = self.head
        while fast_runner:
            fast_runner = fast_runner.next
            slow_runner = slow_runner.next

        return slow_runner.data

    def get_kth_from_back_recursive(self, k):
        """ Time:  O(n)
            Space: O(n),
            Assume that self.len is unknown
            ugly code -.-
        """
        def _get_kth_from_back_recur(head, k_):

            if not head:  # null
                return 0, None
            else:
                idx, data_ = _get_kth_from_back_recur(head.next, k_)
                idx += 1
                if idx == k_:  # kth from the back
                    return idx, head.data
                else:
                    return idx, data_

        if k <= 0:
            raise ArgError('k must be greater than 1')

        _, data = _get_kth_from_back_recur(self.head, k)
        if not data:
            raise ArgError("out of range")
        else:
            return data

    def switch_nodes(self):
        """ O(n)
            1->2->3->4  ==> 2->1->4->3
        """
        if self.len <= 1:
            return

        # init
        prev = None
        cur, next_ = self.head, self.head.next
        self.head = next_

        while cur and next_:
            # switch
            if prev:
                prev.next = next_
            cur.next = next_.next
            next_.next = cur

            # for next round
            prev = cur
            cur = cur.next
            # end condition is cur is None
            if cur:
                next_ = cur.next

        if prev:
            self.tail = prev

    def reverse(self):
        """ O(n) """
        if self.len <= 1:
            return

        # init, >=2 nodes
        cur = self.head
        next_ = self.head.next
        cur.next = None

        while cur and next_:
            tmp = next_.next
            next_.next = cur
            cur, next_ = next_, tmp

        self.head, self.tail = self.tail, self.head

    def reverse_recursive(self):

        def _reverse_recursive(prev, cur):
            if not cur:
                self.head = prev
                return

            next_ = cur.next
            cur.next = prev
            _reverse_recursive(prev=cur, cur=next_)

        if self.len < 1:
            return

        next_ = self.head.next
        self.tail = self.head
        self.head.next = None
        _reverse_recursive(prev=self.head, cur=next_)

    def release(self):
        """ O(n) """
        runner = self.head
        while runner:
            release = runner
            runner = runner.next
            release.next = None
            del release

        del self.head
        del self.tail
        self.head, self.tail = None, None
        self.len = 0

    def partition_stable(self, pivot):
        """
        time: O(n)
        space: O(n)
        create two linked lists and merge them
        """

        def append_new_node(head, tail, node):
            if not head:
                head = runner

            if tail:
                tail.next = runner

            tail = runner
            return head, tail

        """
        3->5->8->5->10->2->1 ,pivot=5
        3->2->1->5->8->5->10
        """
        if self.len <= 1:
            return

        before_head, before_tail = None, None
        after_head, after_tail = None, None
        runner = self.head

        # create 2 linked list, one is < pivot, another is >= pivot
        while runner:
            if runner.data < pivot:
                before_head, before_tail = append_new_node(before_head, before_tail, runner)
            else:
                after_head, after_tail = append_new_node(after_head, after_tail, runner)

            runner = runner.next

        # merge two linked list
        if after_tail:
            after_tail.next = None

        if not before_head:
            self.head = after_head
            return

        self.head = before_head
        before_tail.next = after_head

    def partition_non_stable(self, pivot):
        """
        time: O(n)
        space: O(n)
        """
        if self.len <= 1:
            return

        head, tail = None, None

        runner = self.head

        while runner:
            target = runner
            runner = runner.next
            if target.data < pivot:
                if head:
                    target.next = head
                head = target
                if not tail:  # first node
                    tail = head
            else:
                if tail:
                    tail.next = target
                tail = target
                if not head:  # first node
                    head = target

        if tail:
            tail.next = None

        self.head = head

    def is_palindrome(self):
        """
        time:  O(n)
        space: O(n)
        use mid to control flow
        """
        return is_palindrome(self)

    def is_palindrome_v2(self):
        """
        time:  O(n)
        space: O(n)
        use fast and flow runner to control flow
        """

        return is_palindrome_v2(self)

    def is_palindrome_recursive(self):
        """
        time:  O(n)
        space: O(n)
        """
        return is_palindrome_recursive(self)

    def make_circular(self):
        """
        make linkedlist circular
        1->2->3->1->2->3 .... infinite loop
        """
        self.tail.next = self.head


class DLinkedList(LinkedListABC):
    """ Doubly Linked List
    """

    def __init__(self):
        super().__init__()

    def __repr__(self):
        """ O(n) """
        if self.len == 0:
            return ''

        d_list = list()
        runner = self.head
        while runner:
            d_list.append(repr(runner))
            runner = runner.next

        return '<->'.join(d_list)

    def push_front_by_node(self, new):
        if self.len == 0:
            self.head = self.tail = new
        else:
            self.head.prev = new
            new.next = self.head
            self.head = new

        self.len += 1

        return new

    def push_back_by_node(self, new):
        if self.len == 0:
            self.head = self.tail = new
        else:
            self.tail.next = new
            new.prev = self.tail
            self.tail = new
        self.len += 1

        return new

    def push_front(self, data):
        """O(1)"""
        new = Node(data)

        return self.push_front_by_node(new)

    def push_back(self, data):
        """O(1)"""
        new = Node(data)

        return self.push_back_by_node(new)

    def pop_front_node(self):
        """O(1)"""
        if self.len == 0:
            return None

        ret_n = self.head
        if self.len == 1:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        self.len -= 1
        return ret_n

    def pop_back_node(self):
        """O(1)"""
        if self.len == 0:
            return None

        ret_n = self.tail
        if self.len == 1:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        self.len -= 1
        return ret_n

    def pop_front(self):
        ret_n = self.pop_front_node()
        if not ret_n:
            return None
        return ret_n.data

    def pop_back(self):
        ret_n = self.pop_back_node()
        if not ret_n:
            return None

        return ret_n.data

    def revmoe_node(self, remove_node):
        """
        The node should be in the list
        """
        if remove_node.prev:
            remove_node.prev.next = remove_node.next
        else:
            # remove_node is head node
            self.head = remove_node.next

        if remove_node.next:
            remove_node.next.prev = remove_node.prev
        else:
            # remove_node is tail node
            self.tail = remove_node.prev

        self.len -= 1


def main():
    datas = [1, 2, 3]
    l2 = LinkedList()
    l2.bulk_push_back(datas)
    l2.reverse_recursive()

    return 0


if __name__ == "__main__":
    sys.exit(main())
