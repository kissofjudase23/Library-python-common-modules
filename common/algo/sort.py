import sys
import collections


def check_wiggle(array: list) -> None:
    less = True
    # This is a greedy algorithm
    for i in range(0, len(array)-1):
        if less:
            if array[i] > array[i+1]:
                return False
        else:
            if array[i] < array[i+1]:
                return False

        less = not less

    return True


def heap_sort(array: list) -> None:

    def max_heapify(array: list, cur, boundary):
        # bubble down operation
        while cur < boundary:
            biggest = cur
            left = 2 * cur + 1
            right = 2 * cur + 2

            # find the biggest
            if left < boundary and array[left] > array[biggest]:
                biggest = left

            if right < boundary and array[right] > array[biggest]:
                biggest = right

            # stop, do not need to heapify
            if biggest == cur:
                break

            # continue to heapify
            array[biggest], array[cur] = array[cur], array[biggest]
            cur = biggest

    if len(array) <= 1:
        return

    # bottom up heapify from len(array)//2-1 to 0 (skip the nodes on last level)
    for target in range(len(array)//2-1, -1, -1):
        max_heapify(array=array, cur=target, boundary=len(array))

    # from len(array)-1 to 1
    for boundary in range(len(array)-1, 0, -1):
        # swap the max to the current last index
        array[0], array[boundary] = array[boundary], array[0]
        # heapify
        max_heapify(array=array, cur=0, boundary=boundary)


def wiggle_sort(array: list) -> None:
    """
    nums[0] <= nums[1] >= nums[2] <= nums[3]
    Time Complexity: O(n)
    """
    if len(array) <= 1:
        return

    less = True

    # This is a greedy algorithm
    for i in range(0, len(array)-1):
        if less:
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
        else:
            if array[i] < array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]

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


def merge_sort(array: list) -> None:
    """
    Time Complexity: O(nlog(n))
        log(n) round (window size),
        n in each round (merge sorted lists) => total nlong(n)
    Sapce Complexity: O(n), extra space to array copy
    Stable sorting
    """

    window_size = 1

    # windows_size: [1, 2 ,4 ,8 ,16 ...] which means the sorted list unit
    while window_size <= (len(array) - 1):
        # windows_size:1, start:[0, 2, 4, 6, 8]
        # windows_size:2, start:[0, 4, 8]
        # windows_size:4: start:[0, 8]
        start = 0
        while (start + window_size) < len(array):
            """
            Python slice can help to handle out of range issues
            for example:
                array = [1, 2 ,3]
                array[1:100] = [2, 3]
                array[100:] = []
                array[100:10] = []
            So the code from line59 to line66 can be refactored as following
            mid = start + windows_size   # do not need to check range
            end = mid + windows_size  # do not need to check range
            left_window = array[start:mid]
            right_window = array[mid:end]
            """
            mid = start + window_size - 1
            end = start + 2*window_size - 1
            if end > (len(array) - 1):
                end = (len(array) - 1)

            _merge_two_sorted_list(dst=array, dst_start=start,
                                   left_start=start, left_end=mid,
                                   right_start=mid+1, right_end=end)

            start += (2*window_size)  # inner loop

        window_size *= 2  # outer loop


def merge_sort_recursive(array: list) -> None:
    """
    Time  Complexity: O(nlog(n)), T(n) = 2T(n/2) + n
    Sapce Complexity: O(n), extra space for array copy (_merge_two_sorted_list)
    Stable sorting
    """
    def _merge_sort_recursive(array, start, end):

        if start >= end:
            return

        mid = (start + end) // 2

        # print(f'start:{start}, mid:{mid}, end:{end}')

        _merge_sort_recursive(array, start, mid)
        _merge_sort_recursive(array, mid+1, end)

        _merge_two_sorted_list(dst=array, dst_start=start,
                               left_start=start, left_end=mid,
                               right_start=mid+1, right_end=end)

    if len(array) <= 1:
        return

    _merge_sort_recursive(array=array, start=0, end=len(array)-1)


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

    # right window already in dst


