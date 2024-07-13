from collections import deque


def bfs(G, s):
    # Initialize data structures
    q = deque()
    prev = {}
    dist = {}
    visited = set()

    # Start from the source vertex
    q.append(s)
    visited.add(s)
    dist[s] = 0

    while q:
        x = q.popleft()
        for y in G[x]:  # Assuming G[x] gives the neighbors of x
            if y not in visited:
                q.append(y)
                visited.add(y)
                dist[y] = dist[x] + 1
                prev[y] = x

    accessible = visited
    return accessible, prev


# Example usage:
# G is the graph represented as an adjacency list
# s is the starting vertex
G = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

s = 'A'
accessible, prev = bfs(G, s)
print("Accessible vertices:", accessible)
print("Previous map:", prev)
