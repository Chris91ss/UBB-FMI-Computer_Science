#include <cuda_runtime.h>
#include <device_launch_parameters.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <vector>
#include <algorithm>
#include <iostream>
#include "polynomial_cuda.h"

// ==================== CUDA ERROR CHECKING ====================

#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            std::cerr << "CUDA error at " << __FILE__ << ":" << __LINE__ \
                      << " - " << cudaGetErrorString(err) << " (code: " << err << ")" << std::endl; \
            std::cerr << "Operation: " << #call << std::endl; \
            exit(1); \
        } \
    } while(0)

#define CUDA_CHECK_KERNEL() \
    do { \
        cudaError_t err = cudaGetLastError(); \
        if (err != cudaSuccess) { \
            std::cerr << "CUDA kernel launch error: " << cudaGetErrorString(err) << " (code: " << err << ")" << std::endl; \
            exit(1); \
        } \
        err = cudaDeviceSynchronize(); \
        if (err != cudaSuccess) { \
            std::cerr << "CUDA sync error: " << cudaGetErrorString(err) << " (code: " << err << ")" << std::endl; \
            exit(1); \
        } \
    } while(0)

// ==================== CUDA KERNELS ====================

/**
 * CUDA kernel for regular O(n²) polynomial multiplication.
 * Each thread computes one coefficient of the result polynomial.
 * 
 * For result coefficient k, we need to sum all products poly1[i] * poly2[j]
 * where i + j = k.
 * 
 * Synchronization: No explicit synchronization needed - each thread writes
 * to a different memory location (result[k]). CUDA guarantees atomicity
 * of individual memory writes.
 */
__global__ void regular_multiply_kernel(const int* poly1, int n1,
                                        const int* poly2, int n2,
                                        int* result, int result_len) {
    // Each thread computes one coefficient of the result
    int k = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (k < result_len) {
        int sum = 0;
        
        // For coefficient k, find all pairs (i, j) such that i + j = k
        // i ranges from max(0, k - n2 + 1) to min(n1, k + 1)
        int i_start = (0 > (k - n2 + 1)) ? 0 : (k - n2 + 1);
        int i_end = (n1 < (k + 1)) ? n1 : (k + 1);
        
        for (int i = i_start; i < i_end; i++) {
            int j = k - i;
            if (j >= 0 && j < n2) {
                sum += poly1[i] * poly2[j];
            }
        }
        
        result[k] = sum;
    }
}

/**
 * CUDA kernel for regular multiplication using a different approach:
 * Each thread computes all contributions from one coefficient of poly1.
 * This requires atomic operations for synchronization.
 */
__global__ void regular_multiply_atomic_kernel(const int* poly1, int n1,
                                                const int* poly2, int n2,
                                                int* result, int result_len) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (i < n1) {
        // For each coefficient in poly1, multiply with all coefficients in poly2
        for (int j = 0; j < n2; j++) {
            int k = i + j;
            if (k < result_len) {
                // Atomic addition to handle concurrent writes
                atomicAdd(&result[k], poly1[i] * poly2[j]);
            }
        }
    }
}

/**
 * Helper kernel to add two polynomials (used in Karatsuba)
 */
__global__ void add_polynomials_kernel(const int* poly1, int len1,
                                       const int* poly2, int len2,
                                       int* result, int result_len) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < result_len) {
        int val1 = (idx < len1) ? poly1[idx] : 0;
        int val2 = (idx < len2) ? poly2[idx] : 0;
        result[idx] = val1 + val2;
    }
}

/**
 * Helper kernel to subtract two polynomials (used in Karatsuba)
 */
__global__ void subtract_polynomials_kernel(const int* poly1, int len1,
                                            const int* poly2, int len2,
                                            int* result, int result_len) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < result_len) {
        int val1 = (idx < len1) ? poly1[idx] : 0;
        int val2 = (idx < len2) ? poly2[idx] : 0;
        result[idx] = val1 - val2;
    }
}

/**
 * Helper kernel to shift polynomial (multiply by x^shift)
 */
__global__ void shift_polynomial_kernel(const int* poly, int poly_len,
                                        int* result, int result_len, int shift) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (idx < result_len) {
        if (idx >= shift && idx < shift + poly_len) {
            result[idx] = poly[idx - shift];
        } else {
            result[idx] = 0;
        }
    }
}

// ==================== HOST FUNCTIONS ====================

