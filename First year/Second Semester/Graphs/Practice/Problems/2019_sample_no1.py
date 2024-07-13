from collections import deque, defaultdict


# exam 2019 no.1
def find_minimum_cycle(graph, start_vertex):
    # Distance dictionary to keep track of distances from the start vertex
    distance = {}
    # Queue for BFS: stores tuple (current vertex, distance, path)
    queue = deque([(start_vertex, 0, [])])
    # Minimum cycle length initialized as infinity
    min_cycle_length = float('inf')
    # Path of the minimum cycle
    min_cycle_path = []

    while queue:
        current, dist, path = queue.popleft()

        for neighbor in graph[current]:
            # If the neighbor is the start vertex and the path length is non-zero,
            # we found a cycle.
            if neighbor == start_vertex and len(path) > 0:
                if dist + 1 < min_cycle_length:
                    min_cycle_length = dist + 1
                    min_cycle_path = path + [current]
            elif neighbor not in path:
                # Continue with BFS if the neighbor hasn't been visited in this path
                queue.append((neighbor, dist + 1, path + [current]))
                distance[neighbor] = dist + 1

    return min_cycle_length, min_cycle_path if min_cycle_length != float('inf') else None


def main():
    # Example graph represented as an adjacency list
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D', 'E'],
        'D': ['A'],  # Back to A, forming a cycle A -> B -> C -> D -> A
        'E': ['F'],
        'F': ['C'],  # No cycle through F directly
    }

    # Start vertex
    start_vertex = 'A'
    # Find the minimum cycle
    cycle_length, cycle_path = find_minimum_cycle(graph, start_vertex)
    print("Minimum cycle length:", cycle_length)
    print("Cycle path:", cycle_path)


if __name__ == "__main__":
    main()
