import sys
from pprint import pprint as pp
from typing import List


def permutation_rec(nums: List[int]) -> List[List[int]]:
    """
    Time:  O(n!)
        n * (n-1) * (n-2) * ... 3 * 2 * 1
    Space: O(n!)
        total n! permutation
    """
    perms = []

    def _permutation(start):
        if start == len(nums)-1:
            perms.append(nums[:])
            return

        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            _permutation(start=start+1)
            nums[start], nums[i] = nums[i], nums[start]

    if not nums:
        return perms

    _permutation(start=0)
    return perms


def permutation_iter(nums: List[int]) -> List[List[int]]:
    """
    Time:  O(n!)
        1 * 2 * 3 * ... * (n-2) * (n-1) * n
    Space: O(n!)
        total n! permutation
    """
    if not nums:
        return [[]]

    perms = [[nums[0]]]

    for i in range(1, len(nums)):
        new_perms = []
        for perm in perms:
            # n + 1 position for each perm
            for b in range(len(perm)+1):
                new_perms.append(perm[:b]+[nums[i]]+perm[b:])

        perms = new_perms

    return perms


def subsets_rec(nums: List[int]) -> List[List[int]]:
    """
    DFS Traverse
    []
    [1], [1,2], [1,2,3], [1,3]
    [2], [2,3]
    [3]
    Time: O(n*2^n)
        total 2^n subset, each subset need O(n) to copy
    Space: O(2^n)
        total 2^n subset
    """
    def _subsets(cur: list, start):
        # make a copy
        subs.append(cur[:])

        if start == len(nums):
            return

        for i in range(start, len(nums)):
            cur.append(nums[i])
            # !!! start = i =1 rather than start + 1
            _subsets(cur, start=i+1)
            cur.pop()

    subs = []
    cur = []
    if not nums:
        return []
    _subsets(cur, 0)
    return subs


def subsets_iter(nums: List[int]) -> List[List[int]]:
    """
    s1: [[]]
    s2: [[], [a]]
    s3: [[], [a], [b], [a, b]]
    s4: [[], [a], [b], [a, b], [c], [a, c], [b, c], [a, b, c]]
    Time: O(n*2^n)
        total 1 + 2 + 4 + 8 ... 2^(n-1): 2^n operation
        each operation needs O(n) time to copy list
    Space: O(2^n)
        O(2^n) subsets
    """
    subs = [[]]

    for num in nums:
        subs_len = len(subs)
        for i in range(subs_len):
            # copy without num
            subs.append(subs[i].copy())
            # with num
            subs[i].append(num)

    return subs


def subsets_iter_bit(nums: List[int]) -> List[List[int]]:
    """
    use [a, b, c] as example:
    000: []
    001: [a]
    010: [b]
    011: [a, b]
    100: [c]
    101: [a, c]
    110: [a, b]
    111: [a, b, c]
    Time: O(n*2^n)
        total 2^n subsets, and each subset needs O(n) time to populate elements
    Space: O(2^n)
        2 ** len(nums) = O(2^n) subsets
    """
    subs = []
    subs_len = 2 ** len(nums)

    for sub_idx in range(subs_len):
        new_sub = []

        for num_idx in range(len(nums)):
            # populate elements
            if sub_idx & (1 << num_idx):
                new_sub.append(nums[num_idx])

        subs.append(new_sub)

    return subs


def combination_rec(n: int, k: int) -> List[List[int]]:
    """
    DFS Traverse
    Time: O(k* n!/(n!*(n-k)!))
    Space: O(n!/(n!*(n-k)!))
    """
    def _combination(cur: list, start):
        if len(cur) == k:
            comb.append(cur[:])
            return

        # skip the cases that can not satisfy k == len(cur) in the future
        if k - len(cur) > n - start + 1:  # included start
            return

        # from start to n
        for i in range(start, n+1):
            cur.append(i)
            _combination(cur=cur, start=i+1)
            cur.pop()

    comb = []
    cur = []
    if k > n:
        return comb
    _combination(cur=cur, start=1)
    return comb


def combin_iter(n: int, k: int) -> List[List[int]]:
    """
    Ref:
    https://leetcode.com/problems/combinations/discuss/26992/Short-Iterative-C%2B%2B-Answer-8ms
    """
    comb = []
    cur = [0 for _ in range(k)]
    i = 0

    while i >= 0:
        cur[i] += 1
        if cur[i] > n:
            i -= 1
        elif i == k - 1:
            comb.append(cur[:])
        else:
            i += 1
            cur[i] = cur[i-1]

    return comb


def combin_iter_v2(n: int, k: int) -> List[List[int]]:
    """
    Ref: https://leetcode.com/problems/combinations/discuss/27029/AC-Python-backtracking-iterative-solution-60-ms
    Time: O(k* n!/(n!*(n-k)!))
    Space: O(n!/(n!*(n-k)!))   (extrac space O(k))
    """
    comb = []
    cur = []
    start = 1

    while True:
        l = len(cur)

        if l == k:
            comb.append(cur[:])

        # k - l > n - start + 1 means that l will not satisfy k in the future
        # in fact, (k - l) > (n - start + 1)  can cover start > n when (l-k) = -1
        if l == k or (k - l) > (n - start + 1) or start > n:
            if not cur:
                break
            start = cur.pop() + 1

        else:
            cur.append(start)
            start += 1

    return comb


def main():
    pp(combin_iter_v2(4, 3))


if __name__ == "__main__":
    sys.exit(main())
