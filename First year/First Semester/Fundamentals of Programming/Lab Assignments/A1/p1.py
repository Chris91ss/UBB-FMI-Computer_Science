# Solve the problem from the first set here
# 2. Given natural number n, determine the prime numbers p1 and p2 such that n = p1 + p2
# (check the Goldbach hypothesis).
import math


def is_prime(n: int) -> bool:  # checks if a number is prime or not
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for enum in range(3, int(math.sqrt(n)) + 1):
        if n % enum == 0:
            return False
    return True


def goldbach():  # determines the prime pair numbers so that n = p1 + p2
    n = int(input("n = "))
    if n <= 2 and n % 2 != 0:
        print("ERROR, there are no existing pairs such that the following expression is verified:\n",
              "n = p1 + p2, where p1 and p2 are prime numbers")
        return

    p1 = 0
    for i in range(2, n // 2 + 1):
        if is_prime(i):
            p1 = i

        p2 = n - p1
        if is_prime(p2):
            print("n = ", p1, " + ", p2)
            break


goldbach()
