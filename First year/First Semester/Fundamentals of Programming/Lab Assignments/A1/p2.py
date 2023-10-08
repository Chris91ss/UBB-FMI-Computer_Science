# Solve the problem from the second set here
# 9. Consider a given natural number n. Determine the product p of all the proper factors of n.


def factors_product():
    n = int(input("n = "))

    product = 1
    for i in range(2, n):
        if n % i == 0:
            product *= i

    print("The product of all the proper factors of n is: ", product)


factors_product()
