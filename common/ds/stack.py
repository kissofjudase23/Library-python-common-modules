import sys
from abc import ABC, abstractmethod


class Node(object):
    def __init__(self, data=None, next=None):
        self.data = data
        self.prev = next


def is_equal(s1, s2):
    """ O(n)
    """

    if s1.len != s2.len:
        return False

    for v1, v2 in zip(s1, s2):
        if v1 != v2:
            return False

    return True


class StackABC(ABC):

    def __init__(self):
        self.top = None
        self.len = 0

    def __iter__(self):
        runner = self.top
        while runner:
            yield runner.data
            runner = runner.prev

    def __eq__(self, other):
        if not self.__class__.__name__ == other.__class__.__name__:
            return False
        else:
            return (self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, val):
        self._len = val

    def bulk_push(self, input_list):
        """ O(n) """
        for i in input_list:
            self.push(i)

    @abstractmethod
    def push(self, val):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def pop(self):
        raise NotImplementedError('please implemet this method')


class Stack(StackABC):

    def __init__(self):
        super().__init__()

    def push(self, val):
        new = Node(data=val)
        if self.len != 0:
            new.prev = self.top

        self.top = new
        self.len += 1

    def pop(self):
        if self.len == 0:
            return None

        ret = self.top.data
        self.top = self.top.prev
        self.len -= 1
        return ret

    def __repr__(self):
        """ O(n) """
        if self.len == 0:
            return ''

        d_list = list()
        runner = self.top
        while runner:
            d_list.append(str(runner.data))
            runner = runner.prev

        return '->'.join(d_list)


def main():
    pass

if __name__ == "__main__":
    sys.exit(main())
