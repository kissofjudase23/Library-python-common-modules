import sys


def binary_search(array: list, target) -> int:
    """
    Time  Complexity: O(log(n)), total log(n) round, each round takes O(1)
    Sapce Complexity: O(1)
    return -1 if not found
    """

    start, end = 0, len(array) - 1

    # len is approxmiately equal to 1, n/2^k = 1, k = log(n)
    while start <= end:
        mid = (start + end)//2
        if target == array[mid]:
            return mid
        elif target < array[mid]:
            end = mid - 1
        else:
            start = mid + 1

    return -1


def binary_search_recursive(array: list, target) -> int:
    """
    Time  Complexity: O(log(n)), T(n) = T(n/2) + 1
    Sapce Complexity: O(log(n))
    return -1 if not found
    """
    def _binary_search_recursive(array, start, end, target):
        """
        In order to reuse the same list, we need list pointers start, end
        """

        # out of range
        if start > end:
            return -1

        mid = (start + end)//2

        if target == array[mid]:
            return mid

        elif target < array[mid]:
            return _binary_search_recursive(array, start, mid - 1, target)

        else:  # target > array[mid]
            return _binary_search_recursive(array,  mid + 1, end, target)

    start, end = 0, len(array) - 1
    return _binary_search_recursive(array, start, end, target)


def main():
    sorted_list = [1, 2, 3, 4, 5]

    print(binary_search_recursive(array=sorted_list, target=2))


if __name__ == "__main__":
    sys.exit(main())
