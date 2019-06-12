import sys
from abc import ABC, abstractmethod

from .linkedlist import DLinkedList, CacheNode


class CacheABC(ABC):

    def __init__(self, cap):
        self._cap = cap

    @property
    def cap(self):
        return self._cap

    @property
    @abstractmethod
    def len(self):
        raise NotImplementedError('please implemet this property')

    @abstractmethod
    def set(self, key, val):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def get(self, key):
        raise NotImplementedError('please implemet this method')

    @abstractmethod
    def delete(self, key):
        raise NotImplementedError('please implemet this method')


class LRUCache(CacheABC):
    """
    self.map:
        key:
            User defined key
        value:
            The reference of cache node stored in Doubly Linked List
    self.d_linked_list
        Doubly linked list can provide O(1) remove operation
    """

    def __init__(self, cap):
        super().__init__(cap)
        self.map = dict()
        self.d_linked_list = DLinkedList()

    @property
    def len(self):
        return self.d_linked_list.len

    def set(self, key, val):
        """O(1)"""

        if key in self.map:
            return

        # remove the last node
        if self.d_linked_list.len == self.cap:
            removed_node = self.d_linked_list.pop_back_node()
            self.map.pop(removed_node.key)

        new = CacheNode(key=key, data=val)
        self.d_linked_list.push_front_by_node(new)
        self.map[key] = new

    def get(self, key):

        if key not in self.map:
            return None

        node = self.map[key]

        # move the node to the first
        self.d_linked_list.revmoe_node(node)
        self.d_linked_list.push_front_by_node(node)

        return node.data

    def delete(self, key):

        if key not in self.map:
            return None

        node = self.map[key]
        self.d_linked_list.revmoe_node(node)
        self.map.pop(key)

    def __repr__(self):
        return repr(self.d_linked_list)


def main():
    cache = LRUCache(3)
    d = {"a": 100, "b": 200, "c": 300}
    for k, v in d.items():
        cache.set(k, v)
    print(cache)
    print(cache.len)


if __name__ == "__main__":
    sys.exit(main())
