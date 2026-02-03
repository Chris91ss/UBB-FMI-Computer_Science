import time
from typing import List, Tuple

import numpy as np
from mpi4py import MPI

from polynomial_multiplication import (
    regular_multiply_sequential,
    karatsuba_multiply_sequential,
    generate_random_polynomial,
)


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


# ==================== HELPER FUNCTIONS ====================

def _distribute_ranges(total: int, workers: int, worker_rank: int) -> Tuple[int, int]:
    """
    Split a range [0, total) into roughly equal contiguous chunks.
    Returns the (start, end) indices for the given worker_rank in [0, workers).
    """
    base = total // workers
    rem = total % workers

    if worker_rank < rem:
        start = worker_rank * (base + 1)
        end = start + base + 1
    else:
        start = rem * (base + 1) + (worker_rank - rem) * base
        end = start + base

    return start, end


# ==================== MPI POLYNOMIAL MULTIPLICATION ====================

def mpi_regular_multiply(poly1: List[int], poly2: List[int]) -> Tuple[List[int], float]:
    """
    Naive O(n²) polynomial multiplication using MPI.

    - Rank 0 holds the input polynomials and gathers the final result.
    - All ranks receive the polynomials via high-level broadcast.
    - Each rank computes a contiguous subset of result coefficients.
    - Partial results are combined with Reduce (sum) on rank 0.

    Returns (result, elapsed_time) on rank 0.
    On non-root ranks, the result list is empty.
    """
    # Broadcast full polynomials from root as Python objects
    if rank == 0:
        data = (poly1, poly2)
    else:
        data = None

    poly1, poly2 = comm.bcast(data, root=0)

    n1 = len(poly1)
    n2 = len(poly2)

    result_len = n1 + n2 - 1

    # Each rank computes a range of coefficients
    start_idx, end_idx = _distribute_ranges(result_len, size, rank)

    local_result = [0] * result_len

    comm.Barrier()
    t_start = time.time()

    for k in range(start_idx, end_idx):
        # coefficient k: sum_{i+j=k} a_i * b_j
        for i in range(max(0, k - n2 + 1), min(n1, k + 1)):
            j = k - i
            if 0 <= j < n2:
                local_result[k] += poly1[i] * poly2[j]

    # Reduce partial sums into global result on rank 0.
    # Use numpy arrays so MPI.SUM is element-wise addition.
    local_arr = np.array(local_result, dtype="int64")
    if rank == 0:
        global_arr = np.empty_like(local_arr)
    else:
        global_arr = None

    comm.Reduce(local_arr, global_arr, op=MPI.SUM, root=0)
    comm.Barrier()
    t_end = time.time()

    elapsed = t_end - t_start

    if rank == 0:
        global_result = global_arr.tolist()
        return global_result, elapsed
    return [], elapsed


def mpi_karatsuba_multiply(poly1: List[int], poly2: List[int]) -> Tuple[List[int], float]:
    """
    Distributed Karatsuba polynomial multiplication using MPI.

    Strategy (high-level):
    - Rank 0 does the full Karatsuba recursion.
    - For the three independent top-level multiplications (z0, z1, z2),
      it uses MPI to parallelise each call across all ranks using the
      naive MPI multiplication as the base primitive.

    This keeps the code understandable while still demonstrating a
    distributed version of the Karatsuba idea.
    """
    # We only orchestrate the algorithm from rank 0.
    # Other ranks simply participate in the naive MPI multiplications
    # when called via helper.

    def karatsuba_distributed(a: List[int], b: List[int]) -> List[int]:
        # Base case: for small inputs just use the MPI naive version
        # (which itself splits the work across processes).
        if len(a) < 32 or len(b) < 32 or size == 1:
            # Let rank 0 provide data; others will receive via broadcast inside mpi_regular_multiply
            if rank == 0:
                res, _ = mpi_regular_multiply(a, b)
            else:
                # Other ranks call with dummy data; mpi_regular_multiply ignores it for root 0
                res, _ = mpi_regular_multiply([], [])
            return res

        # Make both polynomials same length
        max_len = max(len(a), len(b))
        a_padded = a + [0] * (max_len - len(a))
        b_padded = b + [0] * (max_len - len(b))

        mid = max_len // 2

        low1, high1 = a_padded[:mid], a_padded[mid:]
        low2, high2 = b_padded[:mid], b_padded[mid:]

        # z0 = low1 * low2 (distributed)
        if rank == 0:
            z0, _ = mpi_regular_multiply(low1, low2)
        else:
            z0, _ = mpi_regular_multiply([], [])

        # z2 = high1 * high2 (distributed)
        if rank == 0:
            z2, _ = mpi_regular_multiply(high1, high2)
        else:
            z2, _ = mpi_regular_multiply([], [])

        # (low1 + high1)
        max_sum_len1 = max(len(low1), len(high1))
        sum1 = [0] * max_sum_len1
        for i in range(len(low1)):
            sum1[i] += low1[i]
        for i in range(len(high1)):
            sum1[i] += high1[i]

        # (low2 + high2)
        max_sum_len2 = max(len(low2), len(high2))
        sum2 = [0] * max_sum_len2
        for i in range(len(low2)):
            sum2[i] += low2[i]
        for i in range(len(high2)):
            sum2[i] += high2[i]

        # z1 = (low1 + high1) * (low2 + high2) (distributed)
        if rank == 0:
            z1, _ = mpi_regular_multiply(sum1, sum2)
        else:
            z1, _ = mpi_regular_multiply([], [])

        if rank != 0:
            # Non-root ranks do not assemble the final result; they already
            # contributed in the Reduce operations above.
            return []

        # On rank 0: combine like classic Karatsuba
        from polynomial_multiplication import subtract_polynomials

        z1 = subtract_polynomials(z1, z0)
        z1 = subtract_polynomials(z1, z2)

        result_size = len(a) + len(b) - 1
        result = [0] * result_size

        # Add z0
        for i in range(len(z0)):
            if i < result_size:
                result[i] += z0[i]

        # Add z1 * x^mid
        for i in range(len(z1)):
            idx = i + mid
            if idx < result_size:
                result[idx] += z1[i]

        # Add z2 * x^(2*mid)
        for i in range(len(z2)):
            idx = i + 2 * mid
            if idx < result_size:
                result[idx] += z2[i]

        return result

    comm.Barrier()
    t_start = time.time()
    result = karatsuba_distributed(poly1, poly2)
    comm.Barrier()
    t_end = time.time()

    elapsed = t_end - t_start

    if rank == 0:
        return result, elapsed
    return [], elapsed


