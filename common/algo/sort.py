import sys


def _merge_two_sorted_list(left, right, dst, *, dst_start=0):

    merge_runner = dst_start
    left_runner = right_runner = 0

    # print(f'left:{left}, right:{right}')

    while left_runner < len(left) and right_runner < len(right):
        if left[left_runner] < right[right_runner]:
            dst[merge_runner] = left[left_runner]
            left_runner += 1
        else:
            dst[merge_runner] = right[right_runner]
            right_runner += 1
        merge_runner += 1

    while left_runner < len(left):
        dst[merge_runner] = left[left_runner]
        left_runner += 1
        merge_runner += 1

    while right_runner < len(right):
        dst[merge_runner] = right[right_runner]
        right_runner += 1
        merge_runner += 1


def merge_sort(l):
    """
    Time Complexity: O(nlog(n))
        log(n) round (window size),
        n in each round (merge sorted lists) => total nlong(n)
    Sapce Complexity: O(n), extra space to array copy
    Stable sorting
    """

    window_size = 1

    # windows_size: [1, 2 ,4 ,8 ,16 ...] which means the sorted list unit
    while window_size < len(l):
        # windows_size:1, left:[0, 2, 4, 6, 8]
        # windows_size:2, left:[0, 4, 8]
        # windows_size:4: left:[0, 8]
        left = 0
        while left < len(l) - 1:
            """
            Python slice can help to handle out of range issues
            for example:
                l = [1, 2 ,3]
                l[1:100] = [2, 3]
                l[100:] = []
                l[100:10] = []
            So the code from line59 to line66 can be refactored as following
            mid = left + windows_size   # do not need to check range
            right = mid + windows_size  # do not need to check range
            left_window = l[left:mid]
            right_window = l[mid:right]
            """
            mid = left + window_size
            if mid > len(l):  # example: [9, 8, 7, 6, 5, 4, 3 ,2 ,1]
                break
            right = mid + window_size
            if right > len(l):
                right = len(l)
            left_window = l[left:mid]
            right_window = l[mid:right]

            # print(f'w:{windows_size}, left:{left}, mid:{mid}, right:{right}')
            _merge_two_sorted_list(left=left_window,
                                   right=right_window,
                                   dst=l,
                                   dst_start=left)

            left += (2*window_size)  # inner loop

        window_size *= 2  # outer loop


def merge_sort_recursive(l):
    """
    Time  Complexity: O(nlog(n)), T(n) = 2T(n/2) + n
    Sapce Complexity: O(n), extra space to array copy
    Stable sorting
    """
    if len(l) <= 1:
        return

    # use double slash for integer division
    mid = len(l)//2

    # print(f'l:{l}, mid:{mid}')

    # slice is a copy in python
    left = l[:mid]
    right = l[mid:]

    merge_sort_recursive(left)
    merge_sort_recursive(right)

    _merge_two_sorted_list(left=left, right=right, dst=l)


def quick_sort_recursive(l):

    def _get_partition(l, start, end):
        border = start

        # use median of three to determine pivot can get rid of worst cases
        pivot = end

        # print(f'start:{start}, end:{end}, pivot:{pivot}, l[pivot]:{l[pivot]}, l:{l}')

        for runner in range(start, end):
            if l[runner] <= l[pivot]:
                l[border], l[runner] = l[runner], l[border]
                border += 1

        l[border], l[pivot] = l[pivot], l[border]

        # print(f'border:{border}, l:{l}')

        return border

    def _quick_sort_recursive(l, start, end):

        if start >= end:
            return

        pivot = _get_partition(l, start, end)
        # left part
        _quick_sort_recursive(l, start, pivot-1)
        # right part
        _quick_sort_recursive(l, pivot+1, end)

    if len(l) <= 1:
        return

    _quick_sort_recursive(l=l, start=0, end=len(l) - 1)


def main():
    data = [0, 1, 2]
    merge_sort_recursive(data)
    print(data)


if __name__ == '__main__':
    sys.exit(main())
