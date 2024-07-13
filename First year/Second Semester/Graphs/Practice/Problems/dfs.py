def dfs(G, s):
    # Initialize data structures
    stack = [s]
    prev = {}
    visited = set()
    dist = {}

    # Start from the source vertex
    visited.add(s)
    dist[s] = 0

    while stack:
        x = stack.pop()
        for y in G[x]:  # Assuming G[x] gives the neighbors of x
            if y not in visited:
                stack.append(y)
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
accessible, prev = dfs(G, s)
print("Accessible vertices:", accessible)
print("Previous map:", prev)
