"""
================================================================================
LAB WORK 1: BENCHMARKING ALGORITHMIC GROWTH RATES
From: DATA STRUCTURES & ALGORITHMS WITH PYTHON - Algorithm Analysis
      Laboratory Works (Python)

Objective:
Empirically investigate constant, logarithmic, linear, nlogn, quadratic and
exponential growth patterns.

Tasks:
• Implement representative operations/algorithms: list indexing, binary search,
  linear search, merge sort, a double-loop pair counter and (for small n only)
  exponential subset enumeration.
• Choose safe input-size ranges appropriate to each growth class; exponential
  algorithms must use much smaller n.
• Repeat measurements. Exclude data generation from the timed region and document
  input characteristics.
• Plot execution time against n. Where useful, examine normalized quantities such
  as T(n)/n, T(n)/(nlog₂n) and T(n)/n².
• Prepare a table of algorithm, theoretical bound, measured trend and
  experimental limitations.

Analysis:
Discuss constants, lower-order terms, interpreter overhead, input limits and
whether measured trends agree with expected growth classes.

Deliverables:
Python source, experimental setup, timing data, plots and comparison table.
================================================================================
"""

import sys
import time
import math
import random
import platform


# 1. Representative Algorithms

def list_index(arr, idx):
    return arr[idx]


def bin_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def lin_search(arr, target):
    i = 0
    n = len(arr)
    while i < n:
        if arr[i] == target:
            return i
        i += 1
    return -1


def merge(left, right):
    out = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def merge_sort(seq):
    if len(seq) <= 1:
        return seq
    mid = len(seq) // 2
    return merge(merge_sort(seq[:mid]), merge_sort(seq[mid:]))


def count_pairs(nums):
    valid_pairs = 0
    n = len(nums)
    for idx1 in range(n):
        for idx2 in range(idx1 + 1, n):
            if nums[idx1] + nums[idx2] > 0:
                valid_pairs += 1
    return valid_pairs


def subset_enum(collection):
    n = len(collection)
    result = []
    for mask in range(1 << n):
        subset = [collection[i] for i in range(n) if (mask & (1 << i))]
        result.append(subset)
    return result


# 2. Timing Helpers

