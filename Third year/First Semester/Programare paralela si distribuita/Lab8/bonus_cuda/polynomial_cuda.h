#ifndef POLYNOMIAL_CUDA_H
#define POLYNOMIAL_CUDA_H

#include <vector>

// CUDA implementations
float cuda_regular_multiply(const std::vector<int>& poly1,
                            const std::vector<int>& poly2,
                            std::vector<int>& result);

float cuda_karatsuba_multiply(const std::vector<int>& poly1,
                              const std::vector<int>& poly2,
                              std::vector<int>& result,
                              int threshold = 32);

void cuda_subtract_polynomials(const std::vector<int>& poly1,
                               const std::vector<int>& poly2,
                               std::vector<int>& result);

// CPU implementations for comparison
std::vector<int> cpu_regular_multiply(const std::vector<int>& poly1,
                                     const std::vector<int>& poly2);

std::vector<int> cpu_karatsuba_multiply(const std::vector<int>& poly1,
                                       const std::vector<int>& poly2);

// Utility functions
std::vector<int> generate_random_polynomial(int degree, int min_coeff = 1, int max_coeff = 10);
bool polynomials_equal(const std::vector<int>& poly1, const std::vector<int>& poly2);
void print_polynomial(const std::vector<int>& poly);

#endif // POLYNOMIAL_CUDA_H






