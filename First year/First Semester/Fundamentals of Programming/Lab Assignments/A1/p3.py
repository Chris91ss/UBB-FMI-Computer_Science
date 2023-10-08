# Solve the problem from the third set here
# 15. Generate the largest perfect number smaller than a given natural number n.
# If such a number does not exist, a message should be displayed.
# A number is perfect if it is equal to the sum of its divisors, except itself. (e.g. 6 is a perfect number, as 6=1+2+3)


# we are going to use the next formula f = (d^(exp + 1) - 1) / (d - 1) then subtract the number itself from the sum
def sum_div(n: int):  # complexity < O(sqrt(n))
    sd = 1
    d = 2
    while n != 1:
        exp = 0
        f = 1
        while n % d == 0:
            exp += 1
            n /= d
            f *= d  # f = d^exp

        if exp:
            f *= d  # f = d^(exp + 1)
            f -= 1  # f = d^(exp + 1) - 1
            f /= (d - 1)  # f = d^(exp + 1) - 1) / (d - 1)
            sd *= f

        if d == 2:
            d += 1
        else:
            d += 2

        if d * d > n:
            d = n

    return sd


def is_perfect_number(n: int) -> bool:  # a boolean function that returns True if n is perfect and False otherwise
    div_sum = sum_div(n) - n

    if n == div_sum:
        return True
    else:
        return False


def problem():
    n = int(input("n = "))

    while n > 6:  # 6 is the smallest perfect number
        n -= 1
        if is_perfect_number(n):
            print("The largest perfect number smaller than n is: ", n)
            return

    print("No such number exists!")


problem()
