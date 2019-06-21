import pytest

from ...ds.trie import Trie


class TestStack(object):

    def test_trie(self):
        trie = Trie()
        trie.insert('abcd')

        assert trie.search('abcd') is True
        assert trie.search('abc') is False

        assert trie.starts_with('abc') is True
        assert trie.starts_with('abcd') is True
        assert trie.starts_with('a') is True
        assert trie.starts_with('d') is False

        trie.delete_recursive('abcd')
        assert trie.search('abcd') is False
        assert trie.starts_with('ab') is False