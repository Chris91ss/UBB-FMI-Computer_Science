"""
Hamiltonian Cycle Finder - Parallel Implementation
Finds a Hamiltonian cycle in a directed graph using multi-level parallelization.
"""
import threading
import time
from typing import List, Set, Optional, Tuple
from collections import defaultdict


class Graph:
    """Represents a directed graph using adjacency list."""
    
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adj_list = defaultdict(list)
    
    def add_edge(self, u: int, v: int):
        """Add a directed edge from u to v."""
        if v not in self.adj_list[u]:
            self.adj_list[u].append(v)
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """Get all neighbors of a vertex."""
        return self.adj_list.get(vertex, [])


class ParallelHamiltonianCycle:
    """Parallel Hamiltonian cycle finder with multi-level work splitting."""
    
    def __init__(self, graph: Graph, num_threads: int):
        self.graph = graph
        self.num_threads = num_threads
        self.result = None
        self.result_lock = threading.Lock()
        self.found = threading.Event()
    
    def find_cycle(self, start_vertex: int) -> Optional[List[int]]:
        """
        Find a Hamiltonian cycle starting from start_vertex.
        Returns the cycle if found, None otherwise.
        """
        self.result = None
        self.found.clear()
        
        # Start with the initial path containing only the start vertex
        initial_path = [start_vertex]
        visited = {start_vertex}
        
        # Start parallel search
        self._parallel_search(initial_path, visited, self.num_threads)
        
        return self.result
    
    def _parallel_search(self, path: List[int], visited: Set[int], available_threads: int):
        """
        Recursively search for Hamiltonian cycle with parallelization.
        Splits work at multiple levels based on available threads.
        """
        # If solution already found, stop searching
        if self.found.is_set():
            return
        
        current_vertex = path[-1]
        
        # Base case: if we've visited all vertices
        if len(visited) == self.graph.num_vertices:
            # Check if we can return to start
            start_vertex = path[0]
            if start_vertex in self.graph.get_neighbors(current_vertex):
                cycle = path + [start_vertex]
                with self.result_lock:
                    if self.result is None:
                        self.result = cycle
                        self.found.set()
                return
            return
        
        # Get unvisited neighbors
        neighbors = self.graph.get_neighbors(current_vertex)
        unvisited_neighbors = [n for n in neighbors if n not in visited]
        
        if not unvisited_neighbors:
            return
        
        # If we have only one thread or one neighbor, do sequential search
        if available_threads == 1 or len(unvisited_neighbors) == 1:
            for neighbor in unvisited_neighbors:
                if self.found.is_set():
                    return
                new_path = path + [neighbor]
                new_visited = visited | {neighbor}
                self._parallel_search(new_path, new_visited, 1)
        else:
            # Split work among neighbors based on available threads
            threads = []
            threads_per_neighbor = available_threads // len(unvisited_neighbors)
            remaining_threads = available_threads % len(unvisited_neighbors)
            
            for i, neighbor in enumerate(unvisited_neighbors):
                if self.found.is_set():
                    break
                
                # Allocate threads: first neighbors get one extra thread if there's remainder
                threads_for_this = threads_per_neighbor + (1 if i < remaining_threads else 0)
                
                new_path = path + [neighbor]
                new_visited = visited | {neighbor}
                
                # If we have more than one thread for this branch, create a thread
                if threads_for_this > 1 and len(unvisited_neighbors) > 1:
                    thread = threading.Thread(
                        target=self._parallel_search,
                        args=(new_path, new_visited, threads_for_this)
                    )
                    thread.start()
                    threads.append(thread)
                else:
                    # Sequential search for this branch
                    self._parallel_search(new_path, new_visited, threads_for_this)
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()


def create_test_graph() -> Graph:
    """Create a test graph with a Hamiltonian cycle."""
    graph = Graph(5)
    # Create a cycle: 0 -> 1 -> 2 -> 3 -> 4 -> 0
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)
    # Add some extra edges
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    return graph