def merge_sort_v2(array: list) -> None:
    """
    Time Complexity: O(nlog(n))
        log(n) round (window size),
        n in each round (merge sorted lists) => total nlong(n)
    Sapce Complexity: O(n), extra space to array copy
    Stable sorting
    """

    window_size = 1

    # windows_size: [1, 2 ,4 ,8 ,16 ...] which means the sorted list unit
    while window_size <= (len(array) - 1):
        # windows_size:1, start:[0, 2, 4, 6, 8]
        # windows_size:2, start:[0, 4, 8]
        # windows_size:4: start:[0, 8]
        start = 0
        while (start + window_size) < len(array):
            """
            Python slice can help to handle out of range issues
            for example:
                array = [1, 2 ,3]
                array[1:100] = [2, 3]
                array[100:] = []
                array[100:10] = []
            So the code from line59 to line66 can be refactored as following
            mid = start + windows_size   # do not need to check range
            end = mid + windows_size  # do not need to check range
            left_window = array[start:mid]
            right_window = array[mid:end]
            """
            mid = start + window_size
            end = mid + window_size
            if end > len(array):
                end = len(array)

            left_window = array[start:mid]
            right_window = array[mid:end]

            _merge_two_sorted_list_v2(dst=array, dst_start=start,
                                      left_window=left_window,
                                      right_window=right_window)

            start += (2*window_size)  # inner loop

        window_size *= 2  # outer loop


def merge_sort_recursive_v2(array: list) -> None:
    """
    Time  Complexity: O(nlog(n)), T(n) = 2T(n/2) + n
    Sapce Complexity: O(n), extra space for array copy (_merge_two_sorted_list)
    Stable sorting
    """

    if len(array) <= 1:
        return

    mid = len(array)//2

    left_window = array[0:mid]
    right_window = array[mid:len(array)]

    merge_sort_recursive_v2(left_window)
    merge_sort_recursive_v2(right_window)

    _merge_two_sorted_list_v2(dst=array, dst_start=0,
                              left_window=left_window,
                              right_window=right_window)


def _get_partition(array: list, start, end) -> None:
    border = start

    # use median of three to determine pivot can get rid of worst cases
    pivot = end

    # find the border
    for compare in range(start, end):
        if array[compare] <= array[pivot]:
            array[border], array[compare] = array[compare], array[border]
            border += 1

    # switch the pivot to the border
    array[border], array[pivot] = array[pivot], array[border]

    return border


def quick_sort(array: list) -> None:
    """
    Time Complexity: O(nlog(n))
    Sapce Complexity: O(1)
    Ref:
    1. https://www.techiedelight.com/iterative-implementation-of-quicksort/
    2. https://stackoverflow.com/questions/39666714/quick-sort-implement-by-queue
    """

    if len(array) <= 1:
        return

    start = 0
    end = len(array) - 1
    stack = list()

    Pair = collections.namedtuple('Pair', ['start', 'end'])
    stack.append(Pair(start=start, end=end))

    while len(stack):
        pair = stack.pop()
        start, end = pair.start, pair.end

        pivot = _get_partition(array, start, end)

        # left partition
        if start < pivot - 1:
            stack.append(Pair(start=start, end=pivot-1))

        # right partition
        if pivot + 1 < end:
            stack.append(Pair(start=pivot + 1, end=end))


def quick_sort_recursive(array: list) -> None:
    """
    Time Complexity:  O(nlog(n))
    Sapce Complexity: O(log(n)) ~ O(n)
    Ref:
    1. https://www.geeksforgeeks.org/python-program-for-quicksort/
    2. https://www.youtube.com/watch?v=CB_NCoxzQnk
    """
    def _quick_sort_recursive(array, start, end):

        if start >= end:
            return

        pivot = _get_partition(array, start, end)
        # start part
        _quick_sort_recursive(array, start, pivot-1)
        # end part
        _quick_sort_recursive(array, pivot+1, end)

    if len(array) <= 1:
        return

    _quick_sort_recursive(array=array, start=0, end=len(array) - 1)


