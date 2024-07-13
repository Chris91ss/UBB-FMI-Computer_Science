import networkx as nx


def is_valid_vertex(v, pos, path, graph):
    # Check if the current vertex and the last vertex in the path are adjacent
    if graph.has_edge(path[pos - 1], v) == 0:
        return False

    # Check if the vertex has already been included
    if v in path:
        return False

    return True


def hamiltonian_cycle_util(graph, path, pos):
    # Base case: full cycle is found
    if pos == len(graph):
        # And if there is an edge from the last vertex to the first vertex
        if graph.has_edge(path[pos - 1], path[0]):
            path.append(path[0])  # To complete the cycle
            return True
        else:
            return False

    # Try different vertices as the next candidate in the Hamiltonian Cycle
    for v in graph.nodes():
        if is_valid_vertex(v, pos, path, graph):
            path[pos] = v

            if hamiltonian_cycle_util(graph, path, pos + 1):
                return True

            # If adding vertex v doesn't lead to a solution, remove it
            path[pos] = -1

    return False


def find_hamiltonian_cycle(graph):
    path = [-1] * len(graph)
    # Start with the first vertex in the graph
    path[0] = list(graph.nodes())[0]

    if not hamiltonian_cycle_util(graph, path, 1):
        print("No Hamiltonian Cycle exists")
        return None

    # Print the solution
    print("Hamiltonian Cycle exists:", path)
    return path


# Example usage
if __name__ == "__main__":
    # Create a sample graph
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)])

    cycle = find_hamiltonian_cycle(G)
    if cycle:
        print("Hamiltonian Cycle found:", cycle)
