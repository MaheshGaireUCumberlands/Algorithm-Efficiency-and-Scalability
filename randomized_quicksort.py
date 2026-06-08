import random
import sys

sys.setrecursionlimit(1000000)

def _partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1

def _quicksort_random(arr, low, high):
    if low < high:
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        p = _partition(arr, low, high)
        _quicksort_random(arr, low, p-1)
        _quicksort_random(arr, p+1, high)

def randomized_quicksort(arr):
    a = list(arr)
    _quicksort_random(a, 0, len(a)-1)
    return a

def _quicksort_deterministic(arr, low, high):
    if low < high:
        # use first element as pivot -> move it to end then partition
        arr[low], arr[high] = arr[high], arr[low]
        p = _partition(arr, low, high)
        _quicksort_deterministic(arr, low, p-1)
        _quicksort_deterministic(arr, p+1, high)

def deterministic_quicksort(arr):
    a = list(arr)
    _quicksort_deterministic(a, 0, len(a)-1)
    return a

if __name__ == '__main__':
    import random
    data = [random.randint(0, 1000) for _ in range(1000)]
    print('Randomized quicksort sample run...')
    print(randomized_quicksort(data)[:10])