/**
 * Regular O(n²) polynomial multiplication using CUDA.
 * 
 * Algorithm:
 * - Each thread computes one coefficient of the result polynomial
 * - For coefficient k, thread sums all products poly1[i] * poly2[j] where i + j = k
 * 
 * Synchronization:
 * - No explicit synchronization needed - each thread writes to a unique location
 * - CUDA guarantees atomicity of individual memory writes
 */
float cuda_regular_multiply(const std::vector<int>& poly1,
                            const std::vector<int>& poly2,
                            std::vector<int>& result) {
    int n1 = poly1.size();
    int n2 = poly2.size();
    int result_len = n1 + n2 - 1;
    
    result.resize(result_len, 0);
    
    // Allocate device memory
    int *d_poly1, *d_poly2, *d_result;
    size_t poly1_size = n1 * sizeof(int);
    size_t poly2_size = n2 * sizeof(int);
    size_t result_size = result_len * sizeof(int);
    
    CUDA_CHECK(cudaMalloc(&d_poly1, poly1_size));
    CUDA_CHECK(cudaMalloc(&d_poly2, poly2_size));
    CUDA_CHECK(cudaMalloc(&d_result, result_size));
    
    // Copy input to device
    CUDA_CHECK(cudaMemcpy(d_poly1, poly1.data(), poly1_size, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_poly2, poly2.data(), poly2_size, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemset(d_result, 0, result_size));
    
    // Configure kernel launch parameters
    int threadsPerBlock = 256;
    int blocksPerGrid = (result_len + threadsPerBlock - 1) / threadsPerBlock;
    
    // Create CUDA events for timing
    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));
    
    // Launch kernel
    CUDA_CHECK(cudaEventRecord(start));
    regular_multiply_kernel<<<blocksPerGrid, threadsPerBlock>>>(
        d_poly1, n1, d_poly2, n2, d_result, result_len);
    
    // Check for kernel launch errors immediately
    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        std::cerr << "Kernel launch error: " << cudaGetErrorString(err) << std::endl;
        std::cerr << "Blocks: " << blocksPerGrid << ", Threads: " << threadsPerBlock 
                  << ", Result len: " << result_len << std::endl;
        exit(1);
    }
    
    // Synchronize to ensure kernel completes
    err = cudaDeviceSynchronize();
    if (err != cudaSuccess) {
        std::cerr << "Device sync error: " << cudaGetErrorString(err) << std::endl;
        exit(1);
    }
    
    CUDA_CHECK(cudaEventRecord(stop));
    
    // Wait for kernel to complete
    CUDA_CHECK(cudaEventSynchronize(stop));
    
    // Calculate elapsed time
    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));
    
    // Copy result back to host
    err = cudaMemcpy(result.data(), d_result, result_size, cudaMemcpyDeviceToHost);
    if (err != cudaSuccess) {
        std::cerr << "Memcpy error: " << cudaGetErrorString(err) << std::endl;
        exit(1);
    }
    
    
    // Cleanup
    CUDA_CHECK(cudaFree(d_poly1));
    CUDA_CHECK(cudaFree(d_poly2));
    CUDA_CHECK(cudaFree(d_result));
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));
    
    return milliseconds / 1000.0f; // Convert to seconds
}

/**
 * Karatsuba polynomial multiplication using CUDA.
 * 
 * Algorithm:
 * - Divide and conquer: split polynomials into high and low parts
 * - Compute three products recursively: z0 = low1*low2, z2 = high1*high2, 
 *   z1 = (low1+high1)*(low2+high2)
 * - Combine: result = z0 + z1*x^mid - z0*x^mid - z2*x^mid + z2*x^(2*mid)
 * 
 * Synchronization:
 * - Recursive calls are executed sequentially on host
 * - Each CUDA kernel call uses the same synchronization as regular multiply
 * - Helper kernels (add, subtract, shift) use the same per-thread approach
 */
