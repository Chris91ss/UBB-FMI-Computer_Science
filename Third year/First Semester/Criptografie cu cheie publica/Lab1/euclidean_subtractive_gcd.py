"""
Subtractive-style Euclidean GCD (uses subtraction instead of modulo)
This variant repeatedly subtracts the smaller value from the larger one
 until both numbers become equal. It is distinct from the modulo version.
"""

def euclidean_gcd(a, b):
    """Compute GCD using repeated subtraction (no modulo)."""
    # Normalize inputs to be non-negative
    a, b = abs(a), abs(b)

    # Handle zeros quickly
    if a == 0:
        return b
    if b == 0:
        return a

    # Repeated subtraction until numbers match
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a
