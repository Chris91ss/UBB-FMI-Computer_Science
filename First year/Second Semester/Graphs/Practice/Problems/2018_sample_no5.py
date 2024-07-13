from collections import defaultdict
import math


# exam 2018 no.5
def bellman_ford(graph, V, source):
    distance = [math.inf] * V
    predecessor = [-1] * V
    distance[source] = 0
    cycle_nodes = None

    # Relax all edges V-1 times
    for _ in range(V - 1):
        for u in range(V):
            for v, weight in graph[u]:
                if distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    predecessor[v] = u

    # Check for negative-weight cycles
    for u in range(V):
        for v, weight in graph[u]:
            if distance[u] + weight < distance[v]:
                cycle_nodes = v

    if cycle_nodes is not None:
        return detect_cycle(predecessor, cycle_nodes, V)
    return None


def detect_cycle(predecessor, start, V):
    visited = [False] * V
    cycle = []
    cycle_set = set()
    cycle_lengths = []

    # Find the start of the cycle
    while not visited[start]:
        visited[start] = True
        start = predecessor[start]

    cycle_start = start
    # Gather nodes in the cycle
    while True:
        cycle.append(cycle_start)
        cycle_set.add(cycle_start)
        cycle_start = predecessor[cycle_start]
        if cycle_start == start:
            break
    cycle.append(start)
    cycle.reverse()

    return cycle


def find_shortest_negative_cycle(graph, V, source):
    return bellman_ford(graph, V, source)


# Example usage
if __name__ == "__main__":
    graph = defaultdict(list)
    V = 5  # Number of vertices
    edges = [
        (0, 1, 1),
        (1, 2, -1),
        (2, 3, -1),
        (3, 4, -1),
        (4, 1, -1)
    ]

    for u, v, weight in edges:
        graph[u].append((v, weight))

    source = 0
    cycle = find_shortest_negative_cycle(graph, V, source)
    if cycle:
        print("Negative cycle found:", cycle)
    else:
        print("No negative cycle found")
