import numpy as np
import matplotlib.pyplot as plt


# Define the function
def f(x):
    return x**2


# Define the true derivative
def true_derivative_function(x):
    return 2 * x


# Define the forward difference approximation
def forward_difference(x, h):
    return (f(x + h) - f(x)) / h


# Define the centered difference approximation
def centered_difference(x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


# Choose a point and a range of small values for h
x_value = 2
h_values = np.logspace(-10, 0, 11)

# Compute true derivative
true_derivative = true_derivative_function(x_value)

# Initialize arrays to store errors
forward_errors = []
centered_errors = []

# Calculate errors for different values of h
for _h in h_values:
    forward_error = abs(forward_difference(x_value, _h) - true_derivative)
    centered_error = abs(centered_difference(x_value, _h) - true_derivative)

    forward_errors.append(forward_error)
    centered_errors.append(centered_error)

# Plot the errors
plt.figure(figsize=(10, 6))
plt.loglog(h_values, forward_errors, label='Forward Difference Error (O(h))')
plt.loglog(h_values, centered_errors, label='Centered Difference Error (O(h^2))')
plt.xlabel('h')
plt.ylabel('Error')
plt.title('Error in Finite Difference Approximations')
plt.legend()
plt.show()
