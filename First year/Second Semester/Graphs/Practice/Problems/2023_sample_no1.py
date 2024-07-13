from collections import defaultdict, deque


def topological_sort(graph, V):
    indegree = [0] * V
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1

    queue = deque([v for v in range(V) if indegree[v] == 0])
    topo_order = []

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    return topo_order


def count_max_length_paths(graph, start, end, V):
    # Topologically sort the vertices
    topo_order = topological_sort(graph, V)

    # Array to store the longest distances and path count
    longest = [-float('inf')] * V
    count = [0] * V
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


def main():
    # Example graph and vertices
    V = 5
    graph = defaultdict(list)
    graph[0].append(1)
    graph[0].append(2)
    graph[1].append(3)
    graph[2].append(3)
    graph[3].append(4)

    start_vertex = 0
    end_vertex = 4

    # Calling the function
    result = count_max_length_paths(graph, start_vertex, end_vertex, V)
    print("Number of distinct maximum length paths:", result)


if __name__ == "__main__":
    main()
