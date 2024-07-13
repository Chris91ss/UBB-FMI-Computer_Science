import heapq


def prim_algorithm(G):
    # G is assumed to be a dictionary of dictionaries where G[u][v] is the cost of edge (u, v)

    # Initialize structures
    q = []
    prev = {}
    dist = {}
    edges = []
    s = next(iter(G))  # Choose an arbitrary starting vertex
    vertices = {s}

    # Initialize distances and priority queue
    for x in G[s]:
        dist[x] = G[s][x]
        prev[x] = s
        heapq.heappush(q, (dist[x], x))

    while q:
        d, x = heapq.heappop(q)  # Dequeues the element with minimum value of priority (cost)
        if x not in vertices:
            edges.append((x, prev[x]))
            vertices.add(x)
            for y in G[x]:
                if y not in dist or G[x][y] < dist[y]:
                    dist[y] = G[x][y]
                    heapq.heappush(q, (dist[y], y))
                    prev[y] = x

    return edges


# Example usage
G = {
    1: {2: 1, 3: 3, 6: 2},
    2: {1: 1, 3: 1},
    3: {1: 3, 2: 1, 4: 2, 5: 3, 6: 2},
    4: {3: 2, 5: 1},
    5: {3: 3, 4: 1},
    6: {1: 2, 3: 2}
}

print(prim_algorithm(G))
