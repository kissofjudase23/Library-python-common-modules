import sys
from pprint import pprint as pp
from typing import List


def permute_rec(nums: List[int]) -> List[List[int]]:
    """
    Time:  O(n!)
        n * (n-1) * (n-2) * ... 3 * 2 * 1
    Space: O(n!)
        total n! permutation
    """
    perms = []

    def _permute(nums, start):
        if start == (len(nums)-1):
            perms.append(nums[:])
            return

        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            _permute(nums, start+1)
            nums[start], nums[i] = nums[i], nums[start]

    if not nums:
        return perms

    _permute(nums, 0)
    return perms


def permute_iter(nums: List[int]) -> List[List[int]]:
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
    subs = []

    def _subsets(nums, path, start):
        # make a copy
        subs.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            # !!! not start + 1 here
            _subsets(nums, path, i+1)
            path.pop()

    if not nums:
        return subs

    path = []
    _subsets(nums, path, 0)
    return subs


def subsets_iter(nums: List[int]) -> List[List[int]]:
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
    subs = []
    subs_len = 2 ** len(nums)

    for sub_idx in range(subs_len):
        new_sub = []

        for num_idx in range(len(nums)):
            if sub_idx & (1 << num_idx):
                new_sub.append(nums[num_idx])

        subs.append(new_sub)

    return subs


def main():
    pp(subsets_iter_bit(['1', '2', '3']))


if __name__ == "__main__":
    sys.exit(main())
