from collections import defaultdict, deque


def topological_sort(graph):
    # Use a dictionary to handle any type of vertex label (int or str).
    in_degree = defaultdict(int)
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    # Use a deque to initialize the queue with vertices having no incoming edges.
    queue = deque([u for u in graph if in_degree[u] == 0])
    topo_order = []

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    # Verify that the sort includes all vertices to confirm the graph is a DAG.
    if len(topo_order) != len(graph):
        raise ValueError("Graph is not a DAG or some vertices are disconnected")

    return topo_order


# exam 2023 no.1&4
def count_max_length_paths(graph, start, end, num_vertices):
    topo_order = topological_sort(graph)
    longest = [-float('inf')] * num_vertices
    count = [0] * num_vertices
    longest[start] = 0
    count[start] = 1
    for u in topo_order:
        if longest[u] != -float('inf'):
            for v in graph[u]:
                if longest[v] < longest[u] + 1:
                    longest[v] = longest[u] + 1
                    count[v] = count[u]
                elif longest[v] == longest[u] + 1:
                    count[v] += count[u]
    return count[end] if longest[end] != -float('inf') else 0


# exam 2023 no.2&3
def find_number_of_min_cost_paths(graph, costs, s, t):
    topo_order = topological_sort(graph)
    min_cost = {u: float('inf') for u in graph}
    min_cost[s] = 0
    count = {u: 0 for u in graph}
    count[s] = 1
    for u in topo_order:
        if min_cost[u] != float('inf'):
            for v in graph[u]:
                edge_cost = costs[(u, v)]
                if min_cost[v] > min_cost[u] + edge_cost:
                    min_cost[v] = min_cost[u] + edge_cost
                    count[v] = count[u]
                elif min_cost[v] == min_cost[u] + edge_cost:
                    count[v] += count[u]
    return count[t] if min_cost[t] != float('inf') else 0


def main():
    # Example for count_max_length_paths
    V = 5
    graph1 = defaultdict(list)
    graph1[0].append(1)
    graph1[0].append(2)
    graph1[1].append(3)
    graph1[2].append(3)
    graph1[3].append(4)
    start_vertex = 0
    end_vertex = 4
    print("Number of distinct maximum length paths:", count_max_length_paths(graph1, start_vertex, end_vertex, V))

    # Example for find_number_of_min_cost_paths
    graph2 = defaultdict(list, {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []})
    costs = {('A', 'B'): 1, ('A', 'C'): 4, ('B', 'D'): 3, ('C', 'D'): 2}
    s, t = 'A', 'D'
    print("Number of minimum cost paths from A to D:", find_number_of_min_cost_paths(graph2, costs, s, t))


if __name__ == "__main__":
    main()
