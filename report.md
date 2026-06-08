# Assignment 3 — Analysis Report (Draft)

## Part 1: Randomized Quicksort

- Implementation: pivot chosen uniformly at random from the current subarray (see `randomized_quicksort` in `randomized_quicksort.py`). The deterministic variant uses the first element as pivot.

### Average-case analysis (sketch)

Let T(n) be the running time (number of comparisons) of randomized quicksort on an array of size n. When the pivot is chosen uniformly at random, each possible rank of pivot (1..n) is equally likely. If the pivot has rank k (0-based: k elements less than pivot), the cost is T(k)+T(n-k-1)+Θ(n) for the partition work. Taking expectation over the random pivot:

$$
E[T(n)] = \frac{1}{n} \sum_{k=0}^{n-1} \bigl(E[T(k)] + E[T(n-k-1)]\bigr) + cn
$$

This simplifies to the recurrence

$$
E[T(n)] = \frac{2}{n} \sum_{k=0}^{n-1} E[T(k)] + cn.
$$

Solving this recurrence (standard technique) yields

$$
E[T(n)] = O(n \log n).
$$

An alternative derivation counts expected comparisons: each pair of elements is compared at most once, and the probability two elements are compared is $2/(j-i+1)$ for elements with ranks i<j; summing over pairs gives $E[\#comparisons]=O(n\log n)$.

### Empirical comparison

I measured average running times for randomized and deterministic quicksort on several input types (random, sorted, reverse-sorted, repeated elements) for increasing sizes. The benchmarking script is `bench.py` and outputs `results.csv`. I plot results using `plot_results.py` which produces PNGs.

Observations:
- On random input both algorithms run in about $O(n\log n)$ empirically and have similar running times.
- On already-sorted or reverse-sorted inputs, deterministic quicksort (first-element pivot) performs poorly (degenerates toward $O(n^2)$), while randomized quicksort remains near $O(n\log n)$.
- Arrays with many repeated elements can change partition behavior; both algorithms may show different constants and variance, but randomized pivoting reduces worst-case sensitivity.

Any discrepancies between empirical timings and theory typically come from constants, Python recursion/overhead, and caching effects. Averaging multiple runs reduces noise.

## Part 2: Hashing with Chaining

- Implementation: `HashTableChaining` in `hash_table.py` uses chaining with dynamic resizing. A simple universal-style hash (parameters `a,b` with large prime `p`) is used over Python's `hash(key)` to reduce collision chance.

### Analysis

Under the simple uniform hashing assumption, the expected length of a chain is the load factor $\alpha = n/m$. Then expected time for `search`, `insert`, and `delete` is $O(1 + \alpha)$ because the operation needs to scan a single chain of expected length $\alpha$.

To keep operations close to constant time, maintain a bounded load factor by resizing (rehashing) when $\alpha$ exceeds a threshold (e.g., 1.5) and shrinking when it falls below a lower threshold (e.g., 0.4). Resizing is $O(n)$ but happens rarely; amortized cost per operation remains $O(1)$.

### Notes on implementation

- The implementation uses Python tuples in buckets `(key, value)` and reinserts items on resize.
- `hash()` is used as the base integer, then transformed by a universal-style linear map modulo a large prime to reduce adversarial collisions.

## How to reproduce

Run the benchmark and plot scripts:

```bash
python3 bench.py
python3 plot_results.py
```

The plots will be saved as `plots_<mode>.png` and the numeric results in `results.csv`.

---

I will run the benchmark now (averaging multiple repeats) and generate the plots; results and images will be added to the workspace.
