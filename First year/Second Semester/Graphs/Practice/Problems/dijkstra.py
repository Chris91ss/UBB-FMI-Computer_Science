import heapq


def dijkstra(G, s, t):
    # Priority queue to store (cost, vertex) pairs
    q = []
    heapq.heappush(q, (0, s))

    # Dictionary to store the cost of the minimum cost walk from s to each vertex
    dist = {s: 0}

    # Dictionary to store the predecessor of each vertex on the path from s
    prev = {}

    # While there are elements in the priority queue
    found = False
    while q and not found:
        # Dequeue the element with the minimum cost
        cost_x, x = heapq.heappop(q)

        # If the dequeued vertex is the target vertex, we found the path
        if x == t:
            found = True
            break

        # For each neighbor y of x
        for y, cost_xy in G.get(x, {}).items():
            # If y is not in dist or a shorter path to y is found
            if y not in dist or dist[x] + cost_xy < dist[y]:
                # Update the cost to reach y
                dist[y] = dist[x] + cost_xy
                # Enqueue y with its cost as the priority
                heapq.heappush(q, (dist[y], y))
                # Set the predecessor of y to x
                prev[y] = x

    return dist, prev


# Example usage:
G = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 2, 'D': 5},
    'C': {'D': 1},
    'D': {}
}
s = 'A'
t = 'D'
dist, prev = dijkstra(G, s, t)
print("Distance: ", dist)
print("Predecessors: ", prev)
