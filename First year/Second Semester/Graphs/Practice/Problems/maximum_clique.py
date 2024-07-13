import networkx as nx


def bron_kerbosch(graph, R, P, X, cliques):
    if len(P) == 0 and len(X) == 0:
        cliques.append(R)
        return
    for v in list(P):
        bron_kerbosch(graph, R.union([v]), P.intersection(set(graph.neighbors(v))), X.intersection(set(graph.neighbors(v))), cliques)
        P.remove(v)
        X.add(v)


def find_maximum_clique(graph):
    cliques = []
    bron_kerbosch(graph, set(), set(graph.nodes()), set(), cliques)
    max_clique = max(cliques, key=len)
    return max_clique


# Example usage
if __name__ == "__main__":
    # Create a sample graph
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (3, 5)])

    max_clique = find_maximum_clique(G)
    print("Maximum Clique:", max_clique)
