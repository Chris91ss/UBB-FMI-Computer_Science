"""
Orchestrates full factorial experiments for:
  - Rastrigin (2D)
  - Six-Hump Camelback (2D)

For each function:
  - Run BinaryGA with 1-point & 2-point crossover
  - Run RealValuedGA with arithmetic & BLX-alpha crossover

Each configuration is run for N_REPS independent seeds.
Results (best value, maybe generation of best) are saved to CSV in ../data/.
"""

import os
import csv
import json
import numpy as np
from datetime import datetime

# Import your GA classes and functions
from functions import rastrigin, six_hump_camelback
from ga_real import RealValuedGA
from ga_binary import BinaryGA

# 1. Set global experiment parameters
TOTAL_EVALUATIONS = 10000   # e.g. population_size * num_generations
N_REPS = 30                 # number of independent runs per configuration

# 2. Define your configurations in a list-of-dicts
configs = [
    # ------- Rastrigin, Binary, 1-point -------
    {
        'func_name': 'rastrigin',
        'func': rastrigin,
        'encoding': 'binary',
        'crossover': 'one_point',
        'bits_per_var': 16,
        'pop_size': 50,       # 50 * 200 = 10000 evaluations
        'num_gens': 200,
        'mutation_rate': 0.01
    },
    # ------- Rastrigin, Binary, 2-point -------
    {
        'func_name': 'rastrigin',
        'func': rastrigin,
        'encoding': 'binary',
        'crossover': 'two_point',
        'bits_per_var': 16,
        'pop_size': 50,
        'num_gens': 200,
        'mutation_rate': 0.01
    },
    # ------- Rastrigin, Real, Arithmetic -------
    {
        'func_name': 'rastrigin',
        'func': rastrigin,
        'encoding': 'real',
        'crossover': 'arithmetic',
        'pop_size': 50,
        'num_gens': 200,
        'mutation_rate': 0.1,
        'blx_alpha': None   # not used for arithmetic
    },
    # ------- Rastrigin, Real, BLX-alpha -------
    {
        'func_name': 'rastrigin',
        'func': rastrigin,
        'encoding': 'real',
        'crossover': 'blx',
        'pop_size': 50,
        'num_gens': 200,
        'mutation_rate': 0.1,
        'blx_alpha': 0.5
    },
    # ------- Six-Hump, Binary, 1-point -------
    {
        'func_name': 'six_hump',
        'func': six_hump_camelback,
        'encoding': 'binary',
        'crossover': 'one_point',
        'bits_per_var': 16,
        'pop_size': 50,
        'num_gens': 200,
        'mutation_rate': 0.01
    },
    # ------- Six-Hump, Binary, 2-point -------
    {
        'func_name': 'six_hump',
        'func': six_hump_camelback,
        'encoding': 'binary',
        'crossover': 'two_point',
        'bits_per_var': 16,
        'pop_size': 50,
        'num_gens': 200,
        'mutation_rate': 0.01
    },
    # ------- Six-Hump, Real, Arithmetic -------
    {
        'func_name': 'six_hump',
        'func': six_hump_camelback,
        'encoding': 'real',
        'crossover': 'arithmetic',
        'pop_size': 50,
        'num_gens': 200,
        'mutation_rate': 0.1,
        'blx_alpha': None
    },
    # ------- Six-Hump, Real, BLX-alpha -------
    {
        'func_name': 'six_hump',
        'func': six_hump_camelback,
        'encoding': 'real',
        'crossover': 'blx',
        'pop_size': 50,
        'num_gens': 200,
        'mutation_rate': 0.1,
        'blx_alpha': 0.5
    },
]

# 3. Create output folder for results
RESULTS_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
os.makedirs(RESULTS_DIR, exist_ok=True)

# 4. Define domain bounds for each function
BOUNDS = {
    'rastrigin': [(-5.12, 5.12), (-5.12, 5.12)],
    'six_hump': [(-3, 3), (-2, 2)]
}


def run_experiments():
    """
    For each configuration in configs[], run N_REPS runs, collect best f-values,
    and write summary CSV + detailed JSON if desired.
    """
    summary_rows = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for cfg in configs:
        func_name = cfg['func_name']
        func = cfg['func']
        encoding = cfg['encoding']
        crossover = cfg['crossover']
        pop_size = cfg['pop_size']
        num_gens = cfg['num_gens']
        mutation_rate = cfg['mutation_rate']

        # Domain bounds
        bounds = BOUNDS[func_name]

        # Build unique ID for this configuration
        cfg_id = f"{func_name}_{encoding}_{crossover}"

        # Store best values from each repetition
        best_values = []

        for rep in range(1, N_REPS + 1):
            seed = rep  # you can choose any seeding strategy
            np.random.seed(seed)

            if encoding == 'binary':
                bits = cfg['bits_per_var']
                ga = BinaryGA(
                    func=func,
                    bounds=bounds,
                    bits_per_var=bits,
                    pop_size=pop_size,
                    num_gens=num_gens,
                    crossover_rate=0.8,
                    mutation_rate=mutation_rate,
                    crossover_type=crossover
                )
                best_ind, history = ga.run()
                x_best, y_best = ga._decode(best_ind)
                f_best = func(x_best, y_best)

            else:  # real-valued
                blx_alpha = cfg.get('blx_alpha', 0.5)
                ga = RealValuedGA(
                    func=func,
                    bounds=bounds,
                    pop_size=pop_size,
                    num_gens=num_gens,
                    crossover_rate=0.8,
                    mutation_rate=mutation_rate,
                    crossover_type=crossover,
                    blx_alpha=blx_alpha,
                    sigma=0.1
                )
                best_xy, history = ga.run()
                f_best = func(*best_xy)

            best_values.append(f_best)

        # Summarize results for this config
        best_min = float(np.min(best_values))
        best_mean = float(np.mean(best_values))
        best_std = float(np.std(best_values))

        # Add a row to summary
        summary_rows.append({
            'config_id': cfg_id,
            'func_name': func_name,
            'encoding': encoding,
            'crossover': crossover,
            'pop_size': pop_size,
            'num_gens': num_gens,
            'mutation_rate': mutation_rate,
            'best_min': best_min,
            'best_mean': best_mean,
            'best_std': best_std
        })

        # save detailed best_values to JSON
        detail_path = os.path.join(RESULTS_DIR, f"{cfg_id}_values_{timestamp}.json")
        with open(detail_path, 'w') as fp:
            json.dump(best_values, fp, indent=2)

        print(f"Finished {cfg_id}: min={best_min:.6f}, mean={best_mean:.6f}, std={best_std:.6f}")

    # Write summary CSV
    csv_path = os.path.join(RESULTS_DIR, f"summary_{timestamp}.csv")
    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = list(summary_rows[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary_rows:
            writer.writerow(row)

    print(f"Summary CSV written to: {csv_path}")


if __name__ == "__main__":
    run_experiments()
