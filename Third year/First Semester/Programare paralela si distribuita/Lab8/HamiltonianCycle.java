import java.util.*;
import java.util.concurrent.*;

/**
 * Hamiltonian Cycle Finder - Java Implementation using ForkJoinPool
 * Finds a Hamiltonian cycle in a directed graph using multi-level parallelization.
 */
public class HamiltonianCycle {
    
    static class Graph {
        private int numVertices;
        private Map<Integer, List<Integer>> adjList;
        
        public Graph(int numVertices) {
            this.numVertices = numVertices;
            this.adjList = new HashMap<>();
            for (int i = 0; i < numVertices; i++) {
                adjList.put(i, new ArrayList<>());
            }
        }
        
        public void addEdge(int u, int v) {
            if (!adjList.get(u).contains(v)) {
                adjList.get(u).add(v);
            }
        }
        
        public List<Integer> getNeighbors(int vertex) {
            return adjList.getOrDefault(vertex, new ArrayList<>());
        }
        
        public int getNumVertices() {
            return numVertices;
        }
    }
    
    static class SearchTask extends RecursiveTask<List<Integer>> {
        private Graph graph;
        private List<Integer> path;
        private Set<Integer> visited;
        private int availableThreads;
        private static volatile List<Integer> result = null;
        private static final Object resultLock = new Object();
        
        public SearchTask(Graph graph, List<Integer> path, Set<Integer> visited, int availableThreads) {
            this.graph = graph;
            this.path = new ArrayList<>(path);
            this.visited = new HashSet<>(visited);
            this.availableThreads = availableThreads;
        }
        
        @Override
        protected List<Integer> compute() {
            // Check if result already found
            synchronized (resultLock) {
                if (result != null) {
                    return null;
                }
            }
            
            int currentVertex = path.get(path.size() - 1);
            
            // Base case: if we've visited all vertices
            if (visited.size() == graph.getNumVertices()) {
                // Check if we can return to start
                int startVertex = path.get(0);
                if (graph.getNeighbors(currentVertex).contains(startVertex)) {
                    List<Integer> cycle = new ArrayList<>(path);
                    cycle.add(startVertex);
                    synchronized (resultLock) {
                        if (result == null) {
                            result = cycle;
                            return cycle;
                        }
                    }
                }
                return null;
            }
            
            // Get unvisited neighbors
            List<Integer> neighbors = graph.getNeighbors(currentVertex);
            List<Integer> unvisitedNeighbors = new ArrayList<>();
            for (int neighbor : neighbors) {
                if (!visited.contains(neighbor)) {
                    unvisitedNeighbors.add(neighbor);
                }
            }
            
            if (unvisitedNeighbors.isEmpty()) {
                return null;
            }
            
            // If we have only one thread or one neighbor, do sequential search
            if (availableThreads == 1 || unvisitedNeighbors.size() == 1) {
                for (int neighbor : unvisitedNeighbors) {
                    synchronized (resultLock) {
                        if (result != null) {
                            return null;
                        }
                    }
                    
                    List<Integer> newPath = new ArrayList<>(path);
                    newPath.add(neighbor);
                    Set<Integer> newVisited = new HashSet<>(visited);
                    newVisited.add(neighbor);
                    
                    SearchTask task = new SearchTask(graph, newPath, newVisited, 1);
                    List<Integer> cycle = task.compute();
                    if (cycle != null) {
                        return cycle;
                    }
                }
                return null;
            } else {
                // Split work among neighbors based on available threads
                List<SearchTask> tasks = new ArrayList<>();
                int threadsPerNeighbor = availableThreads / unvisitedNeighbors.size();
                int remainingThreads = availableThreads % unvisitedNeighbors.size();
                
                for (int i = 0; i < unvisitedNeighbors.size(); i++) {
                    synchronized (resultLock) {
                        if (result != null) {
                            return null;
                        }
                    }
                    
                    int neighbor = unvisitedNeighbors.get(i);
                    int threadsForThis = threadsPerNeighbor + (i < remainingThreads ? 1 : 0);
                    
                    List<Integer> newPath = new ArrayList<>(path);
                    newPath.add(neighbor);
                    Set<Integer> newVisited = new HashSet<>(visited);
                    newVisited.add(neighbor);
                    
                    SearchTask task = new SearchTask(graph, newPath, newVisited, threadsForThis);
                    
                    if (threadsForThis > 1 && unvisitedNeighbors.size() > 1) {
                        tasks.add(task);
                        task.fork();
                    } else {
                        List<Integer> cycle = task.compute();
                        if (cycle != null) {
                            return cycle;
                        }
                    }
                }
                
                // Join all tasks and check results
                for (SearchTask task : tasks) {
                    List<Integer> cycle = task.join();
                    if (cycle != null) {
                        return cycle;
                    }
                }
                
                return null;
            }
        }
        
