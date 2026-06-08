import random
import time
import csv
from randomized_quicksort import randomized_quicksort, deterministic_quicksort


def generate_array(n, mode='random'):
    """Generate input arrays for benchmarking.

    Modes supported:
    - 'random': uniformly random integers in [0, n]
    - 'sorted': ascending sequence
    - 'reversed': descending sequence
    - 'repeated': many repeated small values
    """
    if mode == 'random':
        return [random.randint(0, n) for _ in range(n)]
    if mode == 'sorted':
        return list(range(n))
    if mode == 'reversed':
        return list(range(n, 0, -1))
    if mode == 'repeated':
        return [random.choice([1, 2, 3, 4]) for _ in range(n)]
    raise ValueError('unknown mode')


def time_sort(func, arr):
    """Time a sort function on a copy of `arr` and return elapsed seconds.

    The sort function is expected to accept a list and sort it in-place or
    return a sorted list; we pass a copy to avoid side effects between runs.
    """
    a = list(arr)
    t0 = time.perf_counter()
    func(a)
    t1 = time.perf_counter()
    return t1 - t0


def run_bench(sizes=(1000, 5000, 10000, 20000), modes=None, out='results.csv', repeats=3):
    """Run the benchmark suite and write averaged results to CSV.

    For each (n, mode) we run `repeats` trials and store the mean runtime for
    randomized and deterministic quicksort.
    """
    if modes is None:
        modes = ['random', 'sorted', 'reversed', 'repeated']
    rows = []
    for n in sizes:
        for mode in modes:
            times_r = []
            times_d = []
            for _ in range(repeats):
                arr = generate_array(n, mode)
                # measure randomized quicksort
                times_r.append(time_sort(randomized_quicksort, arr))
                # measure deterministic (first-element pivot) quicksort
                times_d.append(time_sort(deterministic_quicksort, arr))
            # average the measured times to reduce noise
            rtime = sum(times_r) / len(times_r)
            dtime = sum(times_d) / len(times_d)
            rows.append({'n': n, 'mode': mode, 'randomized': rtime, 'deterministic': dtime})
            print(f'n={n} mode={mode} randomized={rtime:.6f} det={dtime:.6f}')
    # write numeric results for plotting and report
    with open(out, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['n', 'mode', 'randomized', 'deterministic'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


if __name__ == '__main__':
    run_bench()
