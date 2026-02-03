"""
Euclidean GCD for Arbitrary-Precision Integers
This iterative Euclidean algorithm works with Python's big integers (arbitrary size).
"""

def euclidean_arbitrary_gcd(a, b):
    """Compute GCD using Euclid's algorithm on arbitrary-precision integers."""
    # Normalize inputs to be non-negative to simplify logic
    a, b = abs(a), abs(b)

    # Quick exits for zeros
    if a == 0:
        return b
    if b == 0:
        return a

    # Classic iterative Euclidean algorithm using modulo
    while b != 0:
        a, b = b, a % b
    return a
