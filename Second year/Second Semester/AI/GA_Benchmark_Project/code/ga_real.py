"""
Real-Valued Genetic Algorithm implementation.
Supports:
  - Arithmetic crossover
  - BLX-alpha crossover
  - Gaussian mutation
  - Minimization of a 2D function
"""

import numpy as np
from typing import Callable, List, Tuple


class RealValuedGA:
    def __init__(
        self,
        func: Callable[[float, float], float],   # Objective: (x, y) → scalar
        bounds: List[Tuple[float, float]],      # [(x_min, x_max), (y_min, y_max)]
        pop_size: int = 50,
        num_gens: int = 200,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.1,
        crossover_type: str = 'arithmetic',     # 'arithmetic' or 'blx'
        blx_alpha: float = 0.5,
        sigma: float = 0.1                       # Standard deviation for Gaussian mutation
    ):
        self.func = func
        self.bounds = bounds
        self.pop_size = pop_size
        self.num_gens = num_gens
        self.Pc = crossover_rate
        self.Pm = mutation_rate
        self.cross_type = crossover_type.lower()
        self.alpha = blx_alpha
        self.sigma = sigma

        # Internal state
        self.population = self._initialize_population()
        self.fitness = np.zeros(self.pop_size)

    def _initialize_population(self) -> np.ndarray:
        """
        Create an initial population of shape (pop_size, 2),
        sampling uniformly within each bound.
        """
        pop = np.zeros((self.pop_size, 2))
        for d in range(2):
            low, high = self.bounds[d]
            pop[:, d] = np.random.uniform(low, high, size=self.pop_size)
        return pop

    def evaluate_fitness(self) -> None:
        """
        Evaluate the objective function for each individual
        and store in self.fitness (lower is better).
        """
        for i in range(self.pop_size):
            x, y = self.population[i]
            self.fitness[i] = self.func(x, y)

    def select_parents(self) -> np.ndarray:
        """
        Tournament selection (size=2): return an array of selected parents
        of shape (pop_size, 2).
        """
        parents = np.zeros_like(self.population)
        for i in range(self.pop_size):
            i1, i2 = np.random.choice(self.pop_size, size=2, replace=False)
            if self.fitness[i1] < self.fitness[i2]:
                parents[i] = self.population[i1]
            else:
                parents[i] = self.population[i2]
        return parents

    def crossover(self, p1: np.ndarray, p2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Produce two children from parents p1, p2 using the chosen crossover method.
        Each parent is a length-2 array [x, y].
        """
        # With probability 1−Pc, do no crossover (just copy parents)
        if np.random.rand() > self.Pc:
            return p1.copy(), p2.copy()

        if self.cross_type == 'arithmetic':
            alpha = np.random.rand()
            c1 = alpha * p1 + (1 - alpha) * p2
            c2 = (1 - alpha) * p1 + alpha * p2
        elif self.cross_type == 'blx':
            c1 = np.zeros(2)
            c2 = np.zeros(2)
            for d in range(2):
                x1, x2 = p1[d], p2[d]
                mn, mx = min(x1, x2), max(x1, x2)
                I = mx - mn
                low = mn - self.alpha * I
                high = mx + self.alpha * I
                c1[d] = np.random.uniform(low, high)
                c2[d] = np.random.uniform(low, high)
        else:
            raise ValueError(f"Unknown crossover type: {self.cross_type}")

        # Clip children to domain bounds
        for d in range(2):
            lo, hi = self.bounds[d]
            c1[d] = np.clip(c1[d], lo, hi)
            c2[d] = np.clip(c2[d], lo, hi)

        return c1, c2

    def mutate(self, individual: np.ndarray) -> np.ndarray:
        """
        Apply Gaussian mutation to a single individual (length-2 array).
        Each gene has probability Pm to receive N(0, σ²) noise.
        """
        for d in range(2):
            if np.random.rand() < self.Pm:
                individual[d] += np.random.normal(0, self.sigma)
                # Clip after mutation
                lo, hi = self.bounds[d]
                individual[d] = np.clip(individual[d], lo, hi)
        return individual

    def run(self) -> Tuple[np.ndarray, List[float]]:
        """
        Main GA loop. Returns:
          - best_individual: np.ndarray shape (2,) (the x,y that achieved best fitness)
          - best_history: list of length num_gens, recording best fitness at each generation
        """
        # Evaluate initial fitness
        self.evaluate_fitness()
        best_history: List[float] = []

        for gen in range(self.num_gens):
            # 1. Select parents
            parents = self.select_parents()

            # 2. Create offspring via crossover & mutation
            offspring = []
            for i in range(0, self.pop_size, 2):
                p1, p2 = parents[i], parents[i + 1]
                c1, c2 = self.crossover(p1, p2)
                c1 = self.mutate(c1)
                c2 = self.mutate(c2)
                offspring.append(c1)
                offspring.append(c2)

            # Update population
            self.population = np.array(offspring)

            # 3. Re-evaluate fitness
            self.evaluate_fitness()

            # 4. Record best for this generation
            best_idx = int(np.argmin(self.fitness))
            best_f = float(self.fitness[best_idx])
            best_history.append(best_f)

        # At end, return the overall best individual & history
        best_idx = int(np.argmin(self.fitness))
        best_individual = self.population[best_idx].copy()
        return best_individual, best_history


# Example usage (if run as script):
if __name__ == "__main__":
    from functions import rastrigin

    # Set up GA for Rastrigin on [-5.12,5.12]^2
    ga = RealValuedGA(
        func=rastrigin,
        bounds=[(-5.12, 5.12), (-5.12, 5.12)],
        pop_size=50,
        num_gens=200,
        crossover_rate=0.8,
        mutation_rate=0.1,
        crossover_type='blx',
        blx_alpha=0.3,
        sigma=0.05
    )
    best_xy, history = ga.run()
    print("Best solution:", best_xy, "f-value:", rastrigin(*best_xy))