# ==================== BIG NUMBER MULTIPLICATION (BONUS) ====================

def mpi_big_number_regular(num1: str, num2: str) -> Tuple[str, float]:
    """
    Naive O(n²) big number multiplication using MPI.

    Implementation mirrors `big_number_regular_sequential` from
    `polynomial_multiplication.py`, but distributes the computation
    of digit positions across ranks and reduces the partial results.
    """
    from polynomial_multiplication import big_number_regular_sequential

    # Broadcast full numbers as Python objects
    if rank == 0:
        data = (num1, num2)
    else:
        data = None

    num1, num2 = comm.bcast(data, root=0)

    n1 = len(num1)
    n2 = len(num2)

    result_len = n1 + n2

    # Reverse for easier indexing
    num1_rev = num1[::-1]
    num2_rev = num2[::-1]

    start_idx, end_idx = _distribute_ranges(result_len, size, rank)
    local_result = [0] * result_len

    comm.Barrier()
    t_start = time.time()

    for k in range(start_idx, end_idx):
        for i in range(max(0, k - n2 + 1), min(n1, k + 1)):
            j = k - i
            if 0 <= j < n2:
                local_result[k] += int(num1_rev[i]) * int(num2_rev[j])

    # Reduce partial sums into global result using numpy arrays
    local_arr = np.array(local_result, dtype="int64")
    if rank == 0:
        global_arr = np.empty_like(local_arr)
    else:
        global_arr = None

    comm.Reduce(local_arr, global_arr, op=MPI.SUM, root=0)

    if rank == 0:
        global_result = global_arr.tolist()
        # Handle carries on root with the same logic as the sequential version
        carry = 0
        for i in range(len(global_result)):
            global_result[i] += carry
            carry = global_result[i] // 10
            global_result[i] %= 10

        result_str = "".join(str(d) for d in reversed(global_result)).lstrip("0") or "0"
    else:
        result_str = ""

    comm.Barrier()
    t_end = time.time()
    elapsed = t_end - t_start

    if rank == 0:
        return result_str, elapsed
    return "", elapsed


# ==================== DEMO / PERFORMANCE ====================

