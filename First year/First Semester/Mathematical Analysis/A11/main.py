import numpy as np
import matplotlib.pyplot as plt

A_min = np.array([[2, 1],
                  [1, 2]])

A_max = np.array([[-2, -1],
                  [-1, -2]])

A_saddle = np.array([[1, 0],
                     [0, -1]])


def f(x, A):
    return 0.5 * np.dot(x.T, np.dot(A, x))


def df(x, A):
    return np.dot(A, x)


def plot_surface_contour_gradient(A, title):
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = f(np.array([X[i, j], Y[i, j]]), A)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax.set_title(title)

    # Plot contour lines
    plt.contour(X, Y, Z, levels=10, colors='k')

    # Plot gradient vectors at three different points
    points = np.array([[2, 2],
                       [-2, -2],
                       [0, 0]])
    for point in points:
        grad = df(point, A)
        ax.quiver(point[0], point[1], f(point, A), grad[0], grad[1], 0.1, color='r', length=0.5, normalize=True)

    plt.show()


# Plot for a unique minimum
plot_surface_contour_gradient(A_min, 'Unique Minimum')

# Plot for a unique maximum
plot_surface_contour_gradient(A_max, 'Unique Maximum')

# Plot for a unique saddle point
plot_surface_contour_gradient(A_saddle, 'Unique Saddle Point')
