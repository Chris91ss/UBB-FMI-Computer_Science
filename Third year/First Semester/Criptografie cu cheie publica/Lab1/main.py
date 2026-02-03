import math, timeit, gc
from statistics import median

from euclidean_arbitrary_gcd import euclidean_arbitrary_gcd  # modulo Euclid 
from binary_gcd import binary_gcd                            # Stein's binary GCD
from euclidean_subtractive_gcd import euclidean_gcd as subtractive_gcd  # subtractive

def time_median_us(fn, a, b, warmups=3, repeats=7):
    """Return median execution time in microseconds for fn(a,b)."""
    # Warm-up runs (not timed)
    for _ in range(warmups):
        fn(a, b)
    gcold = gc.isenabled()
    gc.disable()
    try:
        t = timeit.repeat(lambda: fn(a, b), number=1, repeat=repeats)
    finally:
        if gcold:
            gc.enable()
    return median(t) * 1_000_000

def print_header(title):
    print(title)
    print("=" * len(title))

def print_table(rows):
    # rows: list of tuples (label, algoname, result, time_us or None)
    print(f"{'Case':<24} {'Algorithm':<12} {'Result':<30} {'Median (μs)':>12}")
    print("-" * 82)
    for case, algo, res, mus in rows:
        t = f"{mus:,.2f}" if mus is not None else "-"
        print(f"{case:<24} {algo:<12} {str(res):<30} {t:>12}")
    print()

def main():
    # --- Core suite (10+ inputs) — all three algorithms run here ---
    core_cases = [
        ("(48,18)", (48, 18)),
        ("(100,25)", (100, 25)),
        ("(17,13)", (17, 13)),
        ("(1000,100)", (1000, 100)),
        ("(0,5)", (0, 5)),
        ("(0,0)", (0, 0)),
        ("(5,0)", (5, 0)),
        ("(1,1)", (1, 1)),
        ("(123456,789012)", (123456, 789012)),            # gcd 12, OK for subtractive
        ("(10^8, 2*10^8)", (10**8, 2*10**8)),             # power-of-two factor
        ("(999983*42, 42)", (999983*42, 42)),             # shared factor big-ish
    ]
    algos_core = [
        ("Euclidean", euclidean_arbitrary_gcd),
        ("Binary GCD", binary_gcd),
        ("Subtractive", subtractive_gcd),
    ]

    print_header("Lab 1: GCD Algorithms Performance Analysis")
    rows = []
    for label, (a, b) in core_cases:
        for name, fn in algos_core:
            mus = time_median_us(fn, a, b)
            res = fn(a, b)
            rows.append((label, name, res, mus))
    print_table(rows)

    # --- Stretch suite — very large / adversarial cases (no subtractive) ---
    stretch_cases = [
        ("(10^10, 10^10+1)", (10**10, 10**10 + 1)),
        ("(10^20, 10^20+1)", (10**20, 10**20 + 1)),
        ("(huge pair)", (123456789012345678901234567890, 987654321098765432109876543210)),
    ]
    algos_stretch = [
        ("Euclidean", euclidean_arbitrary_gcd),
        ("Binary GCD", binary_gcd),
        # Intentionally omit Subtractive: worst-case O(max(a,b)) → impractical here
    ]

    print_header("Stretch Cases (Large / Near-Equal Integers)")
    rows = []
    for label, (a, b) in stretch_cases:
        for name, fn in algos_stretch:
            mus = time_median_us(fn, a, b)
            res = fn(a, b)
            rows.append((label, name, res, mus))
    print_table(rows)

if __name__ == "__main__":
    main()
