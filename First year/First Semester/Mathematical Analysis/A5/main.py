import numpy as np
import matplotlib.pyplot as plt


# a)Take a convex f and show that for small gamma the method converges to the minimum off.

# Define the convex function f(x) = x^2
# Convex function
def f_convex_function(x):
    return x**2


# Gradient of the function
def gradient_of_the_function(x):
    return 2 * x


# Gradient descent method
def gradient_descent_method(x_0, gamma, numb_steps):
    x = x_0
    x_history = [x]

    for _ in range(numb_steps):
        x = x - gamma * gradient_of_the_function(x)
        x_history.append(x)

    return x_history


# Scenario a: Small gamma
x0 = 4.0
gamma_small = 0.1
num_steps = 10
x_history_small = gradient_descent_method(x0, gamma_small, num_steps)

# Plot the convergence
x_values = np.linspace(-5, 5, 400)
y_values = f_convex_function(x_values)
plt.plot(x_values, y_values, label="f(x) = x^2")
plt.plot(x_history_small, [f_convex_function(x) for x in x_history_small], 'ro-', label="Gradient Descent (small gamma)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.title("Convex Function Convergence (Small Gamma)")
plt.show()


# b) Show that by increasing gamma the method can converge faster (in fewer steps).

# Scenario b: Increasing gamma
gamma_large = 1.0  # Larger learning rate
num_steps_large = 10
x_history_large = gradient_descent_method(x0, gamma_large, num_steps_large)

# Plot the convergence with a larger learning rate
plt.plot(x_values, y_values, label="f(x) = x^2")
plt.plot(x_history_large, [f_convex_function(x) for x in x_history_large], 'go-', label="Gradient Descent (large gamma)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.title("Convex Function Convergence (Large Gamma)")
plt.show()


# c) Show that taking gamma too large might lead to the divergence of the method.

# Scenario c: Gamma too large
gamma_too_large = 2.1  # Too large learning rate
num_steps_large = 10
x_history_too_large = gradient_descent_method(x0, gamma_too_large, num_steps_large)

# Plot the convergence with a too large learning rate
plt.plot(x_values, y_values, label="f(x) = x^2")
plt.plot(x_history_too_large, [f_convex_function(x) for x in x_history_too_large], 'bo-', label="Gradient Descent (too large gamma)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.title("Convex Function Divergence (Too Large Gamma)")
plt.show()


# d) Take a non-convex f and show that the method can get stuck in a local minimum.

# Define the non-convex function f(x) = x^4 - 3x^3 + 2x^2
# Non-convex function
def f_non_convex_function(x):
    return x**4 - 3 * x**3 + 2


# Gradient of the non-convex function
def gradient_of_the_non_convex_function(x):
    return 4 * x**3 - 9 * x**2


# Scenario d: Non-convex function
x0_non_convex = 2.0
gamma_non_convex = 0.01
num_steps_non_convex = 50
x_history_non_convex = gradient_descent_method(x0_non_convex, gamma_non_convex, num_steps_non_convex)

# Plot the convergence for a non-convex function
x_values_non_convex = np.linspace(-1, 3, 400)
y_values_non_convex = f_non_convex_function(x_values_non_convex)
plt.plot(x_values_non_convex, y_values_non_convex, label="f(x) = x^4 - 3x^3 + 2")
plt.plot(x_history_non_convex, [f_non_convex_function(x) for x in x_history_non_convex], 'mo-', label="Gradient Descent (non-convex)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.title("Non-Convex Function Convergence (Getting Stuck in Local Minimum)")
plt.show()
