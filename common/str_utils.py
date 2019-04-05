from collections import defaultdict

from .exc import ArgError


class StrUtils(object):

    @classmethod
    def to_str(cls, bytes_or_str):
        """

        :param bytes_or_str:
        :return: unicode string
        """
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode('utf-8')
        else:
            value = bytes_or_str

        return value

    @classmethod
    def to_bytes(cls, bytes_or_str):
        """

        :param bytes_or_str:
        :return: bytes string
        """
        if isinstance(bytes_or_str, str):
            value = bytes_or_str.encode('utf-8')
        else:
            value = bytes_or_str

        return value

    @staticmethod
    def is_unique_char(s, *, case_sensitive=False):
        """ Determine if str has all unique characters

        Complexity:
        Time  : O(n)
        Space : O(C)
        """

        if not s:
            raise ArgError()

        if not case_sensitive:
            s = s.lower()

        m = dict()
        for c in s:
            if not m.get(c, None):
                m[c] = True
                continue
            else:
                # duplicated
                return False

        return True

    @staticmethod
    def is_permutation(s1, s2, *, case_sensitive=False):
        """ Determine if str1 is the permutation of str2

        Complexity:
        Time  : O(n)
        Space : O(c)
        """

        if not s1 or not s2:
            raise ArgError()

        if len(s1) != len(s2):
            return False

        if not case_sensitive:
            s1, s2 = s1.lower(), s2.lower()

        m = defaultdict(int)

        for c in s1:
            m[c] += 1

        for c in s2:
            m[c] -= 1
            if m[c] < 0:
                return False

        return True

    @staticmethod
    def replace_spaces(s, *, pattern="%20"):
        """ In fact, s.replace(" ", %20) can solve this issue

        Complexity:
            Time  : O(n)
            Space : O(n)
        """

        if not s:
            raise ArgError()

        buf = list()

        for c in s:
            if c == " ":
                buf.append(pattern)
            else:
                buf.append(c)

        return "".join(buf)

    @staticmethod
    def is_palindrome(s):
        """ Determine if s is a palindrome

        Complexity:
            Time  : O(n)
            Space : O(n)
        """
        if not s:
            raise ArgError()

        if len(s) is 1:
            return True

        start, end = 0, len(s)-1

        while start < end:
            if s[start] == s[end]:
                start += 1
                end -= 1
            else:
                return False

        return True

    @staticmethod
    def is_palindrome_permutation(s):
        """ Determine if s is a palindrome permutation

        Complexity:
            Time  : O(n)
            Space : O(n)
        """
        if not s:
            raise ArgError()

        if len(s) is 1:
            return True

        odd_cnt = 0
        m = defaultdict(int)
        for c in s:
            m[c] += 1
            if m[c] % 2 is 0:
                odd_cnt -= 1
            else:
                odd_cnt += 1

        return odd_cnt <= 1
