import math
from dataclasses import dataclass


@dataclass
class Row:
    i: int
    a: int
    p: int
    q: int
    r: int          # r = p^2 - N q^2
    is_square: bool


def is_square(x: int) -> bool:
    if x < 0:
        x = -x
    s = math.isqrt(x)
    return s * s == x


def cf_sqrt_terms(N: int, max_iters: int):
    """Generate a_i terms for the continued fraction of sqrt(N)."""
    a0 = math.isqrt(N)
    m, d, a = 0, 1, a0
    for _ in range(max_iters):
        yield a
        m = d * a - m
        d = (N - m * m) // d
        if d == 0:
            return
        a = (a0 + m) // d


def convergents_and_r(N: int, max_iters: int):
    """Generate rows (i, a_i, p_i, q_i, r_i)."""
    p_m2, p_m1 = 0, 1
    q_m2, q_m1 = 1, 0

    for i, a in enumerate(cf_sqrt_terms(N, max_iters)):
        p = a * p_m1 + p_m2
        q = a * q_m1 + q_m2
        r = p * p - N * q * q

        yield Row(i=i, a=a, p=p, q=q, r=r, is_square=is_square(r))

        p_m2, p_m1 = p_m1, p
        q_m2, q_m1 = q_m1, q


def factor_by_pell_step(N: int, max_iters: int = 5000, print_first_rows: int = 12):
    """
    N is small enough that we can search for an index i with:
        p_i^2 - N q_i^2 = 1
    which implies p_i^2 ≡ 1 (mod N), then gcd(p_i ± 1, N) gives factors.
    """

    print(f"N = {N}\n")
    print(f"{'i':>3} {'a_i':>4} {'p_i':>12} {'q_i':>12} {'r_i=p^2-Nq^2':>16}")
    print("-" * 55)

    found = None
    for row in convergents_and_r(N, max_iters):
        if row.i < print_first_rows:
            print(f"{row.i:3d} {row.a:4d} {row.p:12d} {row.q:12d} {row.r:16d}")

        if row.r == 1:
            # We can work modulo N to keep numbers small
            x = row.p % N  # because gcd(p±1,N)=gcd((p mod N)±1,N)
            g1 = math.gcd(x - 1, N)
            g2 = math.gcd(x + 1, N)
            if 1 < g1 < N or 1 < g2 < N:
                found = (row, x, g1, g2)
                break

    if not found:
        print("\nNo factor found within max_iters. Increase max_iters.")
        return None, None

    row, x, g1, g2 = found
    print("\n--- Found step ---")
    print(f"Index i = {row.i}")
    print(f"r_i = p_i^2 - N*q_i^2 = {row.r}  (so p_i^2 ≡ 1 (mod N))")
    print(f"x = p_i mod N = {x}")
    print(f"Check: x^2 mod N = {(x*x) % N}")
    print(f"gcd(x-1, N) = gcd({x-1}, {N}) = {g1}")
    print(f"gcd(x+1, N) = gcd({x+1}, {N}) = {g2}")

    # Pick the non-trivial factors
    factors = []
    for g in (g1, g2):
        if 1 < g < N:
            factors.append(g)

    if not factors:
        return None, None

    f = factors[0]
    return f, N // f


if __name__ == "__main__":
    # 72 -> N = 7871
    N = 7871
    f1, f2 = factor_by_pell_step(N, max_iters=10000, print_first_rows=12)

    print("\nResult:")
    if f1 is not None:
        print(f"{N} = {f1} * {f2}")
    else:
        print("Failed.")