float cuda_karatsuba_multiply(const std::vector<int>& poly1,
                              const std::vector<int>& poly2,
                              std::vector<int>& result,
                              int threshold) {
    // Base case: use regular multiplication for small polynomials
    if (poly1.size() < threshold || poly2.size() < threshold) {
        return cuda_regular_multiply(poly1, poly2, result);
    }
    
    // Make both polynomials the same length
    int max_len = std::max(poly1.size(), poly2.size());
    std::vector<int> poly1_padded = poly1;
    std::vector<int> poly2_padded = poly2;
    poly1_padded.resize(max_len, 0);
    poly2_padded.resize(max_len, 0);
    
    // Split point
    int mid = max_len / 2;
    
    // Split polynomials
    std::vector<int> low1(poly1_padded.begin(), poly1_padded.begin() + mid);
    std::vector<int> high1(poly1_padded.begin() + mid, poly1_padded.end());
    std::vector<int> low2(poly2_padded.begin(), poly2_padded.begin() + mid);
    std::vector<int> high2(poly2_padded.begin() + mid, poly2_padded.end());
    
    // Recursive calls
    std::vector<int> z0, z2, z1;
    float time_z0 = cuda_karatsuba_multiply(low1, low2, z0, threshold);
    float time_z2 = cuda_karatsuba_multiply(high1, high2, z2, threshold);
    
    // Compute (low1 + high1) and (low2 + high2)
    int max_sum_len1 = std::max(low1.size(), high1.size());
    int max_sum_len2 = std::max(low2.size(), high2.size());
    std::vector<int> sum1(max_sum_len1, 0);
    std::vector<int> sum2(max_sum_len2, 0);
    
    for (size_t i = 0; i < low1.size(); i++) sum1[i] += low1[i];
    for (size_t i = 0; i < high1.size(); i++) sum1[i] += high1[i];
    for (size_t i = 0; i < low2.size(); i++) sum2[i] += low2[i];
    for (size_t i = 0; i < high2.size(); i++) sum2[i] += high2[i];
    
    float time_z1 = cuda_karatsuba_multiply(sum1, sum2, z1, threshold);
    
    // z1 = z1 - z0 - z2
    std::vector<int> z1_temp;
    cuda_subtract_polynomials(z1, z0, z1_temp);
    cuda_subtract_polynomials(z1_temp, z2, z1);
    
    // Combine results: result = z0 + z1 * x^mid + z2 * x^(2*mid)
    int result_size = poly1.size() + poly2.size() - 1;
    result.resize(result_size, 0);
    
    // Add z0
    for (size_t i = 0; i < z0.size() && i < (size_t)result_size; i++) {
        result[i] += z0[i];
    }
    
    // Add z1 * x^mid
    for (size_t i = 0; i < z1.size(); i++) {
        int idx = i + mid;
        if (idx < (size_t)result_size) {
            result[idx] += z1[i];
        }
    }
    
    // Add z2 * x^(2*mid)
    for (size_t i = 0; i < z2.size(); i++) {
        int idx = i + 2 * mid;
        if (idx < (size_t)result_size) {
            result[idx] += z2[i];
        }
    }
    
    return time_z0 + time_z1 + time_z2;
}

/**
 * Helper function to subtract two polynomials using CUDA
 */
void cuda_subtract_polynomials(const std::vector<int>& poly1,
                               const std::vector<int>& poly2,
                               std::vector<int>& result) {
    int max_len = std::max(poly1.size(), poly2.size());
    result.resize(max_len, 0);
    
    int *d_poly1, *d_poly2, *d_result;
    size_t poly1_size = poly1.size() * sizeof(int);
    size_t poly2_size = poly2.size() * sizeof(int);
    size_t result_size = max_len * sizeof(int);
    
    CUDA_CHECK(cudaMalloc(&d_poly1, poly1_size));
    CUDA_CHECK(cudaMalloc(&d_poly2, poly2_size));
    CUDA_CHECK(cudaMalloc(&d_result, result_size));
    
    CUDA_CHECK(cudaMemcpy(d_poly1, poly1.data(), poly1_size, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_poly2, poly2.data(), poly2_size, cudaMemcpyHostToDevice));
    
    int threadsPerBlock = 256;
    int blocksPerGrid = (max_len + threadsPerBlock - 1) / threadsPerBlock;
    
    subtract_polynomials_kernel<<<blocksPerGrid, threadsPerBlock>>>(
        d_poly1, poly1.size(), d_poly2, poly2.size(), d_result, max_len);
    CUDA_CHECK_KERNEL();
    
    CUDA_CHECK(cudaMemcpy(result.data(), d_result, result_size, cudaMemcpyDeviceToHost));
    
    CUDA_CHECK(cudaFree(d_poly1));
    CUDA_CHECK(cudaFree(d_poly2));
    CUDA_CHECK(cudaFree(d_result));
}

// ==================== CPU IMPLEMENTATIONS FOR COMPARISON ====================

/**
 * CPU regular O(n²) polynomial multiplication (sequential)
 */
std::vector<int> cpu_regular_multiply(const std::vector<int>& poly1,
                                     const std::vector<int>& poly2) {
    int n1 = poly1.size();
    int n2 = poly2.size();
    int result_len = n1 + n2 - 1;
    std::vector<int> result(result_len, 0);
    
    for (int i = 0; i < n1; i++) {
        for (int j = 0; j < n2; j++) {
            result[i + j] += poly1[i] * poly2[j];
        }
    }
    
    return result;
}