        public static void reset() {
            synchronized (resultLock) {
                result = null;
            }
        }
        
        public static List<Integer> getResult() {
            synchronized (resultLock) {
                return result;
            }
        }
    }
    
    public static Graph createTestGraph() {
        Graph graph = new Graph(5);
        // Create a cycle: 0 -> 1 -> 2 -> 3 -> 4 -> 0
        graph.addEdge(0, 1);
        graph.addEdge(1, 2);
        graph.addEdge(2, 3);
        graph.addEdge(3, 4);
        graph.addEdge(4, 0);
        // Add some extra edges
        graph.addEdge(0, 2);
        graph.addEdge(1, 3);
        graph.addEdge(2, 4);
        return graph;
    }
    
    public static Graph createLargerTestGraph() {
        Graph graph = new Graph(7);
        // Create a cycle: 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 0
        graph.addEdge(0, 1);
        graph.addEdge(1, 2);
        graph.addEdge(2, 3);
        graph.addEdge(3, 4);
        graph.addEdge(4, 5);
        graph.addEdge(5, 6);
        graph.addEdge(6, 0);
        // Add extra edges
        graph.addEdge(0, 2);
        graph.addEdge(1, 3);
        graph.addEdge(2, 4);
        graph.addEdge(3, 5);
        graph.addEdge(4, 6);
        return graph;
    }
    
    public static Graph createPerformanceTestGraph(int size) {
        Graph graph = new Graph(size);
        
        // Create a Hamiltonian cycle: 0 -> 1 -> 2 -> ... -> (size-1) -> 0
        for (int i = 0; i < size; i++) {
            graph.addEdge(i, (i + 1) % size);
        }
        
        // Add many alternative edges to create a huge search space
        // Forward edges (skipping vertices)
        int maxSkip = Math.min(5, size / 2);
        for (int skip = 2; skip < maxSkip; skip++) {
            for (int i = 0; i < size; i++) {
                graph.addEdge(i, (i + skip) % size);
            }
        }
        
        // Backward edges (for larger graphs)
        if (size >= 15) {
            for (int i = 0; i < size; i++) {
                graph.addEdge(i, (i - 2 + size) % size);
                graph.addEdge(i, (i - 3 + size) % size);
            }
        }
        
        // Cross connections (connect vertices that are far apart)
        if (size >= 12) {
            for (int i = 0; i < size; i += 2) {
                for (int j = i + 4; j < size; j += 3) {
                    graph.addEdge(i, j);
                    graph.addEdge(j, i);
                }
            }
        }
        
        // Additional connections for very large graphs
        if (size >= 18) {
            for (int i = 0; i < size; i++) {
                // Connect to vertices at various distances
                for (int offset : new int[]{5, 7, 9}) {
                    if (offset < size) {
                        graph.addEdge(i, (i + offset) % size);
                    }
                }
            }
        }
        
        return graph;
    }
    
    public static List<Integer> findCycle(Graph graph, int startVertex, int numThreads) {
        SearchTask.reset();
        
        List<Integer> initialPath = new ArrayList<>();
        initialPath.add(startVertex);
        Set<Integer> visited = new HashSet<>();
        visited.add(startVertex);
        
        ForkJoinPool pool = new ForkJoinPool(numThreads);
        try {
            SearchTask task = new SearchTask(graph, initialPath, visited, numThreads);
            pool.invoke(task);
        } finally {
            pool.shutdown();
        }
        
        return SearchTask.getResult();
    }
    