def bubble_sort(array: list) -> None:
    """
    Time:  O(n^2), Best Case is O(n)
    Space: O(1)
    """

    if len(array) <= 1:
        return

    # bubble in len(array)-1 to 1
    for bubble in range(len(array)-1, 0, -1):
        is_swap = False
        for compare in range(0, bubble):
            if array[compare] > array[compare + 1]:
                array[compare], array[compare+1] = array[compare+1], array[compare]
                is_swap = True
        if not is_swap:
            break


def bubble_sort_resursive(array: list) -> None:
    """
    Time:  O(n^2)
    Space: O(n)
    """

    def _bubble_sort_resursive(array, bubble):

        if bubble > len(array) - 1:
            return

        _bubble_sort_resursive(array, bubble + 1)

        for compare in range(0, bubble):
            if array[compare] > array[compare + 1]:
                array[compare], array[compare+1] = array[compare+1], array[compare]

    if len(array) <= 1:
        return

    _bubble_sort_resursive(array=array, bubble=1)


def selection_sort(array: list) -> None:
    """
    Time:  O(n^2)
    Space: O(1)
    """
    if len(array) <= 1:
        return

    # from 0 to len - 2
    for select in range(0, len(array)-1):
        minimum = select
        # from select + 1 to len - 1
        for compare in range(select + 1, len(array)):
            if array[compare] < array[minimum]:
                minimum = compare

        if minimum != select:
            array[select], array[minimum] = array[minimum], array[select]


def selection_sort_recursive(array: list) -> None:
    """
    Time:  O(n^2)
    Space: O(n)
    """
    def _selection_sort_recursive(array, select):

        if select < 0:
            return

        _selection_sort_recursive(array, select - 1)

        minimum = select
        for compare in range(select + 1, len(array)):
            if array[compare] < array[minimum]:
                minimum = compare

        if select != minimum:
            array[select], array[minimum] = array[minimum], array[select]

    if len(array) <= 1:
        return

    _selection_sort_recursive(array, select=len(array)-2)


def insertion_sort(array: list) -> None:
    """
    Time:  O(n^2), best case O(n)
    Space: O(1)
    """
    if len(array) <= 1:
        return

    for insert in range(1, len(array)):
        # compare from new-1 to 0
        for compare in range(insert-1, -1, -1):
            if array[compare] <= array[compare + 1]:
                break
            else:
                array[compare], array[compare+1] = array[compare+1], array[compare]


def insertion_sort_recursive(array: list) -> None:
    """
    Time:  O(n^2)
    Space: O(n)
    """

    def _insertion_sort_recursive(array, insert):

        if insert < 1:
            return

        _insertion_sort_recursive(array, insert-1)
        # compare from new-1 to 0
        for compare in range(insert-1, -1, -1):
            if array[compare] <= array[compare + 1]:
                break
            else:
                array[compare], array[compare+1] = array[compare+1], array[compare]

    if len(array) <= 1:
        return

    _insertion_sort_recursive(array, insert=len(array)-1)


def counting_sort(array: list):
    """
    Ref: https://www.youtube.com/watch?v=OKd534EWcdk
    Time: O(n+k)
    Space: O(n+k)
    """

    offset_arr = [0] * 256
    sorted_arr = [None] * len(array)

    # calculate occurrence count of each character
    for c in array:
        offset_arr[ord(c)] += 1

    # accumulation
    for i in range(1, len(offset_arr)):
        offset_arr[i] = offset_arr[i] + offset_arr[i-1]

    # from n-1 to 1
    for i in range(len(offset_arr)-1, 1, -1):
        offset_arr[i] = offset_arr[i-1]

    # put c to the right place according to index array
    for c in array:
        idx = ord(c)
        sorted_arr[offset_arr[idx]] = c
        offset_arr[idx] += 1

    return sorted_arr


def bucket_sort():
    """
    Ref:
    https://www.youtube.com/watch?v=VuXbEb5ywrU
    https://www.geeksforgeeks.org/bucket-sort-2/
    """
    pass


def radix_sort():
    """
    Ref:
    https://www.youtube.com/watch?v=XiuSW_mEn7g
    https://www.geeksforgeeks.org/radix-sort/
    Time:  O(r*(n+k))
    Space: O(n+k)
    """
    pass


def main():
    array = "bbccaadd"
    print(counting_sort(array))


if __name__ == '__main__':
    sys.exit(main())