/**
 * CPU Karatsuba polynomial multiplication (sequential)
 */
std::vector<int> cpu_karatsuba_multiply(const std::vector<int>& poly1,
                                       const std::vector<int>& poly2) {
    // Base case
    if (poly1.size() < 2 || poly2.size() < 2) {
        return cpu_regular_multiply(poly1, poly2);
    }
    
    // Make both polynomials the same length
    int max_len = std::max(poly1.size(), poly2.size());
    std::vector<int> poly1_padded = poly1;
    std::vector<int> poly2_padded = poly2;
    poly1_padded.resize(max_len, 0);
    poly2_padded.resize(max_len, 0);
    
    // Split point
    int mid = max_len / 2;
    
    // Split polynomials
    std::vector<int> low1(poly1_padded.begin(), poly1_padded.begin() + mid);
    std::vector<int> high1(poly1_padded.begin() + mid, poly1_padded.end());
    std::vector<int> low2(poly2_padded.begin(), poly2_padded.begin() + mid);
    std::vector<int> high2(poly2_padded.begin() + mid, poly2_padded.end());
    
    // Recursive calls
    std::vector<int> z0 = cpu_karatsuba_multiply(low1, low2);
    std::vector<int> z2 = cpu_karatsuba_multiply(high1, high2);
    
    // Compute (low1 + high1) and (low2 + high2)
    int max_sum_len1 = std::max(low1.size(), high1.size());
    int max_sum_len2 = std::max(low2.size(), high2.size());
    std::vector<int> sum1(max_sum_len1, 0);
    std::vector<int> sum2(max_sum_len2, 0);
    
    for (size_t i = 0; i < low1.size(); i++) sum1[i] += low1[i];
    for (size_t i = 0; i < high1.size(); i++) sum1[i] += high1[i];
    for (size_t i = 0; i < low2.size(); i++) sum2[i] += low2[i];
    for (size_t i = 0; i < high2.size(); i++) sum2[i] += high2[i];
    
    std::vector<int> z1 = cpu_karatsuba_multiply(sum1, sum2);
    
    // z1 = z1 - z0 - z2
    for (size_t i = 0; i < z0.size() && i < z1.size(); i++) {
        z1[i] -= z0[i];
    }
    for (size_t i = 0; i < z2.size() && i < z1.size(); i++) {
        z1[i] -= z2[i];
    }
    
    // Combine results
    int result_size = poly1.size() + poly2.size() - 1;
    std::vector<int> result(result_size, 0);
    
    for (size_t i = 0; i < z0.size() && i < (size_t)result_size; i++) {
        result[i] += z0[i];
    }
    for (size_t i = 0; i < z1.size(); i++) {
        int idx = i + mid;
        if (idx < (size_t)result_size) {
            result[idx] += z1[i];
        }
    }
    for (size_t i = 0; i < z2.size(); i++) {
        int idx = i + 2 * mid;
        if (idx < (size_t)result_size) {
            result[idx] += z2[i];
        }
    }
    
    return result;
}

// ==================== UTILITY FUNCTIONS ====================

/**
 * Generate a random polynomial of given degree
 */
std::vector<int> generate_random_polynomial(int degree, int min_coeff, int max_coeff) {
    std::vector<int> poly(degree + 1);
    srand(time(NULL));
    for (int i = 0; i <= degree; i++) {
        poly[i] = rand() % (max_coeff - min_coeff + 1) + min_coeff;
    }
    return poly;
}

/**
 * Check if two polynomials are equal
 */
bool polynomials_equal(const std::vector<int>& poly1, const std::vector<int>& poly2) {
    if (poly1.size() != poly2.size()) {
        return false;
    }
    for (size_t i = 0; i < poly1.size(); i++) {
        if (poly1[i] != poly2[i]) {
            return false;
        }
    }
    return true;
}

/**
 * Print polynomial
 */
void print_polynomial(const std::vector<int>& poly) {
    bool first = true;
    for (int i = poly.size() - 1; i >= 0; i--) {
        if (poly[i] != 0) {
            if (!first) std::cout << " + ";
            if (i == 0) {
                std::cout << poly[i];
            } else if (i == 1) {
                std::cout << poly[i] << "x";
            } else {
                std::cout << poly[i] << "x^" << i;
            }
            first = false;
        }
    }
    if (first) std::cout << "0";
    std::cout << std::endl;
}


