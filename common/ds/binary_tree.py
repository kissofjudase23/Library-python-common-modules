import sys
from abc import ABC, abstractmethod
from collections import deque


class TreeNode(object):

    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Traversal(object):

    @staticmethod
    def preorder(root: TreeNode) -> list:
        visits = list()
        stack = list()
        current = root

        while current or stack:
            if current:
                visits.append(current.val)
                if current.right:
                    stack.append(current.right)
                current = current.left
            else:
                current = stack.pop()

        return visits

    @staticmethod
    def preorder_v2(root: TreeNode) -> list:
        """
        https://www.geeksforgeeks.org/iterative-preorder-traversal/
        """
        visits = list()
        stack = list()

        if not root:
            return visits

        stack.append(root)
        while stack:
            current = stack.pop()
            visits.append(current.val)
            if current.right:
                stack.push(current.right)
            if current.left:
                stack.push(current.left)

        return visits

    @staticmethod
    def preorder_recursive(root: TreeNode) -> list:
        visits = list()

        def _preorder_recursive(node: TreeNode):
            if not node:
                return

            visits.append(node.val)
            _preorder_recursive(node.left)
            _preorder_recursive(node.right)

        if not root:
            return visits

        _preorder_recursive(root)
        return visits

    @staticmethod
    def inorder(root: TreeNode) -> list:
        """
        Ref:
        https://stackoverflow.com/questions/2116662/help-me-understand-inorder-traversal-without-using-recursion
        """
        visits = list()
        stack = list()
        current = root
        while current or stack:
            if current:
                stack.append(current)
                current = current.left

            else:   # len(stack)
                current = stack.pop()
                visits.append(current.val)
                current = current.right

        return visits

    @staticmethod
    def inorder_recursive(root: TreeNode) -> list:
        visits = list()

        def _inorder_recursive(node: TreeNode):
            if not node:
                return

            _inorder_recursive(node.left)
            visits.append(node.val)
            _inorder_recursive(node.right)

        if not root:
            return visits

        _inorder_recursive(root)
        return visits

    @staticmethod
    def postorder(root: TreeNode) -> list:
        """
        Ref:
        https://www.geeksforgeeks.org/iterative-postorder-traversal/
        """
        stack = list()
        visits = list()

        if not root:
            return visits

        stack.append(root)

        while stack:
            current = stack.pop()
            visits.append(current.val)

            if current.left:
                stack.append(current.left)
            if current.right:
                stack.append(current.right)

        visits.reverse()

        return visits

    @staticmethod
    def postorder_recursive(root: TreeNode) -> list:
        visits = list()

        def _postorder_recursive(node: TreeNode):
            if not node:
                return

            _postorder_recursive(node.left)
            _postorder_recursive(node.right)
            visits.append(node.val)

        if not root:
            return visits

        _postorder_recursive(root)
        return visits

    @staticmethod
    def bfs(root: TreeNode) -> list:
        visits = list()
        queue = deque()

        if not root:
            return visits

        queue.append(root)
        while queue:
            current = queue.popleft()
            visits.append(current.val)
            if current.left:
                queue.append(current.left)

            if current.right:
                queue.append(current.right)

        return visits

    def level_order_bfs(root: TreeNode) -> list:
        visits = list()
        queue = deque()

        if not root:
            return visits

        queue.append(root)

        while queue:
            level_visits = list()
            level_size = len(queue)
            for _ in range(level_size):
                current = queue.popleft()
                level_visits.append(current.val)
                if current.left:
                    queue.append(current.left)
                if current.right:
                    queue.append(current.right)

            visits.append(level_visits)
        return visits

    def level_order_dfs(root: TreeNode) ->list:

        visits = list()

        def _level_order_dfs(node, level):
            if len(visits) < (level + 1):
                visits.append(list())

            visits[level].append(node.val)

            if node.left:
                _level_order_dfs(node.left, level+1)
            if node.right:
                _level_order_dfs(node.right, level+1)

        if not root:
            return visits

        _level_order_dfs(node=root, level=0)

        return visits


class BinaryTreeABC(ABC):

    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, node: TreeNode):
        self._root = node

    @abstractmethod
    def insert(self, val) -> None:
        raise NotImplementedError('please implemet this method')

    def bulk_insert(self, vals: list) -> None:
        for val in vals:
            self.insert(val)

    @abstractmethod
    def insert_recursive(self, val) -> None:
        raise NotImplementedError('please implemet this method')

    # @abstractmethod
    # def find(self, val) -> True:
    #     raise NotImplementedError('please implemet this method')

    # @abstractmethod
    # def find_recursive(self, val) -> True:
    #     raise NotImplementedError('please implemet this method')


class BST(BinaryTreeABC):

    def __init__(self):
        super().__init__()

    def insert(self, val) -> None:
        new = TreeNode(val=val)
        if not self.root:
            self.root = new
            return

        parent = None
        current = self.root
        while current:
            parent = current
            if new.val <= current.val:
                current = current.left
            else:
                current = current.right

        if new.val <= parent.val:
            parent.left = new
        else:
            parent.right = new

    def insert_recursive(self, val) -> None:

        def _insert_recursive(current: TreeNode, new: TreeNode):
            if new.val <= current.val:
                if current.left:
                    _insert_recursive(current.left, new)
                else:
                    current.left = new
            else:
                if current.right:
                    _insert_recursive(current.right, new)
                else:
                    current.right = new

        new = TreeNode(val=val)
        if not self.root:
            self.root = new
            return

        _insert_recursive(self.root, new)


def main():
    bst = BST()
    bst.bulk_insert([7, 5, 1, 3, 11, 9, 14])
    print(Traversal.inorder_recursive(bst.root))
    print(Traversal.inorder(bst.root))

    print(Traversal.preorder_recursive(bst.root))
    print(Traversal.preorder(bst.root))

    print(Traversal.postorder_recursive(bst.root))
    print(Traversal.postorder(bst.root))

    print(Traversal.bfs(bst.root))

    print(Traversal.level_order_bfs(bst.root))
    print(Traversal.level_order_dfs(bst.root))


if __name__ == "__main__":
    sys.exit(main())
