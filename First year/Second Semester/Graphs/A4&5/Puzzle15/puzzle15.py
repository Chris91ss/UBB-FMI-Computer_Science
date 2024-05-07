import heapq

from Puzzle15.graphs.puzzle15_graph import Puzzle15Graph


def shortest_path_15puzzle(_graph, start, end):
    """
    Computes the shortest (min length) walk between start and end in graph.

    :param _graph: the graph
    :param start: the start point
    :param end: the end point

    :return: a list of vertices representing the shortest path between the start and end vertices
             [], empty list if no path exists
    """

    def heuristic(node):
        # A simple heuristic that estimates the distance from node to end
        # In this case, we use the number of misplaced tiles as the heuristic value
        # Since it's an admissible heuristic, the algorithm is guaranteed to find the optimal path
        distance = 0
        for i in range(16):
            if node.state[i] != end.state[i]:
                distance += 1
        return distance

    def a_star(graph, start, end):
        # Initialize the priority queue with the start node and its estimated distance
        queue = [(heuristic(start), start)]
        visited = set()
        # Initialize the distances of all nodes to infinity except the start node
        dist = {start: 0}

        while queue:
            # Get the node with the lowest estimated distance
            current_distance, current_node = heapq.heappop(queue)
            if current_node == end:
                break
            # If the node has already been visited, skip it
            if current_node in visited:
                continue
            visited.add(current_node)

            # Explore all neighbors of the current node
            for neighbor in graph.get_neighbors(current_node):
                # Calculate the tentative distance from start to neighbor
                tentative_distance = dist[current_node] + 1
                if tentative_distance < dist.get(neighbor, float('inf')):
                    # Update the distance of neighbor if it's shorter than the previous distance
                    dist[neighbor] = tentative_distance
                    # Estimate the total distance from start to end through neighbor
                    total_distance = tentative_distance + heuristic(neighbor)
                    # Add neighbor to the priority queue with its estimated distance
                    heapq.heappush(queue, (total_distance, neighbor))

        return dist

    dist = a_star(_graph, start, end)
    if end not in dist:
        return []

    walk = [end]
    current_length, current_vertex = dist[end], end
    while current_length:
        current_length -= 1
        for vertex in _graph.get_neighbors(current_vertex):
            if vertex in dist and dist[vertex] == current_length:
                current_vertex = vertex
                walk.append(current_vertex)
                break

    walk.reverse()
    return walk


def shortest_15puzzle():
    graph = Puzzle15Graph()
    dummy_start = graph.get_dummy_start()
    start = graph.get_random_start()
    end = graph.get_end()

    return shortest_path_15puzzle(graph, dummy_start, end)


def run_app():
    solution = shortest_15puzzle()
    print(f"\nThe solution to the 15-puzzle problem has length {len(solution) - 1} and is: \n")
    for move in solution:
        print(f"{move}\n")
    with open("output.txt", "w") as file:
        file.write(f"The solution to the 15-puzzle problem has length {len(solution) - 1} and is: \n")
        for move in solution:
            file.write(f"{str(move)}\n")
