import sys
import collections


def check_wiggle(l: list) -> None:
    less = True
    # This is a greedy algorithm
    for i in range(0, len(l)-1):
        if less:
            if l[i] > l[i+1]:
                return False
        else:
            if l[i] < l[i+1]:
                return False

        less = not less

    return True


def heap_sort(l: list) -> None:

    def max_heapify(l: list):

        # from len(l)//2-1 to 0
        # bubble down operation
        for target in range(len(l)//2-1, -1, -1):
            cur = target
            while cur < len(l):
                biggest = cur
                left = 2 * cur + 1
                right = 2 * cur + 2

                # find the biggest
                if left < len(l) and l[left] > l[biggest]:
                    biggest = left

                if right < len(l) and l[right] > l[biggest]:
                    biggest = right

                # stop, do not need to heapify
                if biggest == cur:
                    break

                # continue to heapify
                l[biggest], l[cur] = l[cur], l[biggest]
                cur = biggest

    if len(l) <= 1:
        return

    max_heapify(l)

    # from len(l)-1 to 1
    for last in range(len(l)-1, 0, -1):
        # swap the max to the current last index
        # bubble down operation
        l[0], l[last] = l[last], l[0]
        cur = 0
        while cur < last:
            biggest = cur
            left = cur * 2 + 1
            right = cur * 2 + 2

            if left < last and l[left] > l[biggest]:
                biggest = left

            if right < last and l[right] > l[biggest]:
                biggest = right

            # stop, do not need to heapify
            if biggest == cur:
                break

            # continue to heapify
            l[biggest], l[cur] = l[cur], l[biggest]
            cur = biggest


def wiggle_sort(l: list) -> None:
    """
    nums[0] <= nums[1] >= nums[2] <= nums[3]
    Time Complexity: O(n)
    """
    if len(l) <= 1:
        return

    less = True

    # This is a greedy algorithm
    for i in range(0, len(l)-1):
        if less:
            if l[i] > l[i+1]:
                l[i], l[i+1] = l[i+1], l[i]
        else:
            if l[i] < l[i+1]:
                l[i], l[i+1] = l[i+1], l[i]

        less = not less


def _merge_two_sorted_list(dst: list, *, dst_start: int,
                           left_start: int, left_end: int,
                           right_start: int, right_end: int) -> None:

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


def merge_sort(l: list) -> None:
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


def merge_sort_recursive(l: list) -> None:
    """
    Time  Complexity: O(nlog(n)), T(n) = 2T(n/2) + n
    Sapce Complexity: O(n), extra space for array copy (_merge_two_sorted_list)
    Stable sorting
    """
    def _merge_sort_recursive(l, start, end):

        if start >= end:
            return

        mid = (start + end) // 2

        # print(f'start:{start}, mid:{mid}, end:{end}')

        _merge_sort_recursive(l, start, mid)
        _merge_sort_recursive(l, mid+1, end)

        _merge_two_sorted_list(dst=l, dst_start=start,
                               left_start=start, left_end=mid,
                               right_start=mid+1, right_end=end)

    if len(l) <= 1:
        return

    _merge_sort_recursive(l=l, start=0, end=len(l)-1)


def _merge_two_sorted_list_v2(dst: list, dst_start: int,
                              left_window: list,
                              right_window: list) -> None:

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

    while right_runner < len(right_window):
        dst[merge_runner] = right_window[right_runner]
        right_runner += 1
        merge_runner += 1


def merge_sort_v2(l: list) -> None:
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
            mid = start + window_size
            end = mid + window_size
            if end > len(l):
                end = len(l)

            left_window = l[start:mid]
            right_window = l[mid:end]

            _merge_two_sorted_list_v2(dst=l, dst_start=start,
                                      left_window=left_window,
                                      right_window=right_window)

            start += (2*window_size)  # inner loop

        window_size *= 2  # outer loop


def merge_sort_recursive_v2(l: list) -> None:
    """
    Time  Complexity: O(nlog(n)), T(n) = 2T(n/2) + n
    Sapce Complexity: O(n), extra space for array copy (_merge_two_sorted_list)
    Stable sorting
    """

    if len(l) <= 1:
        return

    mid = len(l)//2

    left_window = l[0:mid]
    right_window = l[mid:len(l)]

    merge_sort_recursive_v2(left_window)
    merge_sort_recursive_v2(right_window)

    _merge_two_sorted_list_v2(dst=l, dst_start=0,
                              left_window=left_window,
                              right_window=right_window)


def _get_partition(l: list, start, end) -> None:
    border = start

    # use median of three to determine pivot can get rid of worst cases
    pivot = end

    # print(f'start:{start}, end:{end}, pivot:{pivot}, l[pivot]:{l[pivot]}, l:{l}')

    # find the border
    for compare in range(start, end):
        if l[compare] <= l[pivot]:
            l[border], l[compare] = l[compare], l[border]
            border += 1

    # switch the pivot to the border
    l[border], l[pivot] = l[pivot], l[border]

    # print(f'border:{border}, l:{l}')

    return border


def quick_sort(l: list) -> None:
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


def quick_sort_recursive(l: list) -> None:
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


def bubble_sort(l: list) -> None:
    """
    Time:  O(n^2)
    Space: O(1)
    """

    if len(l) <= 1:
        return

    # bubble in len(l)-1 to 1
    for bubble in range(len(l)-1, 0, -1):
        is_swap = False
        for compare in range(0, bubble):
            if l[compare] > l[compare + 1]:
                l[compare], l[compare+1] = l[compare+1], l[compare]
                is_swap = True
        if not is_swap:
            break


def bubble_sort_resursive(l: list) -> None:
    """
    Time:  O(n^2)
    Space: O(n)
    """

    def _bubble_sort_resursive(l, bubble):

        if bubble > len(l) - 1:
            return

        _bubble_sort_resursive(l, bubble + 1)

        for compare in range(0, bubble):
            if l[compare] > l[compare + 1]:
                l[compare], l[compare+1] = l[compare+1], l[compare]

    if len(l) <= 1:
        return

    _bubble_sort_resursive(l=l, bubble=1)


def selection_sort(l: list) -> None:
    """
    Time:  O(n^2)
    Space: O(1)
    """
    if len(l) <= 1:
        return

    # from 0 to len - 2
    for select in range(0, len(l)-1):
        minimum = select
        # from select + 1 to len - 1
        for compare in range(select + 1, len(l)):
            if l[compare] < l[minimum]:
                minimum = compare

        if select != minimum:
            l[select], l[minimum] = l[minimum], l[select]


def selection_sort_recursive(l: list) -> None:
    """
    Time:  O(n^2)
    Space: O(n)
    """
    def _selection_sort_recursive(l, select):

        if select < 0:
            return

        _selection_sort_recursive(l, select - 1)

        minimum = select
        for compare in range(select + 1, len(l)):
            if l[compare] < l[minimum]:
                minimum = compare

        if select != minimum:
            l[select], l[minimum] = l[minimum], l[select]

    if len(l) <= 1:
        return

    _selection_sort_recursive(l, select=len(l)-2)


def insertion_sort(l: list) -> None:
    """
    Time:  O(n^2)
    Space: O(1)
    """
    if len(l) <= 1:
        return

    for insert in range(1, len(l)):
        # compare from new-1 to 0
        for compare in range(insert-1, -1, -1):
            if l[compare] <= l[compare + 1]:
                break
            else:
                l[compare], l[compare+1] = l[compare+1], l[compare]


def insertion_sort_recursive(l: list) -> None:
    """
    Time:  O(n^2)
    Space: O(n)
    """

    def _insertion_sort_recursive(l, insert):

        if insert < 1:
            return

        _insertion_sort_recursive(l, insert-1)
        # compare from new-1 to 0
        for compare in range(insert-1, -1, -1):
            if l[compare] <= l[compare + 1]:
                break
            else:
                l[compare], l[compare+1] = l[compare+1], l[compare]

    if len(l) <= 1:
        return

    _insertion_sort_recursive(l, insert=len(l)-1)


def main():
    data = [i for i in range(10, -1, -1)]
    print(data)
    heap_sort(data)
    print(data)


if __name__ == '__main__':
    sys.exit(main())
