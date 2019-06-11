import sys
from abc import ABC, abstractmethod


class Node(object):

    def __init__(self, data=None, next_=None):
        self.data = data
        self.next = next_

    def __repr__(self):
        return str(self.data)


def is_equal(q1, q2):

    if q1.len != q2.len:
        return False

    for v1, v2 in zip(q1, q2):
        if v1 != v2:
            return False

    return True


class QueueABC(ABC):

    def __init__(self):
        self.head = None
        self.tail = None
        self._len = 0

    def __iter__(self):
        runner = self.head
        while runner:
            yield runner.data
            runner = runner.next

    def __eq__(self, other):
        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        else:
            return is_equal(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, val):
        self._len = val

    def bulk_add(self, input_list):
        """ O(n) """
        for v in input_list:
            self.add(v)

    @abstractmethod
    def add(self, val):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def remove(self):
        raise NotImplementedError('please implemet this method')


class Queue(QueueABC):

    def __init__(self):
        super().__init__()

    def add(self, val):
        """ O(1) """
        new = Node(data=val)

        # the first node
        if self.len == 0:
            self.head = new
        else:
            self.tail.next = new

        self.tail = new
        self.len += 1

    def remove(self):
        """ O(1) """
        if self.len < 1:
            return None

        ret = self.head

        # 1 node
        if self.head is self.tail:
            self.tail = None

        self.head = self.head.next
        self.len -= 1

        return ret.data

    def __repr__(self):
        """ O(n) """
        if self.len == 0:
            return ''

        d_list = list()
        runner = self.head
        while runner:
            d_list.append(runner.__repr__())
            runner = runner.next

        return '->'.join(d_list)


def main():
    data = [1, 2, 3]
    q = Queue()
    q.bulk_add(data)
    print(q)
    print(q.len)

    for _ in data:
        q.remove()
        print(q)
        print(q.len)

    q = Queue()
    q.bulk_add(data)
    print(q)
    print(q.len)

if __name__ == "__main__":
    sys.exit(main())
