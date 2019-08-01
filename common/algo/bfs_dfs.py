import sys

import collections
from pprint import pprint as pp
from typing import List


class NumberOfIsland(object):
    """
    https://leetcode.com/problems/number-of-islands/
    """

    LAND, WATER = '1', '0'
    NEIGHBORS = ((1, 0), (0, -1), (-1, 0), (0, 1))

    @classmethod
    def bfs(cls, grid: List[List[str]]) -> int:
        """
        Time: O(m*n)
        Space: O(m*n)
        """
        def traverse_grid(r, c):
            if grid[r][c] == cls.WATER or memo[r][c]:
                return 0

            memo[r][c] = True
            q = collections.deque()
            q.append((r, c))
            while q:
                r, c = q.popleft()
                for neigbor in cls.NEIGHBORS:
                    nr, nc = r+neigbor[0], c+neigbor[1]
                    # out of boundary
                    if nr < 0 or nr >= row or nc < 0 or nc >= col:
                        continue

                    if grid[nr][nc] == cls.WATER or memo[nr][nc]:
                        continue

                    memo[nr][nc] = True
                    q.append((nr, nc))

            return 1

        if not grid or not grid[0]:
                return 0

        row, col = len(grid), len(grid[0])
        area_cnt = 0
        memo = [[False for _ in range(col)] for _ in range(row)]

        for r in range(row):
            for c in range(col):
                area_cnt += traverse_grid(r, c)

        return area_cnt

    @classmethod
    def dfs(cls, grid: List[List[str]]) -> int:
        """
        Time: O(m*n)
        Space: O(m*n)
        """
        def _dfs(r, c):
            if grid[r][c] == cls.WATER or memo[r][c]:
                return 0

            memo[r][c] = True

            for neigbor in cls.NEIGHBORS:
                nr, nc = r+neigbor[0], c+neigbor[1]
                # out of boundary
                if nr < 0 or nr >= row or nc < 0 or nc >= col:
                    continue
                if grid[nr][nc] == cls.WATER or memo[nr][nc]:
                    continue

                _dfs(nr, nc)

            return 1

        if not grid or not grid[0]:
            return 0

        row, col = len(grid), len(grid[0])
        area_cnt = 0
        memo = [[False for _ in range(col)] for _ in range(row)]

        for r in range(row):
            for c in range(col):
                area_cnt += _dfs(r, c)

        return area_cnt


def main():
    grid2 = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]
    print(NumberOfIsland.bfs(grid2))
    print(NumberOfIsland.dfs(grid2))


if __name__ == '__main__':
    sys.exit(main())
