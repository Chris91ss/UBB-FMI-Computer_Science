# CUDA Polynomial Multiplication

This project implements parallel polynomial multiplication algorithms using CUDA, comparing performance with CPU implementations from Lab 5.

## Overview

The project implements two polynomial multiplication algorithms:
1. **Regular O(n²) Algorithm**: Naive polynomial multiplication
2. **Karatsuba Algorithm**: Divide-and-conquer algorithm with O(n^log₂(3)) ≈ O(n^1.585) complexity

Both algorithms are implemented in CUDA for GPU acceleration and compared with their CPU counterparts.

## Algorithms

### 1. Regular O(n²) Polynomial Multiplication

#### Algorithm Description
The regular polynomial multiplication algorithm computes the product of two polynomials by:
- For each coefficient position `k` in the result polynomial
- Sum all products `poly1[i] * poly2[j]` where `i + j = k`

**Time Complexity**: O(n²) where n is the degree of the polynomials

#### CUDA Implementation
- **Kernel**: `regular_multiply_kernel`
- **Parallelization Strategy**: Each CUDA thread computes one coefficient of the result polynomial
- **Thread Mapping**: Thread with index `k` computes result coefficient at position `k`
- **Memory Access**: Each thread reads from `poly1` and `poly2` arrays and writes to a unique location in `result`

#### Synchronization
- **No explicit synchronization needed**: Each thread writes to a different memory location (`result[k]`)
- CUDA guarantees atomicity of individual memory writes
- All threads execute independently without race conditions

### 2. Karatsuba Algorithm

#### Algorithm Description
The Karatsuba algorithm uses a divide-and-conquer approach:
1. **Split**: Divide each polynomial into high and low parts at the midpoint
2. **Recurse**: Compute three products recursively:
   - `z0 = low1 * low2`
   - `z2 = high1 * high2`
   - `z1 = (low1 + high1) * (low2 + high2)`
3. **Combine**: Compute the result as:
   - `result = z0 + (z1 - z0 - z2) * x^mid + z2 * x^(2*mid)`

**Time Complexity**: O(n^log₂(3)) ≈ O(n^1.585)

#### CUDA Implementation
- **Recursive Structure**: The algorithm is implemented recursively on the host
- **Base Case**: For small polynomials (below threshold, default 32), falls back to regular multiplication
- **Helper Kernels**: Uses CUDA kernels for polynomial addition, subtraction, and shifting operations
- **Parallelization**: Each recursive call uses CUDA kernels for the actual computation

#### Synchronization
- **Recursive Calls**: Executed sequentially on the host (CUDA kernels are launched sequentially)
- **Within Each Kernel**: Same synchronization approach as regular multiplication
- **Helper Operations**: Addition, subtraction, and shifting use per-thread approach with no explicit synchronization

## File Structure

```
bonus_cuda/
├── polynomial_cuda.cu    # CUDA kernels and implementations
├── polynomial_cuda.h     # Header file with function declarations
├── main.cu               # Main program with performance tests
├── Makefile             # Build configuration
└── README.md            # This file
```

## Building the Project

### Prerequisites
- NVIDIA GPU with CUDA support
- CUDA Toolkit installed
- GCC/G++ compiler with C++11 support

### Build Instructions

1. **Check your GPU architecture**:
   ```bash
   nvidia-smi --query-gpu=compute_cap --format=csv
   ```

2. **Update Makefile** (if needed):
   - Edit the `-arch=sm_XX` flag in `Makefile` to match your GPU's compute capability
   - Common architectures:
     - sm_75: Turing (RTX 20xx, GTX 16xx)
     - sm_80: Ampere (RTX 30xx, A100)
     - sm_86: Ampere (RTX 30xx)
     - sm_89: Ada (RTX 40xx)

3. **Build the project**:
   ```bash
   make
   ```

4. **Run the program**:
   ```bash
   ./polynomial_cuda                    # Run all tests
   ./polynomial_cuda <deg1> <deg2>     # Run detailed test with specific degrees
   ```

## Usage Examples

### Run All Tests
```bash
./polynomial_cuda
```
This will:
- Run a basic functionality test
- Run performance comparison with multiple polynomial sizes
- Display results in a formatted table

### Run Custom Test
```bash
./polynomial_cuda 100 100
```
This will run a detailed test with two polynomials of degree 100.

