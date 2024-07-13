import sys
from collections import defaultdict, deque


def find_number_of_min_cost_paths(graph, costs, s, t):
    # Step 1: Perform topological sorting
    def topological_sort():
        in_degree = {u: 0 for u in graph}
        for u in graph:
            for v in graph[u]:
                in_degree[v] += 1
        queue = deque(u for u in graph if in_degree[u] == 0)
        topo_order = []
        while queue:
            u = queue.popleft()
            topo_order.append(u)
            for v in graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
        return topo_order

    # Step 2: Initialize min_cost and count
    min_cost = {u: float('inf') for u in graph}
    min_cost[s] = 0
    count = {u: 0 for u in graph}
    count[s] = 1

    # Step 3: Process vertices in topological order
    topo_order = topological_sort()
    for u in topo_order:
        if min_cost[u] != float('inf'):  # Only proceed if u is reachable
            for v in graph[u]:
                edge_cost = costs[(u, v)]
                if min_cost[v] > min_cost[u] + edge_cost:
                    min_cost[v] = min_cost[u] + edge_cost
                    count[v] = count[u]
                elif min_cost[v] == min_cost[u] + edge_cost:
                    count[v] += count[u]

    return count[t] if min_cost[t] != float('inf') else 0


def main():
    # Example of use
    graph = {
        'A': ['B', 'C'],
        'B': ['D'],
        'C': ['D'],
        'D': []
    }
    costs = {('A', 'B'): 1, ('A', 'C'): 4, ('B', 'D'): 3, ('C', 'D'): 2}
    s, t = 'A', 'D'

    # Call the function
    print(find_number_of_min_cost_paths(graph, costs, s, t))


if __name__ == "__main__":
    main()
