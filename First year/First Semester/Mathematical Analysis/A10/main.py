import numpy as np
import matplotlib.pyplot as plt


# Define the quadratic function
def f(x, y, b):
    return 0.5 * (x**2 + b * y**2)


# Gradient of the function
def gradient_f(x, y, b):
    return np.array([x, b * y])


# Gradient Descent Algorithm
def gradient_descent(x0, y0, b, learning_rate, iterations):
    history = []
    for _ in range(iterations):
        history.append((x0, y0))
        grad = gradient_f(x0, y0, b)
        x0 -= learning_rate * grad[0]
        y0 -= learning_rate * grad[1]
    return np.array(history)


# Plotting
def plot_gradient_descent(b_values):
    for b in b_values:
        x_init, y_init = 2.0, 2.0  # Initial point
        learning_rate = 1.0 / (2.0 * b)  # Optimal learning rate for this problem
        iterations = 50

        history = gradient_descent(x_init, y_init, b, learning_rate, iterations)

        # Contour plot
        x = np.linspace(-3, 3, 400)
        y = np.linspace(-3, 3, 400)
        _x, _y = np.meshgrid(x, y)
        _z = f(_x, _y, b)

        plt.contour(_x, _y, _z, levels=20, cmap='viridis')
        plt.plot(history[:, 0], history[:, 1], 'ro-', label=f'b = {b}')

    plt.title('Gradient Descent Iterations and Contour Lines')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()


# Test the function with different b values
plot_gradient_descent([1, 1/2, 1/5, 1/10])
