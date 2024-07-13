from collections import defaultdict, deque


def kosaraju_algorithm(graph):
    def DF1(graph, vertex, visited, processed):
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                DF1(graph, neighbor, visited, processed)
        processed.append(vertex)

    def reverse_graph(graph):
        reversed_graph = defaultdict(list)
        for vertex in graph:
            for neighbor in graph[vertex]:
                reversed_graph[neighbor].append(vertex)
        return reversed_graph

    # Step 1: Order the vertices using the first DFS
    processed = []
    visited = set()
    for vertex in graph:
        if vertex not in visited:
            visited.add(vertex)
            DF1(graph, vertex, visited, processed)

    # Step 2: Reverse the graph
    reversed_graph = reverse_graph(graph)

    # Step 3: Process the vertices in the order defined by the stack
    visited.clear()
    component_id = 0
    comp = {}

    while processed:
        vertex = processed.pop()
        if vertex not in visited:
            component_id += 1
            q = deque([vertex])
            visited.add(vertex)
            comp[vertex] = component_id
            while q:
                v = q.popleft()
                for neighbor in reversed_graph[v]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        q.append(neighbor)
                        comp[neighbor] = component_id

    return comp


# Example usage:
graph = {
    0: [1],
    1: [2],
    2: [0, 3],
    3: [4],
    4: [5, 7],
    5: [6],
    6: [4],
    7: []
}

components = kosaraju_algorithm(graph)
print(components)
