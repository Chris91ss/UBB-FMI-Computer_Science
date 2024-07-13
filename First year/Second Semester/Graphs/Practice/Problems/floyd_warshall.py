def floyd_warshall(graph):
    """
    Floyd-Warshall algorithm to find the shortest paths between all pairs of vertices.

    :param graph: A dictionary where keys are tuples representing edges and values are their weights.
                  For example, {(0, 1): 2, (1, 2): 3, ...}
    :return: A tuple (dist, next) where dist is a matrix of minimum distances and next is a matrix
             used for path reconstruction.
    """
    # Number of vertices
    vertices = set()
    for edge in graph.keys():
        vertices.update(edge)
    n = len(vertices)

    # Initialize distance and next matrices
    dist = [[float('inf')] * n for _ in range(n)]
    next_vertex = [[None] * n for _ in range(n)]

    # Initialize the distance and next matrices based on input graph
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif (i, j) in graph:
                dist[i][j] = graph[(i, j)]
                next_vertex[i][j] = j

    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_vertex[i][j] = next_vertex[i][k]

    return dist, next_vertex


# Example usage:
graph = {
    (0, 1): 2,
    (1, 2): 3,
    (0, 2): 4,
    # Add more edges as needed
}

distances, next_vertices = floyd_warshall(graph)

# Print the results
print("Distance matrix:")
for row in distances:
    print(row)

print("\nNext vertex matrix:")
for row in next_vertices:
    print(row)
