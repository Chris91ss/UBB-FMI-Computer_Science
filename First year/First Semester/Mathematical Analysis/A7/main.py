import numpy as np


# Function to integrate
def f(x):
    return np.exp(-x**2)


# Trapezoidal rule for numerical integration
def trapezoidal_rule(func, _a, b, n):
    h = (b - _a) / n
    x = np.linspace(_a, b, n + 1)
    y = func(x)
    integral = h * (np.sum(y) - 0.5 * (y[0] + y[-1]))
    return integral


# True value of the integral (sqrt(pi))
true_value = np.sqrt(np.pi)

# Values of a to test
a_values = np.linspace(0.1, 5, 50)


# Calculate the integral for different values of a
for a in a_values:
    integral_value = trapezoidal_rule(f, -a, a, 1000)
    print(f'a = {a: .2f}, Approximated Integral = {integral_value: .6f}, Error = {np.abs(integral_value - true_value): .6f}')
