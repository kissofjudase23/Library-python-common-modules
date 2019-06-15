import sys


def binary_search(l, target):
    """
    Time  Complexity: O(logn)
    Sapce Complexity: O(1)
    return -1 if not found
    """

    start, end = 0, len(l) - 1

    while start <= end:
        mid = (start + end)//2
        if target == l[mid]:
            return mid
        elif target < l[mid]:
            end = mid - 1
        else:
            start = mid + 1

    return -1


def binary_search_recursive(l, target):
    """
    Time  Complexity: O(logn)
    Sapce Complexity: O(logn)
    return -1 if not found
    """
    def _binary_search_recursive(l, start, end, target):

        # out of range
        if start > end:
            return -1

        mid = (start + end)//2

        if target == l[mid]:
            return mid

        elif target < l[mid]:
            return _binary_search_recursive(l, start, mid - 1, target)

        else:  # target > l[mid]
            return _binary_search_recursive(l,  mid + 1, end, target)

    start, end = 0, len(l) - 1
    return _binary_search_recursive(l, start, end, target)


def main():
    sorted_list = [1, 2, 3, 4, 5]

    print(binary_search_recursive(l=sorted_list, target=2))


if __name__ == "__main__":
    sys.exit(main())
