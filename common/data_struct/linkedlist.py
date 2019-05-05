import sys

from ..exc import ArgError


class Node(object):

    def __init__(self):
        self.data = None
        self.next = None


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


class LinkedList(object):
    """implement a Linked List:
       push_back : O(1)
       push_front: O(1)
       remove    : O(n)
    """

    def __init__(self):
        self._len = 0
        self.head = None
        self.tail = None

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, val):
        self._len = val

    def push_front(self, data):
        """ O(1) """
        new = Node()
        new.data = data

        if self.len == 0:
            self.head = self.tail = new
        else:
            new.next = self.head
            self.head = new

        self.len += 1

    def push_back(self, data):
        """ O(1) """
        new = Node()
        new.data = data

        if self.len == 0:
            self.head = self.tail = new
        else:
            self.tail.next = new
            self.tail = new

        self.len += 1

    def pop_front(self):
        """ O(1) """
        if self.len == 0:
            return None

        ret_d = self.head.data
        if self.len == 1:
            self.head, self.tail = None, None
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

    def get_kth_from_front(self, k):
        if k <= 0:
            raise ArgError('k must be greater than 1')

        if k > self.len:
            raise ArgError('out of range')

        runner = self.head
        for _ in range(k-1):
            runner = runner.next

        return runner.data

    def get_kth_from_back(self, k):
        """
        """
        if k <= 0:
            raise ArgError('k must be greater than 1')

        if k > self.len:
            raise ArgError('out of range')

        forward = self.len - k + 1
        return self.get_kth_from_front(forward)

    def push_back_bulk(self, input_list):
        """ O(n) """
        for i in input_list:
            self.push_back(i)

    def push_front_bulk(self, input_list):
        """ O(n^2) """
        for i in input_list:
            self.push_front(i)

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

    def is_palindrome(self):
        """
        time:  O(n)
        space: O(n)
        use fast and flow runner to control flow
        """
        return is_palindrome(self)

    def __iter__(self):
        """ O(n) """
        runner = self.head
        while runner:
            yield runner.data
            runner = runner.next

    def __eq__(self, other):
        """ O(n) """
        if isinstance(other, LinkedList):
            return is_equal(self, other)
        return False

    def __ne__(self, other):
        """ O(n) """
        return not self.__eq__(other)

    def __repr__(self):
        """ O(n) """
        if self.len == 0:
            return ''

        d_list = list()
        runner = self.head
        while runner:
            d_list.append(str(runner.data))
            runner = runner.next

        return '->'.join(d_list)


def main():
    pass


if __name__ == "__main__":
    sys.exit(main())
