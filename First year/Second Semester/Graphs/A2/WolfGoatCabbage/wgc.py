from WolfGoatCabbage.graphs.wgc_graph import WolfGoatCabbageGraph


def shortest_path_wgc(graph, start, end):
    """
    Computes the shortest (min length) walk between start and end in graph.

    :param graph: the graph
    :param start: the start point
    :param end: the end point

    :return: a list of vertices representing the shortest path between the start and end vertices
             [], empty list if no path exists
    """

    def bfs(_graph, start_v):
        distance = {start_v: 0}
        queue = [start_v]

        while queue:
            current = queue.pop(0)
            for neighbor in _graph.get_neighbors(current):
                if neighbor not in distance:
                    distance[neighbor] = distance[current] + 1
                    queue.append(neighbor)

        return distance

    dist = bfs(graph, start)
    if end not in dist:
        return []

    walk = [end]
    current_length, current_vertex = dist[end], end
    while current_length:
        current_length -= 1
        for vertex in graph.get_neighbors(current_vertex):
            if vertex in dist and dist[vertex] == current_length:
                current_vertex = vertex
                walk.append(current_vertex)
                break

    walk.reverse()
    return walk


def shortest_wgc():
    graph = WolfGoatCabbageGraph()
    start = graph.get_start()
    end = graph.get_end()

    return shortest_path_wgc(graph, start, end)


def run_app():
    solution = shortest_wgc()
    print(f"\nThe solution to the Wolf, Goat, Cabbage problem has length {len(solution)} and is: ")
    for move in solution:
        print(move)