def create_larger_test_graph() -> Graph:
    """Create a larger test graph."""
    graph = Graph(7)
    # Create a cycle: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 0
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 0)
    # Add extra edges for more complexity
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(4, 6)
    return graph


def create_performance_test_graph(size: int) -> Graph:
    """Create a test graph of specified size with a Hamiltonian cycle and extra edges."""
    graph = Graph(size)
    
    # Create a Hamiltonian cycle: 0 -> 1 -> 2 -> ... -> (size-1) -> 0
    for i in range(size):
        graph.add_edge(i, (i + 1) % size)
    
    # Add extra edges to create more search paths (makes it harder to find)
    # Add edges skipping one vertex (creates alternative paths)
    for i in range(size):
        graph.add_edge(i, (i + 2) % size)
    
    # Add more edges for larger graphs to increase search space
    if size >= 8:
        # Add edges skipping two vertices
        for i in range(size):
            graph.add_edge(i, (i + 3) % size)
    
    if size >= 10:
        # Add some backward edges to create more complexity
        for i in range(2, size):
            graph.add_edge(i, (i - 2) % size)
    
    if size >= 12:
        # Add more alternative paths
        for i in range(0, size, 3):
            graph.add_edge(i, (i + 4) % size)
    
    return graph


def run_hamiltonian_demo():
    """Run a demo of the Hamiltonian cycle finder."""
    print("\n" + "=" * 60)
    print("Hamiltonian Cycle Finder - Demo")
    print("=" * 60)
    
    graph = create_test_graph()
    print(f"\nGraph with {graph.num_vertices} vertices")
    print("Edges:")
    for u in range(graph.num_vertices):
        for v in graph.get_neighbors(u):
            print(f"  {u} -> {v}")
    
    num_threads = 4
    print(f"\nSearching for Hamiltonian cycle with {num_threads} threads...")
    print("Starting from vertex 0")
    
    finder = ParallelHamiltonianCycle(graph, num_threads)
    start_time = time.time()
    cycle = finder.find_cycle(0)
    end_time = time.time()
    
    if cycle:
        print(f"\nHamiltonian cycle found: {' -> '.join(map(str, cycle))}")
        print(f"Time taken: {end_time - start_time:.4f} seconds")
    else:
        print("\nNo Hamiltonian cycle found")
        print(f"Time taken: {end_time - start_time:.4f} seconds")


def custom_hamiltonian_test():
    """Custom test with user-defined parameters."""
    print("\n" + "=" * 60)
    print("Hamiltonian Cycle Finder - Custom Test")
    print("=" * 60)
    
    try:
        num_vertices = int(input("\nEnter number of vertices (default 5): ") or "5")
        num_threads = int(input("Enter number of threads (default 4): ") or "4")
        start_vertex = int(input("Enter start vertex (default 0): ") or "0")
        
        graph = Graph(num_vertices)
        print(f"\nEnter edges (format: u v, empty line to finish):")
        print("Example: 0 1 (creates edge 0 -> 1)")
        
        while True:
            edge_input = input("Edge: ").strip()
            if not edge_input:
                break
            try:
                u, v = map(int, edge_input.split())
                if 0 <= u < num_vertices and 0 <= v < num_vertices:
                    graph.add_edge(u, v)
                    print(f"  Added edge: {u} -> {v}")
                else:
                    print(f"  Invalid vertex numbers (must be 0-{num_vertices-1})")
            except ValueError:
                print("  Invalid format. Use: u v")
        
        print(f"\nSearching for Hamiltonian cycle with {num_threads} threads...")
        print(f"Starting from vertex {start_vertex}")
        
        finder = ParallelHamiltonianCycle(graph, num_threads)
        start_time = time.time()
        cycle = finder.find_cycle(start_vertex)
        end_time = time.time()
        
        if cycle:
            print(f"\nHamiltonian cycle found: {' -> '.join(map(str, cycle))}")
            print(f"Time taken: {end_time - start_time:.4f} seconds")
        else:
            print("\nNo Hamiltonian cycle found")
            print(f"Time taken: {end_time - start_time:.4f} seconds")
            
    except ValueError as e:
        print(f"Error: {e}")