def median_time(fn, *args, trials=5):
    timings = []
    for _ in range(trials):
        start = time.perf_counter()
        fn(*args)
        stop = time.perf_counter()
        timings.append(stop - start)
    timings.sort()
    return timings[len(timings) // 2]


def ascii_bar(val, max_val, bar_width=25):
    if max_val <= 0:
        return ""
    stars = int((val / max_val) * bar_width)
    return "*" * max(stars, 1)


# 3. Benchmark Execution

def run_benchmarks():
    print("=" * 70)
    print("LAB WORK 1: BENCHMARKING ALGORITHMIC GROWTH RATES")
    print(f"Platform: {platform.system()} ({platform.machine()}) | Python: {platform.python_version()}")
    print("Timing method: Median of 5 trials via time.perf_counter()")
    print("=" * 70)

    # (a) O(1) List Indexing
    print("\n--- 1. Constant Growth O(1): List Indexing ---")
    sizes_o1 = [10000, 50000, 100000, 250000, 500000]
    print(f"{'n':>10} | {'Time (s)':>12} | Relative Trend")
    print("-" * 45)
    for n in sizes_o1:
        arr = list(range(n))
        idx = n // 2
        t = median_time(list_index, arr, idx)
        print(f"{n:>10} | {t:>12.8f} | Constant lookup")

    # (b) O(log n) Binary Search
    print("\n--- 2. Logarithmic Growth O(log n): Binary Search ---")
    sizes_log = [10000, 50000, 100000, 250000, 500000]
    print(f"{'n':>10} | {'Time (s)':>12} | {'T / log2(n)':>15}")
    print("-" * 45)
    for n in sizes_log:
        arr = list(range(n))
        target = -1
        t = median_time(bin_search, arr, target)
        norm = t / math.log2(n)
        print(f"{n:>10} | {t:>12.8f} | {norm:>15.2e}")

    # (c) O(n) Linear Search
    print("\n--- 3. Linear Growth O(n): Linear Search ---")
    sizes_lin = [10000, 50000, 100000, 200000, 400000]
    print(f"{'n':>10} | {'Time (s)':>12} | {'T / n':>15} | Plot")
    print("-" * 60)
    times_lin = []
    for n in sizes_lin:
        arr = list(range(n))
        target = -1
        t = median_time(lin_search, arr, target)
        times_lin.append(t)
    max_t = max(times_lin)
    for n, t in zip(sizes_lin, times_lin):
        norm = t / n
        print(f"{n:>10} | {t:>12.8f} | {norm:>15.2e} | {ascii_bar(t, max_t)}")

    # (d) O(n log n) Merge Sort
    print("\n--- 4. Linearithmic Growth O(n log n): Merge Sort ---")
    sizes_nlog = [1000, 2000, 4000, 8000, 16000]
    print(f"{'n':>10} | {'Time (s)':>12} | {'T / (n log2 n)':>15} | Plot")
    print("-" * 65)
    times_nlog = []
    for n in sizes_nlog:
        arr = [random.randint(1, 100000) for _ in range(n)]
        t = median_time(merge_sort, arr)
        times_nlog.append(t)
    max_t = max(times_nlog)
    for n, t in zip(sizes_nlog, times_nlog):
        norm = t / (n * math.log2(n))
        print(f"{n:>10} | {t:>12.8f} | {norm:>15.2e} | {ascii_bar(t, max_t)}")

    # (e) O(n^2) Double-Loop Pair Counter
    print("\n--- 5. Quadratic Growth O(n^2): Pair Counter ---")
    sizes_quad = [200, 400, 800, 1600, 3200]
    print(f"{'n':>10} | {'Time (s)':>12} | {'T / (n^2)':>15} | Plot")
    print("-" * 60)
    times_quad = []
    for n in sizes_quad:
        arr = [random.randint(-100, 100) for _ in range(n)]
        t = median_time(count_pairs, arr)
        times_quad.append(t)
    max_t = max(times_quad)
    for n, t in zip(sizes_quad, times_quad):
        norm = t / (n ** 2)
        print(f"{n:>10} | {t:>12.8f} | {norm:>15.2e} | {ascii_bar(t, max_t)}")

    # (f) O(2^n) Exponential Subset Enumeration (small n)
    print("\n--- 6. Exponential Growth O(2^n): Subset Enumeration ---")
    sizes_exp = [10, 12, 14, 16, 18, 20]
    print(f"{'n':>10} | {'Time (s)':>12} | {'T / (2^n)':>15} | Plot")
    print("-" * 60)
    times_exp = []
    for n in sizes_exp:
        arr = list(range(n))
        t = median_time(subset_enum, arr, trials=3)
        times_exp.append(t)
    max_t = max(times_exp)
    for n, t in zip(sizes_exp, times_exp):
        norm = t / (2 ** n)
        print(f"{n:>10} | {t:>12.8f} | {norm:>15.2e} | {ascii_bar(t, max_t)}")

    # Summary Table
    print("\n" + "=" * 70)
    print("SUMMARY COMPARISON TABLE")
    print("=" * 70)
    summary = [
        ("List Indexing", "O(1)", "Flat / Independent of n", "Direct memory offset"),
        ("Binary Search", "O(log n)", "Very slow growth", "Requires sorted array"),
        ("Linear Search", "O(n)", "T(n)/n ~ constant ratio", "Cache effects at large n"),
        ("Merge Sort", "O(n log n)", "T(n)/(n log n) stable", "Python list slicing overhead"),
        ("Pair Counter", "O(n^2)", "4x time when n doubles", "Impractical for n > 10,000"),
        ("Subset Enum", "O(2^n)", "Doubles with each +1 to n", "Memory exhaustion for n > 22"),
    ]
    print(f"{'Algorithm':<16} | {'Bound':<10} | {'Measured Trend':<26} | {'Limitations'}")
    print("-" * 75)
    for name, bound, trend, limit in summary:
        print(f"{name:<16} | {bound:<10} | {trend:<26} | {limit}")
    print("=" * 70)


if __name__ == "__main__":
    run_benchmarks()

"""
================================================================================
SAMPLE OUTPUT:
================================================================================
======================================================================
LAB WORK 1: BENCHMARKING ALGORITHMIC GROWTH RATES
Platform: Linux (x86_64) | Python: 3.12.3
Timing method: Median of 5 trials via time.perf_counter()
======================================================================

--- 1. Constant Growth O(1): List Indexing ---
         n |     Time (s) | Relative Trend
---------------------------------------------
     10000 |   0.00000077 | Constant lookup
     50000 |   0.00000051 | Constant lookup
    100000 |   0.00000045 | Constant lookup
    250000 |   0.00000097 | Constant lookup
    500000 |   0.00000070 | Constant lookup

--- 2. Logarithmic Growth O(log n): Binary Search ---
         n |     Time (s) |     T / log2(n)
---------------------------------------------
     10000 |   0.00000412 |        3.10e-07
     50000 |   0.00000581 |        3.72e-07
    100000 |   0.00000639 |        3.84e-07
    250000 |   0.00000693 |        3.86e-07
    500000 |   0.00000630 |        3.33e-07

--- 3. Linear Growth O(n): Linear Search ---
         n |     Time (s) |           T / n | Plot
------------------------------------------------------------
     10000 |   0.00144010 |        1.44e-07 | *
     50000 |   0.00778828 |        1.56e-07 | ***
    100000 |   0.01495151 |        1.50e-07 | ******
    200000 |   0.02994593 |        1.50e-07 | ************
    400000 |   0.05966818 |        1.49e-07 | *************************

--- 4. Linearithmic Growth O(n log n): Merge Sort ---
         n |     Time (s) |  T / (n log2 n) | Plot
-----------------------------------------------------------------
      1000 |   0.00497263 |        4.99e-07 | *
      2000 |   0.00778460 |        3.55e-07 | **
      4000 |   0.01769919 |        3.70e-07 | *****
      8000 |   0.03705675 |        3.57e-07 | ***********
     16000 |   0.08073357 |        3.61e-07 | *************************

--- 5. Quadratic Growth O(n^2): Pair Counter ---
         n |     Time (s) |       T / (n^2) | Plot
------------------------------------------------------------
       200 |   0.00265623 |        6.64e-08 | *
       400 |   0.01250247 |        7.81e-08 | *
       800 |   0.05537826 |        8.65e-08 | *
      1600 |   0.22978087 |        8.98e-08 | ******
      3200 |   0.92535036 |        9.04e-08 | *************************

--- 6. Exponential Growth O(2^n): Subset Enumeration ---
         n |     Time (s) |       T / (2^n) | Plot
------------------------------------------------------------
        10 |   0.00226318 |        2.21e-06 | *
        12 |   0.00883482 |        2.16e-06 | *
        14 |   0.04408709 |        2.69e-06 | *
        16 |   0.22474591 |        3.43e-06 | *
        18 |   1.13123501 |        4.32e-06 | *****
        20 |   5.52872718 |        5.27e-06 | *************************

======================================================================
SUMMARY COMPARISON TABLE
======================================================================
Algorithm        | Bound      | Measured Trend             | Limitations
---------------------------------------------------------------------------
List Indexing    | O(1)       | Flat / Independent of n    | Direct memory offset
Binary Search    | O(log n)   | Very slow growth           | Requires sorted array
Linear Search    | O(n)       | T(n)/n ~ constant ratio    | Cache effects at large n
Merge Sort       | O(n log n) | T(n)/(n log n) stable      | Python list slicing overhead
Pair Counter     | O(n^2)     | 4x time when n doubles     | Impractical for n > 10,000
Subset Enum      | O(2^n)     | Doubles with each +1 to n  | Memory exhaustion for n > 22
======================================================================
================================================================================
"""
