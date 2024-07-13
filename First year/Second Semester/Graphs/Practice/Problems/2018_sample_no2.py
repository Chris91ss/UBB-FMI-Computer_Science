from collections import deque, defaultdict


# exam 2018 no.2
def find_minimum_cycle(graph):
    def bfs(start):
        # Using a local visited set for each BFS to prevent re-visiting nodes in the same traversal
        visited = set()
        queue = deque([(start, [])])  # Start with an empty path

        while queue:
            current, path = queue.popleft()
            visited.add(current)

            for neighbor in graph[current]:
                if neighbor in path:
                    # Cycle found
                    cycle_length = len(path) + 1  # Corrected cycle length calculation
                    return cycle_length, path + [neighbor]  # Return path including the current node and neighbor
                if neighbor not in visited:
                    queue.append((neighbor, path + [current]))  # Include current node in path

        return float('inf'), []  # No cycle from this start node

    # Global visited set to prevent re-processing nodes from which no cycle can be started
    global_visited = set()
    min_cycle_length = float('inf')
    min_cycle = []

    for node in graph:
        if node not in global_visited:
            cycle_length, cycle = bfs(node)
            if cycle_length < min_cycle_length:
                min_cycle_length = cycle_length
                min_cycle = cycle
            global_visited.update(set(cycle))  # Mark all nodes in the cycle as visited globally

    return min_cycle_length, min_cycle if min_cycle else None


def main():
    # Example of how to use the function:
    graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['D', 'E'],
        'D': ['A'],  # Back to A, forming a cycle A -> B -> C -> D -> A
        'E': ['F'],
        'F': []
    }

    cycle_length, cycle = find_minimum_cycle(graph)
    print("Cycle length:", cycle_length)
    print("Cycle path:", cycle)


if __name__ == '__main__':
    main()
