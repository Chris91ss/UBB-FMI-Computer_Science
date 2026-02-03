"""
Binary GCD Algorithm (Stein's Algorithm)
"""

def binary_gcd(a, b):
    """Compute GCD using Binary GCD algorithm"""
    # Ensure both numbers are non-negative
    a, b = abs(a), abs(b)
    
    # Handle trivial zero cases early
    if a == 0:
        return b
    if b == 0:
        return a
    
    shift = 0  # counts common factors of 2
    
    # Remove common factors of 2 from both numbers
    while ((a | b) & 1) == 0:  # both even
        a >>= 1
        b >>= 1
        shift += 1
    
    # Make 'a' odd
    while (a & 1) == 0:
        a >>= 1
    
    # Main loop: keep reducing 'b' until it becomes 0
    while b != 0:
        # Remove all factors of 2 from 'b'
        while (b & 1) == 0:
            b >>= 1
        
        # Ensure a ≤ b
        if a > b:
            a, b = b, a
        
        # Subtract smaller (a) from larger (b)
        b = b - a
    
    # Restore common factors of 2
    return a << shift
