import sys


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

    def delete_recursive(self, word: str) -> None:

        def _delete(current, word, *, index) -> bool:
            """
            Return:
                True : Remove this node from parent dict
            """
            if index == len(word):
                return current.end_of_word

            c = word[index]
            child = current.children.get(c)
            if not child:
                return False

            should_delete_child = _delete(child, word, index=index+1)

            if should_delete_child:
                current.children.pop(c)
                return len(current.children) == 0

            return False

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
