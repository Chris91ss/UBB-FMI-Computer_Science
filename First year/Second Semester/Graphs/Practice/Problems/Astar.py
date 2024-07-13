import heapq


def astar_algorithm(graph, start, goal, h):
    """
    A* algorithm implementation.

    Parameters:
    graph: A dictionary where keys are node names and values are dictionaries of neighboring nodes and their costs.
    start: The starting node.
    goal: The goal node.
    h: A function that estimates the distance from a node to the goal.

    Returns:
    dist: A dictionary with the minimum cost from start to each accessible node.
    prev: A dictionary that maps each accessible node to its predecessor on the path from start.
    """
    # Priority queue
    pq = []
    heapq.heappush(pq, (h(start), start))

    # Dictionaries to store distances and predecessors
    dist = {start: 0}
    prev = {}

    found = False

    while pq and not found:
        _, current = heapq.heappop(pq)

        if current == goal:
            found = True
            break

        for neighbor, cost in graph[current].items():
            new_cost = dist[current] + cost
            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                priority = new_cost + h(neighbor)
                heapq.heappush(pq, (priority, neighbor))
                prev[neighbor] = current

    return dist, prev


# Example usage:
if __name__ == "__main__":
    # Define a graph as a dictionary of dictionaries
    graph = {
        'A': {'B': 1, 'C': 3},
        'B': {'A': 1, 'C': 1, 'D': 4},
        'C': {'A': 3, 'B': 1, 'D': 1},
        'D': {'B': 4, 'C': 1}
    }

    # Define a simple heuristic function
    def heuristic(node):
        heuristics = {
            'A': 4,
            'B': 2,
            'C': 1,
            'D': 0
        }
        return heuristics.get(node, 0)


    start = 'A'
    goal = 'D'

    dist, prev = astar_algorithm(graph, start, goal, heuristic)
    print("Distances:", dist)
    print("Predecessors:", prev)