## Performance Measurements

### Test Configuration
The performance comparison tests polynomials of various sizes:
- Small: 10×10
- Medium: 50×50
- Large: 100×100
- Very Large: 200×200
- Huge: 500×500

### Expected Results

The CUDA implementation typically shows significant speedup over CPU implementation, especially for larger polynomials. Speedup factors depend on:
- GPU architecture and compute capability
- Polynomial size (larger polynomials benefit more from parallelization)
- Memory bandwidth
- CPU vs GPU performance characteristics

### Performance Factors

1. **Polynomial Size**: Larger polynomials provide more parallelism and better GPU utilization
2. **GPU Architecture**: Newer GPUs with more CUDA cores show better performance
3. **Memory Transfer**: Initial data transfer to/from GPU adds overhead, but is amortized for large computations
4. **Algorithm Choice**: Karatsuba is faster for very large polynomials, but has more overhead for small ones

## Synchronization Details

### Regular Multiplication
- **No synchronization needed**: Each thread computes one result coefficient independently
- **Memory access pattern**: Coalesced reads from input arrays, scattered writes to result array
- **Thread independence**: Complete independence between threads

### Karatsuba Algorithm
- **Host-level synchronization**: Recursive calls are sequential (host-side)
- **Device-level synchronization**: Each kernel launch is implicitly synchronized (via `cudaEventSynchronize`)
- **Helper operations**: Addition, subtraction, and shifting use independent threads with no shared state

### CUDA Synchronization Primitives Used
- **Implicit synchronization**: `cudaEventSynchronize()` ensures kernel completion before proceeding
- **Memory barriers**: CUDA runtime ensures memory consistency between kernel launches
- **No explicit locks**: Not needed due to independent thread execution

## Comparison with CPU Implementation (Lab 5)

### CPU Implementation Characteristics
- **Regular Sequential**: O(n²) time, single-threaded
- **Regular Parallel**: O(n²) time, multi-threaded with locks for result updates
- **Karatsuba Sequential**: O(n^log₂(3)) time, recursive single-threaded
- **Karatsuba Parallel**: O(n^log₂(3)) time, parallel recursive calls using ThreadPoolExecutor

### CUDA Advantages
1. **Massive Parallelism**: Thousands of threads vs. typically 4-8 CPU threads
2. **No Lock Contention**: Each thread writes to unique memory location
3. **High Memory Bandwidth**: GPU memory bandwidth typically much higher than CPU
4. **Specialized Hardware**: GPU optimized for parallel arithmetic operations

### CUDA Disadvantages
1. **Memory Transfer Overhead**: Data must be transferred to/from GPU
2. **Small Problem Overhead**: For very small polynomials, overhead dominates
3. **Development Complexity**: More complex than CPU threading

## Verification

The program verifies correctness by comparing CUDA results with CPU results. All implementations should produce identical results for the same input polynomials.

## Troubleshooting

### Common Issues

1. **"No CUDA devices found"**
   - Ensure NVIDIA GPU is installed and drivers are up to date
   - Check that CUDA toolkit is properly installed

2. **"compute capability mismatch"**
   - Update the `-arch=sm_XX` flag in Makefile to match your GPU

3. **Poor performance**
   - Ensure GPU is not being used by other processes
   - Try larger polynomial sizes (GPU excels at large problems)
   - Check that optimization flags are enabled (`-O3`)

4. **Compilation errors**
   - Ensure CUDA toolkit is in PATH
   - Check that compiler supports C++11

## Future Improvements

Potential enhancements:
1. **Shared Memory Optimization**: Use shared memory for frequently accessed data
2. **Streaming**: Overlap computation with memory transfers using CUDA streams
3. **Multi-GPU Support**: Distribute computation across multiple GPUs
4. **Optimized Karatsuba**: Implement iterative Karatsuba to reduce recursion overhead
5. **Mixed Precision**: Use different precision for intermediate calculations

## References

- CUDA Programming Guide: https://docs.nvidia.com/cuda/
- Karatsuba Algorithm: https://en.wikipedia.org/wiki/Karatsuba_algorithm
- Lab 5 CPU Implementation: `../polynomial_multiplication.py`

## Author

CUDA implementation for Lab 8 bonus assignment.






