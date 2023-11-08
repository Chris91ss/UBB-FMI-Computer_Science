import numpy as np
import matplotlib.pyplot as plt


def cantor_function(x_value):
    result = np.zeros_like(x_value)
    for i in range(len(x_value)):
        value = x_value[i]
        while value > 0:
            if value < 1/3:
                result[i] += 0
            elif value >= 2/3:
                result[i] += 1/2
            else:
                result[i] += 1/2
            value -= 1/3  # Instead of multiplication, subtract 1/3
    return result


x = np.linspace(0, 1, 10000)
y = cantor_function(x)

plt.plot(x, y, color='blue')
plt.title("Graph of the Cantor Function")
plt.xlabel("x")
plt.ylabel("Cantor Function(x)")
plt.show()
