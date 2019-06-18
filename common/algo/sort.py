import sys
import collections


def _merge_two_sorted_list(dst, *, dst_start,
                           left_start, left_end,
                           right_start, right_end):

    left_window = dst[left_start:left_end + 1]        # start -> mid
    right_window = dst[right_start:right_end + 1]     # mid + 1 -> end

    merge_runner = dst_start
    left_runner = right_runner = 0

    while left_runner < len(left_window) and right_runner < len(right_window):
        if left_window[left_runner] <= right_window[right_runner]:
            dst[merge_runner] = left_window[left_runner]
            left_runner += 1
        else:
            dst[merge_runner] = right_window[right_runner]
            right_runner += 1
        merge_runner += 1

    while left_runner < len(left_window):
        dst[merge_runner] = left_window[left_runner]
        left_runner += 1
        merge_runner += 1

    # do not need to traverse the rest end window, since it is already in dst
    while right_runner < len(right_window):
        dst[merge_runner] = right_window[right_runner]
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
    while window_size <= (len(l) - 1):
        # windows_size:1, start:[0, 2, 4, 6, 8]
        # windows_size:2, start:[0, 4, 8]
        # windows_size:4: start:[0, 8]
        start = 0
        while (start + window_size) < len(l):
            """
            Python slice can help to handle out of range issues
            for example:
                l = [1, 2 ,3]
                l[1:100] = [2, 3]
                l[100:] = []
                l[100:10] = []
            So the code from line59 to line66 can be refactored as following
            mid = start + windows_size   # do not need to check range
            end = mid + windows_size  # do not need to check range
            left_window = l[start:mid]
            right_window = l[mid:end]
            """
            mid = start + window_size - 1
            end = start + 2*window_size - 1
            if end > (len(l) - 1):
                end = (len(l) - 1)

            _merge_two_sorted_list(dst=l, dst_start=start,
                                   left_start=start, left_end=mid,
                                   right_start=mid+1, right_end=end)

            start += (2*window_size)  # inner loop

        window_size *= 2  # outer loop


def merge_sort_recursive(l):
    """
    Time  Complexity: O(nlog(n)), T(n) = 2T(n/2) + n
    Sapce Complexity: O(n), extra space for array copy (_merge_two_sorted_list)
    Stable sorting
    """
    def _merge_sort_recursive(l, start, end):

        if start >= end:
            return

        mid = (start + end) // 2

        print(f'start:{start}, mid:{mid}, end:{end}')

        _merge_sort_recursive(l, start, mid)
        _merge_sort_recursive(l, mid+1, end)

        _merge_two_sorted_list(dst=l, dst_start=start,
                               left_start=start, left_end=mid,
                               right_start=mid+1, right_end=end)

    if len(l) <= 1:
        return

    _merge_sort_recursive(l, 0, len(l)-1)


def _get_partition(l, start, end):
    border = start

    # use median of three to determine pivot can get rid of worst cases
    pivot = end

    # print(f'start:{start}, end:{end}, pivot:{pivot}, l[pivot]:{l[pivot]}, l:{l}')

    # find the border
    for runner in range(start, end):
        if l[runner] <= l[pivot]:
            l[border], l[runner] = l[runner], l[border]
            border += 1

    # switch the pivot to the border
    l[border], l[pivot] = l[pivot], l[border]

    # print(f'border:{border}, l:{l}')

    return border


def quick_sort(l):
    """
    Time Complexity: O(nlog(n))
    Sapce Complexity: O(1)
    Ref:
    1. https://www.techiedelight.com/iterative-implementation-of-quicksort/
    2. https://stackoverflow.com/questions/39666714/quick-sort-implement-by-queue
    """

    if len(l) <= 1:
        return

    start = 0
    end = len(l) - 1
    stack = list()

    Pair = collections.namedtuple('Pair', ['start', 'end'])

    # The first pirt
    stack.append(Pair(start=start, end=end))

    while len(stack):
        pair = stack.pop()
        start, end = pair.start, pair.end

        pivot = _get_partition(l, start, end)

        # start partition
        if start < pivot - 1:
            stack.append(Pair(start=start, end=pivot-1))

        # end partition
        if pivot + 1 < end:
            stack.append(Pair(start=pivot + 1, end=end))


def quick_sort_recursive(l):
    """
    Time Complexity:  O(nlog(n))
    Sapce Complexity: O(log(n)) ~ O(n)
    Ref:
    1. https://www.geeksforgeeks.org/python-program-for-quicksort/
    2. https://www.youtube.com/watch?v=CB_NCoxzQnk
    """
    def _quick_sort_recursive(l, start, end):

        if start >= end:
            return

        pivot = _get_partition(l, start, end)
        # start part
        _quick_sort_recursive(l, start, pivot-1)
        # end part
        _quick_sort_recursive(l, pivot+1, end)

    if len(l) <= 1:
        return

    _quick_sort_recursive(l=l, start=0, end=len(l) - 1)


def main():
    data = [3, 2, 1, 0]
    merge_sort_recursive(data)
    print(data)


if __name__ == '__main__':
    sys.exit(main())
