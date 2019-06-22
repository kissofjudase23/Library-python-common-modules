import sys
import collections


class Node(object):

    def __init__(self):
        self.children = dict()
        self.end_of_word = False


class Trie(object):

    def __init__(self):
        self.root = Node()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        Time: O(len(word))
        """
        current = self.root
        for c in word:
            child = current.children.get(c)
            if not child:
                child = Node()
                current.children[c] = child
            current = child

        current.end_of_word = True

    def insert_recursive(self, word: str) -> None:
        """
        Inserts a word into the trie.
        Time: O(len(word))
        Space: O(len(word))
        """

        def _inser_recursive(current, word, *, index):
            if index == len(word):
                current.end_of_word = True
                return

            c = word[index]
            child = current.children.get(c)
            if not child:
                child = Node()
                current.children[c] = child
            _inser_recursive(child, word, index+1)

        _inser_recursive(self.root, word, index=0)

    def _search(self, word: str, *, is_prefix: bool) -> bool:
        current = self.root
        for c in word:
            child = current.children.get(c)
            if not child:
                return False
            current = child

        if is_prefix:
            return True

        if current.end_of_word:
            return True

        return False

    def search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        Time: O(len(word))
        """
        return self._search(word=word, is_prefix=False)

    def starts_with(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        Time: O(len(word))
        """
        return self._search(word=prefix, is_prefix=True)

    def search_recursive(self, word: str) -> bool:
        """
        Time: O(len(word))
        Space: O(len(word))
        """
        def _search_recursive(current, word, *, index):
            if index == len(word):
                return current.end_of_word

            c = word[index]
            child = current.children.get(c)
            if not child:
                return False
            return search_recursive(child, word, index+1)

        return _search_recursive(self.root, word, index=0)

    def delete(self, word: str) -> None:
        """
        Time: O(len(word))
        Space: O(len(word)) <-- stack len
        """
        stack = list()
        current = self.root
        Pair = collections.namedtuple('Pair', ['parent', 'child_c'])

        for c in word:
            # push the node in the reverse order
            stack.append(Pair(parent=current, child_c=c))
            # can not find the character of the word
            child = current.children.get(c)
            if not child:
                return
            current = child

        # delete the node only when current.end_of_word is True
        if not current.end_of_word:
            return
        current.end_of_word = False
        # delete the node only when there is no children
        should_delete_child = not len(current.children)

        while should_delete_child and len(stack):
            pair = stack.pop()
            parent, child_c = pair.parent, pair.child_c
            parent.childrent.pop(child_c)
            # delete the node only when there is no children
            should_delete_child = not len(parent)

    def delete_recursive(self, word: str) -> None:
        """
        Time: O(len(word))
        Space: O(len(word))
        """
        def _delete(current, word, *, index) -> bool:
            """
            Return:
                True : Remove this node from parent dict
            """
            # find the word
            if index == len(word):
                # delete the node only when current.end_of_word is True
                if not current.end_of_word:
                    return False

                current.end_of_word = False
                # delete the node only when there is no children
                return not len(current.children)

            c = word[index]
            child = current.children.get(c)
            # can not find the character of the word
            if not child:
                return False

            should_delete_child = _delete(child, word, index=index+1)
            if not should_delete_child:
                return False

            # remove the child reference
            current.children.pop(c)
            return not len(current.children)

        _delete(self.root, word, index=0)


def main():
    trie = Trie()
    trie.insert("abc")

    print(trie.search("abc"))
    print(trie.search("ab"))

    print(trie.starts_with("a"))
    print(trie.starts_with("ab"))
    print(trie.starts_with("abc"))

    trie.delete_recursive("abc")
    print(trie.search("abc"))
    print(trie.starts_with("ab"))


if __name__ == "__main__":
    sys.exit(main())
