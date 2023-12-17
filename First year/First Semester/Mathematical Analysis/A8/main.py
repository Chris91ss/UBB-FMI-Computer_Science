import numpy as np
import matplotlib.pyplot as plt


# Function to check if a point is inside the p-norm unit ball
def inside_unit_ball(x, y, _p):
    return np.linalg.norm([x, y], _p) <= 1


# Function to generate and plot points inside the unit ball for a given p
def plot_unit_ball(_p):
    num_points = 1000
    points_inside = []

    for _ in range(num_points):
        x, y = np.random.uniform(-1, 1, 2)
        if inside_unit_ball(x, y, _p):
            points_inside.append((x, y))

    points_inside = np.array(points_inside).T
    plt.scatter(points_inside[0], points_inside[1], label=f'p={_p}')


# Plotting for different p-norms
norms = [1.25, 1.5, 3, 8]

plt.figure(figsize=(8, 8))

for p in norms:
    plot_unit_ball(p)

plt.title('Unit Ball in R^2 for Different p-norms')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True)
plt.show()
