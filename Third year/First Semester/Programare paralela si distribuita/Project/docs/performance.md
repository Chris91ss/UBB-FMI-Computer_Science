# Performance Measurements

This document describes the performance measurement methodology and presents results for the n-body simulation implementations.

## Measurement Methodology

### Metrics Collected

1. **Total Execution Time:** Wall-clock time for entire simulation
2. **Time per Step:** Average time for a single simulation step
3. **Min/Max Time per Step:** Variability in step execution time
4. **Throughput:** Bodies processed per second (bodies × steps / total_time)

### Measurement Process

1. Generate random initial conditions (same seed for reproducibility)
2. Run simulation for specified number of steps
3. Record time for each step
4. Calculate aggregate statistics
5. Compare across different implementations and configurations

### Test Configurations

- **Number of bodies:** 100, 500, 1000, 5000, 10000
- **Number of steps:** 100 (for consistency)
- **Number of threads:** 1, 2, 4, 8 (for threaded implementation)
- **Number of MPI processes:** 1, 2, 4, 8 (for MPI implementation)

## Performance Results

Performance measurements are collected automatically during simulation runs. The results are displayed in the terminal and saved to text files.

### Metrics Displayed

After each simulation run, the following metrics are shown:
- Total execution time
- Average time per step
- Minimum and maximum time per step
- Throughput (body-steps per second)

### Implementation Comparison

#### Threaded Implementation
- Uses Barnes-Hut algorithm (O(n log n))
- Good for moderate numbers of bodies
- Performance depends on number of CPU cores
- Python GIL limits true parallelism

#### MPI Implementation
- Uses Barnes-Hut algorithm (O(n log n))
- Good for distributed systems
- Communication overhead for small problems
- Better scalability for large problems


### Performance Analysis Guidelines

To collect performance data:

1. Run simulations with different numbers of bodies (e.g., 100, 500, 1000, 5000)
2. Run with different thread/process counts
3. Compare execution times across implementations
4. Calculate speedup and efficiency
5. Record results in the format below

### Example Results Format

For your own measurements, record the actual execution times:

**Threaded Implementation (1000 bodies, 100 steps):**
- Record execution time for different thread counts
- Calculate speedup: Time(1 thread) / Time(n threads)
- Calculate efficiency: Speedup / Number of threads

**MPI Implementation (1000 bodies, 100 steps):**
- Record execution time for different process counts
- Calculate speedup: Time(1 process) / Time(n processes)
- Note communication overhead


## Performance Analysis

### Expected Observations

1. **Threaded Implementation:**
   - Good speedup for moderate number of threads (2-4)
   - Diminishing returns with more threads due to GIL (Global Interpreter Lock) in Python
   - Overhead from thread management becomes significant with many threads

2. **MPI Implementation:**
   - Communication overhead significant for small problems
   - Better scalability for large problems
   - Network latency affects performance
   - Load balancing important for efficiency

3. **Comparison:**
   - Threaded: Better for small-medium problems on single machine
   - MPI: Better for large problems or distributed systems
   - Both implementations benefit from Barnes-Hut algorithm's O(n log n) complexity

### Bottlenecks

1. **Tree Construction:** O(n log n) but single-threaded
2. **Communication:** MPI gather/broadcast operations
3. **Python GIL:** Limits true parallelism in threaded implementation
4. **Memory Access:** Cache misses in tree traversal

### Optimization Opportunities

1. **Parallel Tree Construction:** Build tree in parallel (complex but possible)
2. **Reduced Communication:** Only communicate changed bodies
3. **Better Load Balancing:** Dynamic load balancing based on computation time
4. **Compiled Code:** Use Cython or Numba for critical sections

## Running Performance Tests

To collect performance data:

1. **Threaded:**
   ```bash
   python main.py
   # Choose option 1, vary number of bodies and threads
   ```

2. **MPI:**
   ```bash
   mpirun -n 4 python main.py
   # Choose option 2, vary number of bodies and processes
   ```


Results are automatically saved to text files with timestamps. Check the generated `results_*.txt` files for detailed metrics.

## Notes

- All measurements should be done on the same hardware for fair comparison
- Multiple runs should be averaged to account for system variability
- Warm-up runs should be excluded from measurements
- System load should be minimized during testing

