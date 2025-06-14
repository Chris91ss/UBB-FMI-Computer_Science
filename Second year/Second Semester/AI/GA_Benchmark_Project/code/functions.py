import numpy as np


def rastrigin(x: float, y: float) -> float:
    """
    Rastrigin function (2D).

    Domain: x, y ∈ [-5.12, 5.12]
    Global minimum: f(0,0) = 0

    f(x, y) = 20 + x^2 + y^2 - 10*(cos(2πx) + cos(2πy))
    """
    return 20 + x**2 + y**2 - 10 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))


def six_hump_camelback(x: float, y: float) -> float:
    """
    Six-Hump Camelback function (2D).

    Domain: x ∈ [-3,3], y ∈ [-2,2]
    Two global minima near (±0.0898, −0.7126)

    f(x, y) = (4 − 2.1 x^2 + (x^4)/3) x^2 + x y + (−4 + 4 y^2) y^2
    """
    return (4 - 2.1 * x**2 + (x**4) / 3) * x**2 + x * y + (-4 + 4 * y**2) * y**2


def check_bounds(x: float, lower: float, upper: float) -> float:
    """
    Clips x to be within [lower, upper].
    """
    return np.clip(x, lower, upper)
