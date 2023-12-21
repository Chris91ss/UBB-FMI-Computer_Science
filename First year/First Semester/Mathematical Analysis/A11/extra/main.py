import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv


# Define the quadratic function
def f1(x, y):
    return 0.5 * (x**2 + 3 * y**2)


# Define the objective function
def f2(x, y):
    return 100 * (y - x**2)**2 + (1 - x)**2


# Gradient of the function
def gradient_f1(x, y):
    return np.array([x, 3 * y])


# Gradient of the objective function
def gradient_f2(x, y):
    df_dx = -400 * x * (y - x**2) - 2 * (1 - x)
    df_dy = 200 * (y - x**2)
    return np.array([df_dx, df_dy])


# Hessian of the function
def hessian_f1():
    return np.array([[1, 0], [0, 3]])


# Hessian of the objective function
def hessian_f2(x, y):
    df_dx_dx = 1200 * x**2 - 400 * y + 2
    df_dx_dy = -400 * x
    df_dy_dx = -400 * x
    df_dy_dy = 200
    return np.array([[df_dx_dx, df_dx_dy], [df_dy_dx, df_dy_dy]])


# Newton's Method
def newton_method1(x0, y0, iterations):
    history = []
    for i in range(iterations):
        history.append((x0, y0))
        grad = gradient_f1(x0, y0)
        hessian_inv = inv(hessian_f1())
        delta = -np.dot(hessian_inv, grad)
        x0, y0 = x0 + delta[0], y0 + delta[1]
        print(f"Iteration {i + 1}: (x, y) = ({x0: .4f}, {y0: .4f})")
    return np.array(history)


def newton_method2(x0, y0, iterations):
    history = []
    for i in range(iterations):
        history.append((x0, y0))
        grad = gradient_f2(x0, y0)
        hessian_inv = inv(hessian_f2(x0, y0))
        delta = -np.dot(hessian_inv, grad)
        x0 += delta[0]
        y0 += delta[1]
        print(f"Iteration {i + 1}: (x, y) = ({x0: .4f}, {y0: .4f})")
    return np.array(history)


# Gradient Descent Algorithm
def gradient_descent1(x0, y0, learning_rate, iterations):
    history = []
    for i in range(iterations):
        history.append((x0, y0))
        grad = gradient_f1(x0, y0)
        x0 -= learning_rate * grad[0]
        y0 -= learning_rate * grad[1]
        print(f"Iteration {i + 1}: (x, y) = ({x0: .4f}, {y0: .4f})")
    return np.array(history)


def gradient_descent2(x0, y0, learning_rate, iterations):
    history = []
    for i in range(iterations):
        history.append((x0, y0))
        grad = gradient_f2(x0, y0)
        x0 -= learning_rate * grad[0]
        y0 -= learning_rate * grad[1]
        print(f"Iteration {i + 1}: (x, y) = ({x0: .4f}, {y0: .4f})")
    return np.array(history)


# Plotting
def plot_optimization_methods1():
    x_init, y_init = 2.0, 2.0  # Initial point
    iterations = 10

    # Newton's Method
    print("Newton's Method First Function:")
    newton_history = newton_method1(x_init, y_init, iterations)
    print("\n")

    # Gradient Descent
    print("Gradient Descent First Function:")
    learning_rate = 0.1
    gd_history = gradient_descent1(x_init, y_init, learning_rate, iterations)
    print("\n")

    # Contour plot
    x = np.linspace(-3, 3, 400)
    y = np.linspace(-3, 3, 400)
    _x, _y = np.meshgrid(x, y)
    _z = f1(_x, _y)

    # Newton's Method Plot
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.contour(_x, _y, _z, levels=20, cmap='viridis')
    plt.plot(newton_history[:, 0], newton_history[:, 1], 'ro-', label="Newton's Method")
    plt.title("Newton's Method")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    # Gradient Descent Plot
    plt.subplot(1, 2, 2)
    plt.contour(_x, _y, _z, levels=20, cmap='viridis')
    plt.plot(gd_history[:, 0], gd_history[:, 1], 'bo-', label='Gradient Descent')
    plt.title('Gradient Descent')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    plt.show()


def plot_optimization_methods2():
    x_init, y_init = -1.2, 1.0  # Initial point
    iterations = 10

    # Newton's Method
    print("Newton's Method Second Function:")
    newton_history = newton_method2(x_init, y_init, iterations)
    print("\n")

    # Gradient Descent
    print("Gradient Descent Second Function:")
    learning_rate = 0.001
    gd_history = gradient_descent2(x_init, y_init, learning_rate, iterations)
    print("\n")

    # Contour plot
    x = np.linspace(-2, 2, 400)
    y = np.linspace(-1, 3, 400)
    _x, _y = np.meshgrid(x, y)
    _z = f2(_x, _y)

    # Newton's Method Plot
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.contour(_x, _y, _z, levels=20, cmap='viridis')
    plt.plot(newton_history[:, 0], newton_history[:, 1], 'ro-', label="Newton's Method")
    plt.title("Newton's Method")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    # Gradient Descent Plot
    plt.subplot(1, 2, 2)
    plt.contour(_x, _y, _z, levels=20, cmap='viridis')
    plt.plot(gd_history[:, 0], gd_history[:, 1], 'bo-', label='Gradient Descent')
    plt.title('Gradient Descent')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()

    plt.show()


# Test the optimization methods
plot_optimization_methods1()
plot_optimization_methods2()