def create_complex_performance_graph(size: int) -> Graph:
    """Create a complex graph with many alternative paths to make search challenging."""
    graph = Graph(size)
    
    # Create a Hamiltonian cycle: 0 -> 1 -> 2 -> ... -> (size-1) -> 0
    for i in range(size):
        graph.add_edge(i, (i + 1) % size)
    
    # Add many alternative edges to create a huge search space
    # Each vertex connects to several others, creating many possible paths
    
    # Forward edges (skipping vertices)
    for skip in range(2, min(5, size // 2)):
        for i in range(size):
            graph.add_edge(i, (i + skip) % size)
    
    # Backward edges (for larger graphs)
    if size >= 15:
        for i in range(size):
            graph.add_edge(i, (i - 2 + size) % size)
            graph.add_edge(i, (i - 3 + size) % size)
    
    # Cross connections (connect vertices that are far apart)
    if size >= 12:
        for i in range(0, size, 2):
            for j in range(i + 4, size, 3):
                graph.add_edge(i, j)
                graph.add_edge(j, i)
    
    # Additional random-like connections for very large graphs
    if size >= 18:
        for i in range(size):
            # Connect to vertices at various distances
            for offset in [5, 7, 9]:
                if offset < size:
                    graph.add_edge(i, (i + offset) % size)
    
    return graph


def performance_comparison():
    """Compare performance with different numbers of threads."""
    print("\n" + "=" * 70)
    print("Hamiltonian Cycle Finder - Performance Comparison")
    print("=" * 70)
    
    # Test with larger, more complex graphs
    graph_sizes = [15, 18, 20]
    thread_counts = [1, 2, 4, 8, 16]
    
    for graph_size in graph_sizes:
        print(f"\n{'=' * 70}")
        print(f"Graph Size: {graph_size} vertices")
        print(f"{'=' * 70}")
        
        graph = create_complex_performance_graph(graph_size)
        edge_count = sum(len(graph.get_neighbors(v)) for v in range(graph_size))
        print(f"Graph has {edge_count} edges")
        
        results = []
        
        print(f"\n{'Threads':<10} {'Time (seconds)':<20} {'Status':<15}")
        print("-" * 50)
        
        for num_threads in thread_counts:
            finder = ParallelHamiltonianCycle(graph, num_threads)
            
            # Use time.perf_counter() for more accurate timing
            start_time = time.perf_counter()
            cycle = finder.find_cycle(0)
            end_time = time.perf_counter()
            
            elapsed = end_time - start_time
            status = "Found" if cycle else "Not found"
            
            results.append((num_threads, elapsed, cycle is not None))
            
            # Format time with appropriate precision
            if elapsed < 0.01:
                time_str = f"{elapsed:.6f}"
            elif elapsed < 1:
                time_str = f"{elapsed:.4f}"
            else:
                time_str = f"{elapsed:.2f}"
            
            print(f"{num_threads:<10} {time_str:<20} {status:<15}")
        
        # Summary
        print(f"\nSummary for {graph_size} vertices:")
        best_time = min(r[1] for r in results)
        worst_time = max(r[1] for r in results)
        best_threads = [r[0] for r in results if r[1] == best_time][0]
        worst_threads = [r[0] for r in results if r[1] == worst_time][0]
        
        if worst_time > 0:
            improvement = ((worst_time - best_time) / worst_time * 100)
            print(f"  Best time: {best_time:.4f}s ({best_threads} threads)")
            print(f"  Worst time: {worst_time:.4f}s ({worst_threads} threads)")
            print(f"  Improvement: {improvement:.1f}%")
        else:
            print(f"  All runs completed in < 0.0001s")

