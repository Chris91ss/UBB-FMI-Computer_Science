# Hamiltonian Cycle Finder - Lab 6 Documentation

## Problem Description

Given a directed graph, find a Hamiltonian cycle (a cycle that visits each vertex exactly once and returns to the starting vertex), if one exists. The solution uses parallelization with a specified number of threads, splitting work at multiple levels of the search tree.

## Algorithm Description

### Core Algorithm

The algorithm uses a **backtracking depth-first search** approach:

1. **Start from a fixed vertex**: The search begins from a specified starting vertex (typically vertex 0).

2. **Recursive exploration**: For each vertex, explore all unvisited neighbors:
   - Add the neighbor to the current path
   - Mark it as visited
   - Recursively search from that neighbor
   - If no cycle is found, backtrack (remove from path and mark as unvisited)

3. **Termination conditions**:
   - **Success**: When all vertices have been visited AND there's an edge back to the starting vertex
   - **Failure**: When no unvisited neighbors exist and not all vertices are visited

### Parallelization Strategy

The key innovation is **multi-level work splitting**:

1. **Level-based distribution**: Instead of only splitting at the first level, work is distributed at multiple levels of the search tree.

2. **Thread allocation**: When a vertex has multiple unvisited neighbors:
   - Calculate `threads_per_neighbor = total_threads / num_neighbors`
   - Distribute remaining threads to the first few neighbors
   - Each branch receives a subset of threads for further parallelization

3. **Example**: 
   - 8 threads, first vertex has 3 neighbors
   - Distribution: 3 threads → neighbor 1, 3 threads → neighbor 2, 2 threads → neighbor 3
   - On the first branch, if that neighbor has 4 unvisited neighbors:
     - 2 neighbors get 1 thread each, 2 neighbors get 1 thread each (from the 3 allocated threads)
   - This continues recursively until threads are exhausted or sequential search is more efficient

4. **Sequential fallback**: When only 1 thread is available or only 1 neighbor exists, the search becomes sequential.

## Implementation Details

### Python Implementation

**Technology**: `threading` module with `Thread` objects

**Key Components**:
- `Graph`: Adjacency list representation of the directed graph
- `ParallelHamiltonianCycle`: Main parallel search class
- `_parallel_search()`: Recursive method that splits work among threads

**Synchronization Mechanisms**:
1. **`threading.Lock` (`result_lock`)**: Protects the shared `result` variable
   - Ensures only the first thread to find a solution writes it
   - Prevents race conditions when multiple threads find solutions simultaneously

2. **`threading.Event` (`found`)**: Signals that a solution has been found
   - Allows early termination: threads check this flag before continuing expensive operations
   - Reduces unnecessary computation once a solution is found

3. **Thread joining**: All spawned threads are joined before returning, ensuring complete execution

**Work Distribution Algorithm**:
```python
threads_per_neighbor = available_threads // len(unvisited_neighbors)
remaining_threads = available_threads % len(unvisited_neighbors)

for i, neighbor in enumerate(unvisited_neighbors):
    threads_for_this = threads_per_neighbor + (1 if i < remaining_threads else 0)
    # Create thread if threads_for_this > 1, else sequential search
```

### Java Implementation

**Technology**: `ForkJoinPool` with `RecursiveTask`

**Key Components**:
- `Graph`: Adjacency list using `HashMap<Integer, List<Integer>>`
- `SearchTask`: Extends `RecursiveTask<List<Integer>>` for parallel execution
- `findCycle()`: Entry point that creates ForkJoinPool and invokes the task

**Synchronization Mechanisms**:
1. **`synchronized` blocks on `resultLock`**: 
   - Protects the static `result` variable
   - Ensures thread-safe access when checking/updating the result
   - Used before expensive operations to check if solution already found

2. **`fork()` and `join()`**: 
   - `fork()`: Asynchronously executes subtasks
   - `join()`: Waits for task completion and retrieves result
   - ForkJoinPool manages thread pool and work-stealing

3. **Early termination checks**: Multiple synchronized checks prevent unnecessary computation

**Work Distribution Algorithm**:
```java
int threadsPerNeighbor = availableThreads / unvisitedNeighbors.size();
int remainingThreads = availableThreads % unvisitedNeighbors.size();

for (int i = 0; i < unvisitedNeighbors.size(); i++) {
    int threadsForThis = threadsPerNeighbor + (i < remainingThreads ? 1 : 0);
    // Fork task if threadsForThis > 1, else compute directly
}
```

## Performance Considerations

### Time Complexity

- **Worst case**: O(n!) where n is the number of vertices
  - In the worst case, we explore all possible permutations
- **Best case**: O(n) if the cycle is found immediately
- **Average case**: Depends heavily on graph structure

### Parallelization Benefits

1. **Speedup**: Multiple threads explore different branches simultaneously
2. **Early termination**: Once one thread finds a solution, others can stop
3. **Load balancing**: Work-stealing in ForkJoinPool helps balance load

### Limitations

1. **Thread overhead**: Creating too many threads can hurt performance
2. **Graph structure**: Dense graphs with many edges benefit more than sparse graphs
3. **GIL in Python**: Python's Global Interpreter Lock limits true parallelism for CPU-bound tasks (though I/O and some operations can still benefit)

## Performance Measurements

### Test Graphs

1. **Small graph (5 vertices)**: 
   - Cycle: 0→1→2→3→4→0
   - Additional edges for complexity

2. **Larger graph (7 vertices)**:
   - Cycle: 0→1→2→3→4→5→6→0
   - Additional edges for complexity

### Expected Results

Performance varies based on:
- Number of threads
- Graph size and density
- Position of the Hamiltonian cycle in the search space

**Typical observations**:
- 1 thread: Baseline sequential performance
- 2-4 threads: Moderate speedup (1.5-3x)
- 8+ threads: Diminishing returns due to overhead

### Running Performance Tests

**Python**:
```python
from hamiltonian_cycle import performance_comparison
performance_comparison()
```

**Java**:
```bash
javac HamiltonianCycle.java
java HamiltonianCycle
```

## Usage Examples

### Python

```python
from hamiltonian_cycle import Graph, ParallelHamiltonianCycle

# Create graph
graph = Graph(5)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
# ... add more edges

# Find cycle with 4 threads
finder = ParallelHamiltonianCycle(graph, num_threads=4)
cycle = finder.find_cycle(start_vertex=0)

if cycle:
    print(f"Cycle found: {cycle}")
```

### Java

```java
Graph graph = HamiltonianCycle.createTestGraph();
List<Integer> cycle = HamiltonianCycle.findCycle(graph, 0, 4);
if (cycle != null) {
    System.out.println("Cycle found: " + cycle);
}
```

## Conclusion

Both implementations successfully parallelize the Hamiltonian cycle search using multi-level work splitting. The Java implementation using ForkJoinPool provides better performance for CPU-intensive tasks due to true parallelism, while the Python implementation demonstrates the concept using threading. The synchronization mechanisms ensure correctness while allowing early termination for efficiency.

