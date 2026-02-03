# N-Body Simulation - Barnes-Hut Algorithm

Parallel and distributed implementation of the n-body problem using the Barnes-Hut algorithm.

## Project Structure

```
Project/
├── README.md
├── requirements.txt
├── main.py                    # Main entry point with menu
├── src/
│   ├── __init__.py
│   ├── body.py               # Body class
│   ├── barnes_hut.py         # Barnes-Hut tree structure
│   ├── threaded_sim.py       # Thread-based implementation
│   └── mpi_sim.py            # MPI distributed implementation
└── docs/
    ├── algorithms.md         # Algorithm descriptions
    ├── synchronization.md   # Synchronization mechanisms
    └── performance.md       # Performance measurements
```

## Requirements

- Python 3.7+
- numpy
- mpi4py (for MPI implementation)
- colorama (for colored console output)
- MPI runtime (e.g., OpenMPI, MPICH) for distributed execution

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. For MPI implementation, install MPI runtime:
   - **Linux:** `sudo apt-get install openmpi-bin libopenmpi-dev` (Ubuntu/Debian)
   - **Windows:** Install MS-MPI or use WSL
   - **macOS:** `brew install open-mpi`

## Usage

### Interactive Menu

Run the main program:
```bash
python main.py
```

The menu offers:
1. **Run Threaded Simulation** - Multi-threaded implementation using ThreadPoolExecutor
2. **Run MPI Simulation** - Distributed implementation using MPI
3. **Exit**

### Threaded Simulation

Choose option 1 from the menu. You will be prompted for:
- Number of bodies (default: 1000)
- Number of threads (default: 4)
- Number of simulation steps (default: 100)

### MPI Simulation

Run with MPI:
```bash
mpirun -n <num_processes> python main.py
```

Then choose option 2 from the menu. You will be prompted for:
- Number of bodies (default: 1000)
- Number of simulation steps (default: 100)

The number of MPI processes is determined by the `-n` parameter.


## Algorithm

The simulation uses the **Barnes-Hut algorithm** to approximate gravitational forces:
- Time complexity: O(n log n) per time step (vs O(n²) for direct calculation)
- Uses an octree to partition 3D space
- Approximates distant groups of bodies as a single mass at their center of mass
- θ (theta) parameter controls accuracy vs speed trade-off (default: 0.5)

## Documentation

See the `docs/` directory for detailed documentation:
- **algorithms.md**: Description of the n-body problem and Barnes-Hut algorithm
- **synchronization.md**: Synchronization mechanisms used in parallel implementations
- **performance.md**: Performance measurement methodology and results

## Implementation Details

### Threaded Implementation
- Uses `concurrent.futures.ThreadPoolExecutor`
- Bodies are divided into chunks, one per thread
- Minimal synchronization (read-only tree access)
- Good for single-machine parallelization

### MPI Implementation
- Uses `mpi4py` for distributed computing
- Bodies are distributed across MPI ranks
- Communication via `MPI_Gatherv` and `MPI_Bcast` after each step
- Suitable for distributed systems and clusters


## Performance

Performance metrics are displayed after each simulation run:
- Total execution time
- Average time per step
- Throughput (body-steps per second)

For detailed performance analysis, see `docs/performance.md`.

## License

This project is for educational purposes.

