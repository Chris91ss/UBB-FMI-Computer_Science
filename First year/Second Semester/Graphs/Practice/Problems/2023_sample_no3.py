import sys
from collections import defaultdict, deque


def find_min_cost_paths(graph, n, s, t):
    # Topological sort of the graph nodes
    topo_order = topological_sort(graph, n)

    # Initialize distances and path counts
    dist = [float('inf')] * n
    count = [0] * n
    dist[s] = 0
    count[s] = 1

    # Relax edges according to topological order
    for u in topo_order:
        if dist[u] < float('inf'):  # Proceed only if `u` is reachable
            for v, weight in graph[u]:
                if dist[u] + weight < dist[v]:  # Found a shorter path to `v`
                    dist[v] = dist[u] + weight
                    count[v] = count[u]
                elif dist[u] + weight == dist[v]:  # Found another min cost path to `v`
                    count[v] += count[u]

    # Return the number of minimum cost paths from s to t
    return count[t]


def topological_sort(graph, n):
    in_degree = [0] * n
    for u in range(n):
        for v, _ in graph[u]:
            in_degree[v] += 1

    # Queue for vertices with no incoming edges
    zero_in_degree_queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []

    while zero_in_degree_queue:
        u = zero_in_degree_queue.popleft()
        topo_order.append(u)
        for v, _ in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                zero_in_degree_queue.append(v)

    if len(topo_order) != n:
        raise ValueError("Graph is not a DAG")

    return topo_order


def main():
    # Example usage
    n = 6  # Number of vertices in the graph
    graph = defaultdict(list)
    # Add directed edges (u, v, cost)
    edges = [(0, 1, 3), (0, 2, 6), (1, 2, 4), (1, 3, 4), (1, 4, 11), (2, 3, 8), (3, 4, -4), (2, 5, 11), (3, 5, 5),
             (4, 5, 2)]
    for u, v, cost in edges:
        graph[u].append((v, cost))

    s = 0  # Start vertex
    t = 5  # End vertex
    print(find_min_cost_paths(graph, n, s, t))  # Output the number of distinct minimum cost paths


if __name__ == "__main__":
    main()
