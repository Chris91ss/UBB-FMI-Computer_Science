# Synchronization Mechanisms

This document describes the synchronization mechanisms used in the parallelized variants of the n-body simulation.

## Threaded Implementation

### Thread Pool

The threaded implementation uses Python's `concurrent.futures.ThreadPoolExecutor` to manage a pool of worker threads. Bodies are divided into chunks, and each thread processes one chunk.

### Synchronization Mechanisms

#### 1. Tree Construction
- **Synchronization:** Single-threaded
- **Rationale:** Tree construction is fast (O(n log n)) and building multiple trees would be wasteful. The tree is built once per time step before force calculations.

#### 2. Force Calculation
- **Synchronization:** None required during calculation
- **Rationale:** Each thread works on a different subset of bodies. Force calculations are read-only operations on the tree structure, so no synchronization is needed.

#### 3. Force Accumulation
- **Synchronization:** None required
- **Rationale:** Each body's force is calculated and stored independently. No shared state is modified during force calculation.

#### 4. Position/Velocity Updates
- **Synchronization:** None required
- **Rationale:** Each body is updated independently. Since bodies are partitioned across threads, there are no race conditions.

### Thread Safety

The implementation ensures thread safety by:
- **Read-only tree access:** The Barnes-Hut tree is built before parallel execution and not modified during force calculations
- **Independent body updates:** Each thread updates different bodies, avoiding write conflicts
- **No shared mutable state:** All shared data (the tree) is read-only during parallel execution

### Potential Race Conditions (Avoided)

1. **Tree modification during traversal:** Avoided by building tree before parallel execution
2. **Concurrent force updates:** Avoided by partitioning bodies across threads
3. **Position updates:** Avoided by updating bodies independently

## MPI Implementation

### Domain Decomposition

The MPI implementation uses domain decomposition to partition bodies across MPI ranks. Each rank is responsible for a subset of bodies.

### Synchronization Mechanisms

#### 1. Initial Body Distribution
- **Communication:** `MPI_Bcast` (broadcast)
- **Purpose:** Distribute initial body configuration to all ranks
- **Pattern:** One-to-many communication

#### 2. Body Synchronization (After Each Step)
- **Communication:** `MPI_Gatherv` and `MPI_Bcast`
- **Purpose:** 
  - Gather updated positions, velocities, and masses from all ranks
  - Broadcast the complete state to all ranks
- **Pattern:** Many-to-one (gather) then one-to-many (broadcast)

#### 3. Performance Timing
- **Communication:** `MPI_Allreduce` with `MPI_MAX` operation
- **Purpose:** Synchronize timing measurements across all ranks
- **Pattern:** All-to-all reduction

### Communication Pattern

Each time step follows this pattern:

```
1. Gather all body data (MPI_Gatherv)
   - Each rank sends its local bodies' positions, velocities, masses
   - Rank 0 collects all data

2. Broadcast complete state (MPI_Bcast)
   - Rank 0 broadcasts complete body state to all ranks
   - All ranks now have the same view of all bodies

3. Build local tree
   - Each rank builds its own Barnes-Hut tree from all bodies
   - No communication needed (all ranks have same data)

4. Calculate forces for local bodies
   - Each rank calculates forces only for its assigned bodies
   - No communication needed (read-only tree traversal)

5. Update local bodies
   - Each rank updates positions/velocities of its local bodies
   - No communication needed (independent updates)

6. Repeat from step 1
```

### Synchronization Points

1. **After tree construction:** All ranks must have the same body positions before building trees
2. **After force calculation:** All ranks must synchronize before next step
3. **Timing synchronization:** All ranks wait for slowest rank before proceeding

### Load Balancing

- Bodies are distributed evenly across ranks
- If n bodies and p ranks: each rank gets approximately n/p bodies
- Remaining bodies (n % p) are distributed to the first (n % p) ranks

### Deadlock Prevention

- All collective operations (Gatherv, Bcast, Allreduce) are called by all ranks
- No point-to-point communication that could cause deadlocks
- All ranks participate in all collective operations

## Comparison

| Aspect | Threaded | MPI |
|--------|----------|-----|
| **Shared Memory** | Yes | No |
| **Communication** | Implicit (shared memory) | Explicit (message passing) |
| **Synchronization** | Minimal (read-only tree) | Explicit (gather/broadcast) |
| **Scalability** | Limited by cores | Limited by network |
| **Overhead** | Low (shared memory) | Higher (network communication) |

