import pytest

from ...ds.trie import Trie


class TestStack(object):

    def test_search_starts_with(self):
        trie = Trie()
        trie.insert('abcd')

        assert trie.search('abcd') is True
        assert trie.search('abc') is False

        assert trie.starts_with('abc') is True
        assert trie.starts_with('abcd') is True
        assert trie.starts_with('a') is True
        assert trie.starts_with('d') is False

    def test_delete(self):
        trie = Trie()

        trie.insert('abc')
        trie.insert('abcd')

        assert trie.search('abc') is True
        assert trie.search('abcd') is True

        trie.delete('abc')
        assert trie.search('abc') is False
        assert trie.search('abcd') is True

    def test_delete_recursive(self):
        trie = Trie()

        trie.insert('abc')
        trie.insert('abcd')

        assert trie.search('abc') is True
        assert trie.search('abcd') is True

        trie.delete_recursive('abc')
        assert trie.search('abc') is False
        assert trie.search('abcd') is True