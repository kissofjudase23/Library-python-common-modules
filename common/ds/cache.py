import sys
from abc import ABC, abstractmethod

from .linkedlist import DLinkedList, CacheNode


class CacheABC(ABC):

    def __init__(self, cap):
        self._cap = _cap

    @property
    def capacity(self):
        return self._cap

    @capacity.setter
    def capacity(self, val):
        self._cap = val

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

    def __init__(self, size):
        super().__init__(size)
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
        if self.len == self.capacity:
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

    def delete(self, key):

        if key not in self.map:
            return None

        node = self.map[key]
        self.d_linked_list.revmoe_node(node)
        self.map.pop(key)

    def __repr__(self):
        return self.d_linked_list.__repr__()