    public static void main(String[] args) {
        System.out.println("============================================================");
        System.out.println("Hamiltonian Cycle Finder - Java Demo");
        System.out.println("============================================================");
        
        Graph graph = createTestGraph();
        System.out.println("\nGraph with " + graph.getNumVertices() + " vertices");
        System.out.println("Edges:");
        for (int u = 0; u < graph.getNumVertices(); u++) {
            for (int v : graph.getNeighbors(u)) {
                System.out.println("  " + u + " -> " + v);
            }
        }
        
        int numThreads = 4;
        System.out.println("\nSearching for Hamiltonian cycle with " + numThreads + " threads...");
        System.out.println("Starting from vertex 0");
        
        long startTime = System.nanoTime();
        List<Integer> cycle = findCycle(graph, 0, numThreads);
        long endTime = System.nanoTime();
        
        double elapsed = (endTime - startTime) / 1_000_000_000.0;
        
        if (cycle != null) {
            System.out.print("\nHamiltonian cycle found: ");
            System.out.println(cycle.stream()
                .map(String::valueOf)
                .reduce((a, b) -> a + " -> " + b)
                .orElse(""));
            System.out.printf("Time taken: %.4f seconds\n", elapsed);
        } else {
            System.out.println("\nNo Hamiltonian cycle found");
            System.out.printf("Time taken: %.4f seconds\n", elapsed);
        }
        
        // Performance comparison
        System.out.println("\n============================================================");
        System.out.println("Performance Comparison");
        System.out.println("============================================================");
        
        // Test with larger, more complex graphs
        int[] graphSizes = {15, 18, 20};
        int[] threadCounts = {1, 2, 4, 8, 16};
        
        for (int graphSize : graphSizes) {
            System.out.println("\n" + "============================================================");
            System.out.println("Graph Size: " + graphSize + " vertices");
            System.out.println("============================================================");
            
            Graph testGraph = createPerformanceTestGraph(graphSize);
            int edgeCount = 0;
            for (int u = 0; u < testGraph.getNumVertices(); u++) {
                edgeCount += testGraph.getNeighbors(u).size();
            }
            System.out.println("Graph has " + edgeCount + " edges");
            
            System.out.printf("\n%-10s %-20s %-15s\n", "Threads", "Time (seconds)", "Status");
            System.out.println("------------------------------------------------------------");
            
            // Store results for summary
            double bestTime = Double.MAX_VALUE;
            double worstTime = 0;
            int bestThreads = 1, worstThreads = 1;
            
            for (int threads : threadCounts) {
                SearchTask.reset();
                startTime = System.nanoTime();
                cycle = findCycle(testGraph, 0, threads);
                endTime = System.nanoTime();
                elapsed = (endTime - startTime) / 1_000_000_000.0;
                
                String status = cycle != null ? "Found" : "Not found";
                
                System.out.printf("%-10d %-20.6f %-15s\n", threads, elapsed, status);
                
                // Track best/worst for summary
                if (elapsed < bestTime) {
                    bestTime = elapsed;
                    bestThreads = threads;
                }
                if (elapsed > worstTime) {
                    worstTime = elapsed;
                    worstThreads = threads;
                }
            }
            
            // Summary
            System.out.println("\nSummary for " + graphSize + " vertices:");
            if (worstTime > 0) {
                double improvement = ((worstTime - bestTime) / worstTime * 100);
                System.out.printf("  Best time: %.4fs (%d threads)\n", bestTime, bestThreads);
                System.out.printf("  Worst time: %.4fs (%d threads)\n", worstTime, worstThreads);
                System.out.printf("  Improvement: %.1f%%\n", improvement);
            } else {
                System.out.println("  All runs completed in < 0.0001s");
            }
        }
    }
}

