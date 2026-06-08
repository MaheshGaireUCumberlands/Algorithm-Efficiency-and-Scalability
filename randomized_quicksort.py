import random
import sys

# Increase recursion limit for large arrays (Python default may be small)
sys.setrecursionlimit(1000000)


def _partition(arr, low, high):
    """Partition step of quicksort (Lomuto scheme).

    Elements <= pivot are moved to the left of the pivot index; elements
    > pivot are left on the right. Returns final pivot index.
    """
    pivot = arr[high]
    i = low - 1
    # iterate through subarray and move elements <= pivot to the front
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    # place pivot after the last smaller-or-equal element
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def _quicksort_random(arr, low, high):
    """Recursive randomized quicksort helper.

    Chooses a pivot uniformly at random from arr[low:high+1], swaps it to
    the end, partitions, then recurses on the two subarrays.
    """
    if low < high:
        # choose a random pivot index and move pivot to 'high' for partition
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        p = _partition(arr, low, high)
        # recurse on left and right partitions
        _quicksort_random(arr, low, p - 1)
        _quicksort_random(arr, p + 1, high)


def randomized_quicksort(arr):
    """Public API: returns a sorted copy using randomized quicksort.

    We copy the input to avoid mutating the caller's array.
    """
    a = list(arr)
    _quicksort_random(a, 0, len(a) - 1)
    return a


def _quicksort_deterministic(arr, low, high):
    """Recursive deterministic quicksort using first element as pivot.

    This implementation moves the first element to the end and then calls
    the same partition routine, which results in worst-case O(n^2) on
    already-sorted input.
    """
    if low < high:
        # move first element to end to reuse the same _partition implementation
        arr[low], arr[high] = arr[high], arr[low]
        p = _partition(arr, low, high)
        _quicksort_deterministic(arr, low, p - 1)
        _quicksort_deterministic(arr, p + 1, high)


def deterministic_quicksort(arr):
    """Public API: returns a sorted copy using deterministic quicksort.

    Uses the first element as pivot (via swap). Returns a new list.
    """
    a = list(arr)
    _quicksort_deterministic(a, 0, len(a) - 1)
    return a


if __name__ == '__main__':
    import random as _r

    # quick smoke test when run directly
    data = [_r.randint(0, 1000) for _ in range(1000)]
    print('Randomized quicksort sample run...')
    print(randomized_quicksort(data)[:10])
