import collections
from pprint import pprint as pp

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

        m = collections.defaultdict(int)

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
        m = collections.defaultdict(int)
        for c in s:
            m[c] += 1
            if m[c] % 2 is 0:
                odd_cnt -= 1
            else:
                odd_cnt += 1

        return odd_cnt <= 1

    @staticmethod
    def get_lps(pattern):
        # init lps array
        lps = [None] * len(pattern)
        lps[0] = 0

        p = 0  # prefix pointer
        s = 1  # suffix pointer

        while s < len(pattern):
            if pattern[s] == pattern[p]:
                p += 1
                lps[s] = p  # update suffix length
                s += 1
            else:
                if p != 0:
                    # backward the prefix pointer to the position
                    # after the matched prefix/suffix string
                    p = lps[p-1]
                else:
                    # do not match anything
                    lps[s] = 0
                    s += 1
        return lps

    @staticmethod
    def is_substring(s, pattern):
        """ Use KMP algorithm
        Time:  O(m+n), where m is length of s and n is the length os pattern.
        Space: O(n)
        Reference:
        https://www.youtube.com/watch?v=GTJr8OvyEVQ
        http://jakeboxer.com/blog/2009/12/13/the-knuth-morris-pratt-algorithm-in-my-own-words/
        """
        if not pattern or len(pattern) == 0:
            return 0

        lps = StrUtils.get_lps(pattern)
        i = j = 0
        res = -1

        while i < len(s):
            if s[i] == pattern[j]:
                i += 1
                j += 1
                if j == len(pattern):
                    res = i - j
                    break
            else:
                if j != 0:
                    # backward the prefix pointer to the position
                    # after the matched prefix/suffix string
                    j = lps[j-1]
                else:
                    # do not match anything
                    i += 1
        return res

    @staticmethod
    def traverse_lcs_memo(s1, s1_idx, s2, s2_idx, memo):
        """ traverse the memo array to find lcs
        """
        lcs_len = memo[s1_idx][s2_idx]
        lcs = [None] * lcs_len
        i, j = s1_idx, s2_idx

        while lcs_len:
            if s1[i] == s2[j]:
                lcs_len -= 1
                lcs[lcs_len] = s1[i]
                i -= 1
                j -= 1
            else:
                if memo[i][j] == memo[i-1][j]:
                    i -= 1
                else:  # memo[i][j] == memo[i][j-1]
                    j -= 1

        return "".join(lcs)

    @staticmethod
    def lcs(s1, s2):
        """
        Longest common sequence
        Time: O(n^2), Space: O(n^2)
        Ref: https://www.youtube.com/watch?v=NnD96abizww
        """
        if not s1 or not s2:
            return ""

        l1, l2 = len(s1), len(s2)

        memo = [[0 for _ in range(l2)] for _ in range(l1)]

        if s1[0] == s2[0]:
            memo[0][0] = 1

        # init first row
        for j in range(1, l2):
            if memo[0][j-1] or s2[j] == s1[0]:
                memo[0][j] = 1

        # init first column
        for i in range(1, l1):
            if memo[i-1][0] or s1[i] == s2[0]:
                memo[i][0] = 1

        # complete the memo
        for i in range(1, l1):
            for j in range(1, l2):
                if s1[i] == s2[j]:
                    memo[i][j] = memo[i-1][j-1] + 1
                else:
                    memo[i][j] = max(memo[i-1][j], memo[i][j-1])

        return StrUtils.traverse_lcs_memo(s1, l1-1,
                                          s2, l2-1,
                                          memo)


if __name__ == "__main__":
    pass
