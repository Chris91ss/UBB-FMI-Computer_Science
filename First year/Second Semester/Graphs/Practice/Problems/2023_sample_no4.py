from collections import deque, defaultdict


def topological_sort(graph, V):
    in_degree = [0] * V
    for u in range(V):
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque([u for u in range(V) if in_degree[u] == 0])
    topo_order = []

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return topo_order


def count_max_length_paths(graph, start, end, V):
    # Step 1: Perform a topological sort
    topo_order = topological_sort(graph, V)

    # Initialize distances and path counts
    dist = [-float('inf')] * V
    count = [0] * V
    dist[start] = 0
    count[start] = 1

    # Step 2: Compute the longest path using the topological order
    for u in topo_order:
        if dist[u] != -float('inf'):
            for v in graph[u]:
                if dist[v] < dist[u] + 1:
                    dist[v] = dist[u] + 1
                    count[v] = count[u]
                elif dist[v] == dist[u] + 1:
                    count[v] += count[u]

    # Step 3: Return the number of maximum length paths to the end vertex
    return count[end] if dist[end] != -float('inf') else 0


def main():
    # Example usage:
    V = 6
    graph = defaultdict(list)
    # Define the edges of the graph
    edges = [(0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 3)]
    for u, v in edges:
        graph[u].append(v)

    # Start and end vertices
    start = 0
    end = 3

    # Get the number of distinct paths of maximum length from start to end
    result = count_max_length_paths(graph, start, end, V)
    print("Number of distinct paths of maximum length:", result)


if __name__ == "__main__":
    main()
