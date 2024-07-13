from collections import deque, defaultdict


# exam 2018 no.9
def count_shortest_paths(graph, s, t):
    # Initialize the queue for BFS with the starting vertex s
    Q = deque([s])

    # Dictionary to store the shortest distance from s to each vertex
    distance = defaultdict(lambda: float('inf'))
    distance[s] = 0  # Distance to the starting vertex is 0

    # Dictionary to store the number of shortest paths to each vertex
    count = defaultdict(int)
    count[s] = 1  # There is one path to the starting vertex (itself)

    # Perform BFS
    while Q:
        # Dequeue a vertex from the queue
        u = Q.popleft()

        # Explore all neighbors of u
        for v in graph[u]:
            # If v is being visited for the first time
            if distance[v] == float('inf'):
                distance[v] = distance[u] + 1  # Update the distance to v
                Q.append(v)  # Enqueue v for further exploration

            # If v is reachable via a shortest path through u
            if distance[v] == distance[u] + 1:
                count[v] += count[u]  # Increment the count of shortest paths to v

    # Return the number of shortest paths from s to t
    return count[t]


# Main function to test the count_shortest_paths function
def main():
    # Define a sample graph as an adjacency list
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['D'],
        'D': ['F'],
        'E': ['F'],
        'F': []
    }

    # Starting vertex
    s = 'A'
    # Target vertex
    t = 'F'

    # Call the function and print the result
    num_paths = count_shortest_paths(graph, s, t)
    print(f"The number of distinct shortest paths from {s} to {t} is: {num_paths}")


if __name__ == "__main__":
    main()
