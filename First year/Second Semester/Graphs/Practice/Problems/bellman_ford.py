
def bellman_ford(graph, start):
    # Initialize distance and predecessor dictionaries
    dist = {vertex: float('inf') for vertex in graph}
    prev = {vertex: None for vertex in graph}
    dist[start] = 0

    # Relax edges repeatedly
    changed = True
    while changed:
        changed = False
        for vertex in graph:
            for neighbor, cost in graph[vertex].items():
                if dist[neighbor] > dist[vertex] + cost:
                    dist[neighbor] = dist[vertex] + cost
                    prev[neighbor] = vertex
                    changed = True

    return dist, prev


# Example graph represented as an adjacency list
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 3, 'D': 2, 'E': 2},
    'C': {},
    'D': {'B': 1, 'C': 5},
    'E': {'D': 3}
}

# Running the Bellman-Ford algorithm
start_vertex = 'A'
dist, prev = bellman_ford(graph, start_vertex)

print("Distance from start vertex:", dist)
print("Predecessor map:", prev)
