# -*- coding: utf-8 -*-

import pytest

from ..exc import ArgError
from ..str_utils import StrUtils


class TestEncodeFormatter(object):

    @pytest.mark.parametrize('str_, assert_str', [
        pytest.param('utf8_str', 'utf8_str'),
        pytest.param(b'bytes_str', 'bytes_str')
    ])
    def test_to_utf8_str(self, str_, assert_str):

        utf8_str = StrUtils.to_str(str_)

        assert isinstance(utf8_str, str)
        assert utf8_str == assert_str

    @pytest.mark.parametrize('str_, assert_str', [
        pytest.param('utf8_str', b'utf8_str'),
        pytest.param(b'bytes_str', b'bytes_str')
    ])
    def test_to_bytes_str(self, str_, assert_str):
        bytes_str = StrUtils.to_bytes(str_)

        assert isinstance(bytes_str, bytes)
        assert bytes_str == assert_str

    @pytest.mark.parametrize('s, expected', [
        pytest.param('abcdefg', True),
        pytest.param('aa', False),
        pytest.param('aA', False),
        pytest.param('bcdefgaa', False),
    ])
    def test_is_unique_char(self, s, expected):
        actual = StrUtils.is_unique_char(s)
        assert actual is expected

    @pytest.mark.parametrize('s, expected', [
        pytest.param('aa', False),
        pytest.param('aA', True),
    ])
    def test_is_unique_case_sensitive_char(self, s, expected):
        actual = StrUtils.is_unique_char(s, case_sensitive=True)
        assert actual is expected

    @pytest.mark.parametrize('s', [
        pytest.param(None),
        pytest.param(""),
    ])
    def test_is_unique_char_raise(self, s):
        with pytest.raises(ArgError):
            StrUtils.is_unique_char(s)

    @pytest.mark.parametrize('s1, s2, expected', [
        pytest.param('abcde', 'edcba', True),
        pytest.param('abcde', 'aaaaa', False),
        pytest.param('ab', 'AB', True)
    ])
    def test_check_permutation(self, s1, s2, expected):
        actual = StrUtils.is_permutation(s1, s2)
        assert actual is expected

    @pytest.mark.parametrize('s1, s2', [
        pytest.param(None, "abc"),
        pytest.param(None, ""),
        pytest.param("abc", None),
        pytest.param("", None),
        pytest.param(None, None),
        pytest.param("", "")
    ])
    def test_check_permutation_raise(self, s1, s2):
        with pytest.raises(ArgError):
            StrUtils.is_permutation(s1, s2)

    @pytest.mark.parametrize('s, expected', [
        pytest.param('abc', 'abc'),
        pytest.param(' a c ', '%20a%20c%20'),
        pytest.param('   ', '%20%20%20'),
    ])
    def test_is_unique_char(self, s, expected):
        actual = StrUtils.replace_spaces(s, pattern='%20')
        assert actual == expected

    @pytest.mark.parametrize('s, expected', [
        pytest.param('abcba', True),
        pytest.param('aaaaa', True),
        pytest.param('a', True),
        pytest.param('aa', True),
        pytest.param('aabbccdddccbbaa', True),
        pytest.param('abc', False)
    ])
    def test_is_palindrome(self, s, expected):
        actual = StrUtils.is_palindrome(s)
        assert actual is expected

    @pytest.mark.parametrize('s, expected', [
        pytest.param('abcba', True),
        pytest.param('a', True),
        pytest.param('aa', True),
        pytest.param('aabbccddeeff', True),
        pytest.param('aabbccddeeffg', True),
        pytest.param('abca', False)
    ])
    def test_is_palindrome_permutation(self, s, expected):
        actual = StrUtils.is_palindrome_permutation(s)
        assert actual is expected

    @pytest.mark.parametrize('s, pattern, expected', [
        pytest.param('aaaaaaaaaaab', 'aaaaab', 6),
        pytest.param('aaab', 'aaab', 0),
        pytest.param('aaab', 'aaac', -1),
        pytest.param('aaab', '', 0),
        pytest.param('aaab', None, 0)
    ])
    def test_substring(self, s, pattern, expected):
        actual = StrUtils.is_substring(s, pattern)
        assert actual == expected

    @pytest.mark.parametrize('s1, s2, expected', [
        pytest.param('aaaa', 'aaaa', 'aaaa'),
        pytest.param('acbcf', 'abcdaf', 'abcf')
    ])
    def test_lcs(self, s1, s2, expected):
        actual = StrUtils.lcs(s1, s2)
        assert actual == expected