def run_mpi_polynomial_performance():
    """
    Run a performance comparison between:
    - sequential regular
    - sequential Karatsuba
    - MPI regular
    - MPI "Karatsuba" (top-level distributed)

    Output is a table printed only by rank 0.
    This function is meant to be launched with mpiexec, e.g.:
        mpiexec -n 4 python polynomial_mpi.py
    """
    if rank == 0:
        from colorama import Fore, init as colorama_init

        colorama_init(autoreset=True)
        print(Fore.GREEN + "=" * 80)
        print(Fore.GREEN + "LAB 7 - DISTRIBUTED POLYNOMIAL MULTIPLICATION (MPI)")
        print(Fore.GREEN + "=" * 80)
        print(Fore.CYAN + f"MPI world size: {size} processes\n")

    # Degrees for testing (same style as lab 5)
    test_degrees = [10, 20, 50, 100, 200]

    if rank == 0:
        from colorama import Fore

        print(Fore.CYAN + "Running performance tests...\n")

        results = []
        for deg in test_degrees:
            poly1 = generate_random_polynomial(deg)
            poly2 = generate_random_polynomial(deg)

            # Sequential regular
            t0 = time.time()
            regular_multiply_sequential(poly1, poly2)
            t_reg_seq = time.time() - t0

            # Sequential Karatsuba
            t0 = time.time()
            karatsuba_multiply_sequential(poly1, poly2)
            t_kar_seq = time.time() - t0

            # MPI regular (root provides data; other ranks will join when called)
            mpi_res, t_mpi_reg = mpi_regular_multiply(poly1, poly2)

            # MPI Karatsuba
            mpi_res2, t_mpi_kar = mpi_karatsuba_multiply(poly1, poly2)

            results.append(
                {
                    "deg": deg,
                    "reg_seq": t_reg_seq,
                    "kar_seq": t_kar_seq,
                    "mpi_reg": t_mpi_reg,
                    "mpi_kar": t_mpi_kar,
                }
            )

        # Print table
        print(Fore.GREEN + "\n" + "=" * 90)
        print(Fore.GREEN + "PERFORMANCE SUMMARY TABLE (POLYNOMIALS)")
        print(Fore.GREEN + "=" * 90)
        print(
            Fore.CYAN
            + f"{'Degree':<10} {'Reg Seq (s)':<15} {'Kar Seq (s)':<15} "
            f"{'MPI Reg (s)':<15} {'MPI Kar (s)':<15}"
        )
        print(Fore.CYAN + "-" * 90)

        for r in results:
            print(
                Fore.YELLOW
                + f"{r['deg']:<10} "
                f"{r['reg_seq']:<15.6f} {r['kar_seq']:<15.6f} "
                f"{r['mpi_reg']:<15.6f} {r['mpi_kar']:<15.6f}"
            )

        print()
    else:
        # Non-root ranks still have to participate in all MPI calls inside the loop.
        # They will just sit in the helpers when rank 0 is timing.
        for deg in test_degrees:
            # Dummy local generation to keep types consistent; only root's data is used.
            poly1 = [0] * (deg + 1)
            poly2 = [0] * (deg + 1)

            mpi_regular_multiply(poly1, poly2)
            mpi_karatsuba_multiply(poly1, poly2)


def run_mpi_big_number_performance():
    """
    Bonus: compare sequential and MPI big number multiplication.
    """
    from polynomial_multiplication import (
        big_number_regular_sequential,
        generate_random_big_number,
    )

    if rank == 0:
        from colorama import Fore, init as colorama_init

        colorama_init(autoreset=True)
        print(Fore.GREEN + "=" * 80)
        print(Fore.GREEN + "LAB 7 BONUS - DISTRIBUTED BIG NUMBER MULTIPLICATION (MPI)")
        print(Fore.GREEN + "=" * 80)
        print(Fore.CYAN + f"MPI world size: {size} processes\n")

    test_digits = [10, 20, 50, 100, 200]

    if rank == 0:
        from colorama import Fore

        print(Fore.CYAN + "Running big number performance tests...\n")

        results = []
        for d in test_digits:
            num1 = generate_random_big_number(d)
            num2 = generate_random_big_number(d)

            t0 = time.time()
            big_number_regular_sequential(num1, num2)
            t_seq = time.time() - t0

            mpi_res, t_mpi = mpi_big_number_regular(num1, num2)

            results.append({"digits": d, "seq": t_seq, "mpi": t_mpi})

        print(Fore.GREEN + "\n" + "=" * 80)
        print(Fore.GREEN + "PERFORMANCE SUMMARY TABLE (BIG NUMBERS)")
        print(Fore.GREEN + "=" * 80)
        print(
            Fore.CYAN
            + f"{'Digits':<10} {'Seq (s)':<15} {'MPI Regular (s)':<20}"
        )
        print(Fore.CYAN + "-" * 80)

        for r in results:
            print(
                Fore.YELLOW
                + f"{r['digits']:<10} {r['seq']:<15.6f} {r['mpi']:<20.6f}"
            )

        print()
    else:
        for d in test_digits:
            num1 = "0" * d
            num2 = "0" * d
            mpi_big_number_regular(num1, num2)


if __name__ == "__main__":
    import os

    mode = os.environ.get("LAB7_MODE", "polynomial")
    if mode == "big_numbers":
        run_mpi_big_number_performance()
    else:
        run_mpi_polynomial_performance()


