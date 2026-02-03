import random

def is_prime(n, k=128):
    """
    Miller-Rabin primality test.

    Args:
        n: An integer to be tested for primality.
        k: The number of rounds of testing to perform.

    Returns:
        True if n is probably prime, False otherwise.
    """
    # Handle base cases: 2 and 3 are prime.
    if n == 2 or n == 3:
        return True
    # Numbers less than or equal to 1, and even numbers (other than 2) are not prime.
    if n <= 1 or n % 2 == 0:
        return False

    # The algorithm requires n-1 to be written as 2^s * d, where d is odd.
    # We find s and d by repeatedly dividing n-1 by 2.
    s = 0
    d = n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    # Perform the test k times for better accuracy.
    for _ in range(k):
        # Choose a random integer 'a' in the range [2, n-2].
        # 'a' is a potential "witness" to the compositeness of n.
        a = random.randrange(2, n - 1)
        # Compute x = a^d mod n.
        x = pow(a, d, n)

        # If x is 1 or n-1, 'a' is not a witness, so we continue to the next iteration.
        if x == 1 or x == n - 1:
            continue
        
        # This loop squares x for s-1 times.
        # If we find x = n-1 at any point, 'a' is not a witness, and we break to the next iteration.
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        # If the loop finishes without finding x = n-1, then n is composite.
        # This is because we didn't find a non-trivial square root of 1 modulo n.
        else:
            return False
    
    # If n passes all k rounds, it is probably prime.
    return True

if __name__ == "__main__":
    try:
        while True:
            num_str = input("Enter an integer to test for primality (or 'q' to quit): ")
            if num_str.lower() == 'q':
                break
            
            try:
                number_to_test = int(num_str)
                if is_prime(number_to_test):
                    print(f"{number_to_test} is probably prime.")
                else:
                    print(f"{number_to_test} is composite.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
            print()
    except KeyboardInterrupt:
        print("\nExiting.")
