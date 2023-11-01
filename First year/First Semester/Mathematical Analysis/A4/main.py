import math
import matplotlib.pyplot as plt


# Define the original series
def original_series(number_of_terms):
    total = 0
    _partial_sums = []
    for n in range(1, number_of_terms + 1):
        total += (-1) ** (n + 1) / n
        _partial_sums.append(total)
    return _partial_sums


# Define a function to compute a rearranged series
def rearranged_series(number_of_terms, p_terms, q_terms):
    total = 0
    _partial_sums = []
    for n in range(1, number_of_terms + 1):
        if n % (p_terms + q_terms) <= p_terms:
            total += (-1) ** (n + 1) / n
        _partial_sums.append(total)
    return _partial_sums


# Values of N to consider
N_values = [10000, 20000, 50000]

# Define different p and q values for rearranged series
rearrangement_params = [(2, 1), (1, 2), (3, 2), (2, 3), (2, 5), (5, 2)]

for p, q in rearrangement_params:
    for N in N_values:
        partial_sums = rearranged_series(N, p, q)
        plt.plot(range(1, N + 1), partial_sums, label=f'Rearranged (p={p}, q={q}), N={N}')

# Plot the results
plt.axhline(y=math.log(2), color='red', linestyle='--', label='ln(2)')
plt.xlabel('Number of terms (n)')
plt.ylabel('Partial Sums')
plt.legend()
plt.title('Convergence of the Series and Rearranged Series with Different p and q')
plt.grid(True)
plt.show()
