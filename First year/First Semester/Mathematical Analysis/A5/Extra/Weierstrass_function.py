import numpy as np
import matplotlib.pyplot as plt


def weierstrass(value_x, value_a, value_b, number_of_terms):
    result = 0
    for n in range(number_of_terms):
        result += value_a ** n * np.cos(value_b ** n * np.pi * value_x)
    return result


x = np.linspace(0, 1, 10000)  # Define the x values
a = 0.5  # Choose a value for 'a' (0 < a < 1)
b = 3    # Choose a value for 'b' (a*b > 1 + 3*pi/2)
n_terms = 100  # Number of terms in the series

y = weierstrass(x, a, b, n_terms)

plt.plot(x, y)
plt.title("Graph of the Weierstrass Function")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.show()
