"""
Exercise 5: Algorithm for computing Euler's totient function φ(n)
and finding all natural numbers less than a bound b that have a specific value v.
"""


def gcd(a, b):
    """Compute greatest common divisor using Euclidean algorithm."""
    while b != 0:
        a, b = b, a % b
    return abs(a)


def euler_totient(n, target_v=None):
    """
    Compute Euler's totient function φ(n).
    φ(n) = number of integers from 1 to n that are coprime to n.
    
    Args:
        n: Number to compute totient for
        target_v: Optional target value for early stopping
    """
    if n <= 0:
        return 0
    
    count = 0
    for i in range(1, n + 1):
        if gcd(n, i) == 1:
            count += 1
            # Early stop: if we already exceed target, no point continuing
            if target_v is not None and count > target_v:
                return count  # Return any value > target_v
    return count


def find_numbers_with_totient_value(v, b):
    """
    Find all natural numbers less than b that have v as their totient value.
    """
    result = []
    
    # Guard conditions for quick exits
    if b <= 1:
        return result  # No natural numbers < 1
    
    if v < 0:
        return result  # Totient function is always non-negative
    
    # Special case: φ(n) = 1 only for n = 1 and n = 2
    if v == 1:
        if 1 < b:
            result.append(1)
        if 2 < b:
            result.append(2)
        return result
    
    # φ(n) is even for all n > 2
    if v > 1 and v % 2 == 1:
        return result  # No solutions for odd v > 1
    
    # Check all numbers from 1 to b-1
    for n in range(1, b):
        if euler_totient(n, target_v=v) == v:
            result.append(n)
    
    return result


def main():
    """Main program."""
    print("Exercise 5: Euler's Totient Function Algorithm")
    print("=" * 50)
    
    # Get input
    v = int(input("Enter target totient value (v): "))
    b = int(input("Enter upper bound (b): "))
    
    print(f"\nFinding all numbers n < {b} where φ(n) = {v}")
    
    # Find and display results
    numbers = find_numbers_with_totient_value(v, b)
    
    if numbers:
        print(f"\nFound {len(numbers)} number(s): {numbers}")
        # Verify
        for n in numbers:
            print(f"φ({n}) = {euler_totient(n)}")
    else:
        print(f"\nNo numbers found with φ(n) = {v}")
        
        # Explain why no results were found
        if b <= 1:
            print("Reason: No natural numbers exist < 1")
        elif v < 0:
            print("Reason: Totient function is always non-negative")
        elif v > 1 and v % 2 == 1:
            print("Reason: φ(n) is even for all n > 2, so no solutions for odd v > 1")


if __name__ == "__main__":
    main()
