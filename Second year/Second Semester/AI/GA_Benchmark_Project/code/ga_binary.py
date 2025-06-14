"""
Binary-Encoded Genetic Algorithm for 2D minimization.
Supports:
  - 1-point and 2-point crossover on bitstrings
  - Bit-flip mutation
  - Minimization of a function defined in functions.py
"""

import numpy as np
from typing import Callable, List, Tuple


class BinaryGA:
    def __init__(
        self,
        func: Callable[[float, float], float],    # Objective function (x,y) → scalar
        bounds: List[Tuple[float, float]],       # [(x_min, x_max), (y_min, y_max)]
        bits_per_var: int = 16,                  # Number of bits per variable
        pop_size: int = 50,
        num_gens: int = 200,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.01,
        crossover_type: str = 'one_point'        # 'one_point' or 'two_point'
    ):
        self.func = func
        self.bounds = bounds
        self.bits_per_var = bits_per_var
        self.chrom_length = bits_per_var * 2    # total bits for [x,y]
        self.pop_size = pop_size
        self.num_gens = num_gens
        self.Pc = crossover_rate
        self.Pm = mutation_rate
        self.cross_type = crossover_type.lower()

        # Internal state: population of shape (pop_size, chrom_length), dtype=np.uint8
        self.population = self._initialize_population()
        self.fitness = np.zeros(self.pop_size)

    def _initialize_population(self) -> np.ndarray:
        """
        Randomly initialize a binary matrix of shape (pop_size, chrom_length).
        Each entry is 0 or 1 with equal probability.
        """
        return np.random.randint(0, 2, size=(self.pop_size, self.chrom_length), dtype=np.uint8)

    def _binary_to_real(self, bits: np.ndarray, var_index: int) -> float:
        """
        Convert a slice of bits to a real number in the domain of variable var_index (0 or 1).
        bits: length = chrom_length
        var_index=0 → first bits_per_var decode to x
        var_index=1 → second bits_per_var decode to y
        """
        start = var_index * self.bits_per_var
        end = start + self.bits_per_var
        sub = bits[start:end]   # e.g. array of 0/1 of length bits_per_var
        # Convert binary array to integer
        integer_value = 0
        for bit in sub:
            integer_value = (integer_value << 1) | int(bit)
        max_int = 2**self.bits_per_var - 1
        lo, hi = self.bounds[var_index]
        # Linear mapping: [0, max_int] → [lo, hi]
        return lo + (hi - lo) * integer_value / max_int

    def _decode(self, individual: np.ndarray) -> Tuple[float, float]:
        """
        Decode a full binary chromosome into (x, y).
        """
        x = self._binary_to_real(individual, var_index=0)
        y = self._binary_to_real(individual, var_index=1)
        return x, y

    def evaluate_fitness(self) -> None:
        """
        For each individual, decode (x,y) and evaluate func(x,y).
        Store the result in self.fitness (lower is better).
        """
        for i in range(self.pop_size):
            x, y = self._decode(self.population[i])
            self.fitness[i] = self.func(x, y)

    def select_parents(self) -> np.ndarray:
        """
        Tournament selection (size=2). Returns an array of selected parents
        shape (pop_size, chrom_length).
        """
        parents = np.zeros_like(self.population)
        for i in range(self.pop_size):
            i1, i2 = np.random.choice(self.pop_size, size=2, replace=False)
            if self.fitness[i1] < self.fitness[i2]:
                parents[i] = self.population[i1].copy()
            else:
                parents[i] = self.population[i2].copy()
        return parents

    def crossover(self, p1: np.ndarray, p2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform 1-point or 2-point crossover on two parent bit arrays.
        Returns two child bit arrays (each length=chrom_length).
        """
        # With probability 1−Pc, no crossover (just copy parents)
        if np.random.rand() > self.Pc:
            return p1.copy(), p2.copy()

        L = self.chrom_length
        if self.cross_type == 'one_point':
            # Choose one crossover point in [1, L−1]
            point = np.random.randint(1, L)
            c1 = np.concatenate([p1[:point], p2[point:]])
            c2 = np.concatenate([p2[:point], p1[point:]])
        elif self.cross_type == 'two_point':
            # Choose two points a < b in [1, L−1]
            a = np.random.randint(1, L - 1)
            b = np.random.randint(a + 1, L)
            c1 = (
                np.concatenate([p1[:a], p2[a:b], p1[b:]])
            )
            c2 = (
                np.concatenate([p2[:a], p1[a:b], p2[b:]])
            )
        else:
            raise ValueError(f"Unknown crossover type: {self.cross_type}")

        return c1.astype(np.uint8), c2.astype(np.uint8)

    def mutate(self, individual: np.ndarray) -> np.ndarray:
        """
        Bit-flip mutation: each bit flips (0↔1) with probability Pm.
        """
        for i in range(self.chrom_length):
            if np.random.rand() < self.Pm:
                individual[i] = 1 - individual[i]
        return individual

    def run(self) -> Tuple[np.ndarray, List[float]]:
        """
        Main GA loop. Returns:
          - best_individual: binary array of length chrom_length
          - best_history: list of length num_gens of the best objective found
        """
        # 1. Evaluate initial fitness
        self.evaluate_fitness()
        best_history: List[float] = []

        for gen in range(self.num_gens):
            # 2. Parent selection
            parents = self.select_parents()

            # 3. Generate offspring via crossover & mutation
            offspring = []
            for i in range(0, self.pop_size, 2):
                p1, p2 = parents[i], parents[i + 1]
                c1, c2 = self.crossover(p1, p2)
                c1 = self.mutate(c1)
                c2 = self.mutate(c2)
                offspring.append(c1)
                offspring.append(c2)

            self.population = np.array(offspring, dtype=np.uint8)

            # 4. Evaluate new fitness
            self.evaluate_fitness()

            # 5. Record best for this generation
            best_idx = int(np.argmin(self.fitness))
            best_f = float(self.fitness[best_idx])
            best_history.append(best_f)

        # Return the best binary string and its history
        best_idx = int(np.argmin(self.fitness))
        best_individual = self.population[best_idx].copy()
        return best_individual, best_history


# Example usage (if run as script):
if __name__ == "__main__":
    from functions import six_hump_camelback

    # Set up GA for Six-Hump Camelback on [-3,3]×[-2,2]
    ga = BinaryGA(
        func=six_hump_camelback,
        bounds=[(-3, 3), (-2, 2)],
        bits_per_var=16,
        pop_size=50,
        num_gens=200,
        crossover_rate=0.8,
        mutation_rate=0.01,
        crossover_type='two_point'
    )
    best_bin, history = ga.run()
    # Decode best to real
    x_best, y_best = ga._decode(best_bin)
    print("Best (x, y):", x_best, y_best, "  f(x,y):", six_hump_camelback(x_best, y_best))
