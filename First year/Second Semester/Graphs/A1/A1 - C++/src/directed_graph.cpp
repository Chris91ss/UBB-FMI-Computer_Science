#include "directed_graph.h"
#include "graph_exceptions.h"
using namespace std;

DirectedGraph::DirectedGraph(int number_of_vertices): number_of_vertices(number_of_vertices), number_of_edges(0){
    inbound_edges = {};
    outbound_edges = {};
    costs = {};
}

string DirectedGraph::toString() {
    string result = "DirectedGraph: " + to_string(number_of_vertices) +
                         " vertices, " + to_string(number_of_edges) + " edges\n";
    for (const auto& [vertex, _inbound_edges] : inbound_edges) {
        for (int inbound_edge : _inbound_edges) {
            if (this->inbound_edges[vertex].empty() && this->outbound_edges[vertex].empty()) {
                result += " " + to_string(vertex) + " -> isolated vertex\n";
                continue;
            }
            result += " " + to_string(inbound_edge) + " -> " + to_string(vertex) +
                      " ->: " + to_string(costs[{inbound_edge, vertex}]) + "\n";
        }
    }
    return result;
}

int DirectedGraph::GetNumberOfVertices() const{
    return number_of_vertices;
}

void DirectedGraph::SetNumberOfVertices(int numberOfVertices) {
    DirectedGraph::number_of_vertices = numberOfVertices;
}

bool DirectedGraph::CheckIfEdgeExists(int source, int destination) const {
    return costs.find({source, destination}) != costs.end();
}

int DirectedGraph::GetCostOfAnEdge(int source, int destination) const {
    if (CheckIfEdgeExists(source, destination))
        return costs.at({source, destination});
    else {
        throw GraphException("There is no edge from " + to_string(source) + " to " + to_string(destination));
    }
}

void DirectedGraph::SetCostOfAnEdge(int source, int destination, int cost) {
    // Check if the edge exists
    if (CheckIfEdgeExists(source, destination)) {
        // Update the cost if the edge exists
        costs[make_pair(source, destination)] = cost;
    } else {
        // Add the edge with the specified cost if it doesn't exist
        AddEdge(source, destination, cost);
    }
}

vector<int> DirectedGraph::GetInboundEdges(int vertex) const {
    // Check if the vertex exists in the graph
    auto it = inbound_edges.find(vertex);
    if (it == inbound_edges.end()) {
        throw GraphException("Vertex does not exist in the graph");
    }

    // Return the inbound edges for the vertex
    return it->second;
}

vector<int> DirectedGraph::GetOutboundEdges(int vertex) const {
    // Check if the vertex exists in the graph
    auto it = outbound_edges.find(vertex);
    if (it == outbound_edges.end()) {
        throw GraphException("Vertex does not exist in the graph");
    }

    // Return the outbound edges for the vertex
    return it->second;
}

vector<int> DirectedGraph::GetVertices() const {
    vector<int> vertices;
    vertices.reserve(inbound_edges.size());
    for (const auto& entry : inbound_edges) {
        vertices.push_back(entry.first);
    }
    return vertices;
}

bool DirectedGraph::CheckIfGraphIsEmpty() const {
    return number_of_vertices == 0;
}

void DirectedGraph::AddVertex(int vertex) {
    if (inbound_edges.find(vertex) != inbound_edges.end()) {
        throw GraphException("The vertex already exists");
    }

    inbound_edges[vertex] = {};
    outbound_edges[vertex] = {};
    ++number_of_vertices;
}

void DirectedGraph::RemoveVertex(int vertex) {
    if (inbound_edges.find(vertex) == inbound_edges.end()) {
        throw GraphException("The vertex does not exist");
    }

    for (const auto& [source, _outbound_edges] : outbound_edges) {
        if (CheckIfEdgeExists(source, vertex)) {
            RemoveEdge(source, vertex);
        }
    }

    for (const auto& [destination, _inbound_edges] : inbound_edges) {
        if (CheckIfEdgeExists(vertex, destination)) {
            RemoveEdge(vertex, destination);
        }
    }

    inbound_edges.erase(vertex);
    outbound_edges.erase(vertex);
    --number_of_vertices;
}

void DirectedGraph::AddEdge(int source, int destination, int cost) {
    if (CheckIfEdgeExists(source, destination)) {
        throw GraphException("The edge already exists");
    }

    try {
        AddVertex(source);
    } catch (const GraphException&) {
    }

    try {
        AddVertex(destination);
    } catch (const GraphException&) {
    }

    if (outbound_edges.find(source) == outbound_edges.end()) {
        outbound_edges[source] = {};
    }
    if (inbound_edges.find(destination) == inbound_edges.end()) {
        inbound_edges[destination] = {};
    }

    inbound_edges[destination].push_back(source);
    outbound_edges[source].push_back(destination);
    costs[{source, destination}] = cost;
    ++number_of_edges;
}

void DirectedGraph::RemoveEdge(int source, int destination) {
    if (!CheckIfEdgeExists(source, destination)) {
        throw GraphException("The edge does not exist");
    }

    inbound_edges[destination].erase(remove(inbound_edges[destination].begin(), inbound_edges[destination].end(), source),
                                     inbound_edges[destination].end());
    outbound_edges[source].erase(remove(outbound_edges[source].begin(), outbound_edges[source].end(), destination),
                                  outbound_edges[source].end());
    costs.erase({source, destination});
    --number_of_edges;
}

shared_ptr<DirectedGraph> DirectedGraph::GetCopyOfGraph() const {
    auto graph_copy = make_shared<DirectedGraph>(number_of_vertices);
    graph_copy->inbound_edges = inbound_edges;
    graph_copy->outbound_edges = outbound_edges;
    graph_copy->costs = costs;
    return graph_copy;
}

void DirectedGraph::CreateRandomGraph(int numberOfVertices, int numberOfEdges) {
    if (numberOfEdges > numberOfVertices * (numberOfVertices - 1)) {
        throw GraphException("Invalid input! The number of edges must be less than the number of vertices * (number of vertices - 1)");
    }
    if (this->number_of_vertices != 0) {
        throw GraphException("The graph already exists.");
    }

    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> distribution(1, 100);

    for (int i = 0; i < numberOfVertices; ++i) {
        AddVertex(i);
    }

    uniform_int_distribution<int> cost_distribution(1, 100);
    // Generate all possible edges
    vector<pair<int, int>> possible_edges;
    for (int i = 0; i < numberOfVertices; ++i) {
        for (int j = 0; j < numberOfVertices; ++j) {
            if (i != j) {
                possible_edges.emplace_back(i, j);
            }
        }
    }

    int num_edges = numberOfEdges;
    for (const auto& edge : possible_edges) {
        int source = edge.first;
        int destination = edge.second;
        int cost = cost_distribution(gen); // Random cost between 1 and 100
        AddEdge(source, destination, cost);
        num_edges--;
        if (num_edges == 0) {
            break;
        }
    }
}

void DirectedGraph::ReadGraphFromFile(const string &file_name) {
    ifstream file(file_name);
    if (!file.is_open()) {
        throw GraphException("Unable to open file");
    }

    number_of_edges = 0;
    number_of_vertices = 0;
    inbound_edges.clear();
    outbound_edges.clear();
    costs.clear();

    int num_vertices, num_edges;
    file >> num_vertices >> num_edges;

    for (int vertex = 0; vertex < num_vertices; ++vertex) {
        AddVertex(vertex);
    }

    int source, destination, cost;
    while (num_edges--) {
        file >> source >> destination >> cost;
        AddEdge(source, destination, cost);
    }
}

void DirectedGraph::WriteGraphToFile(const string &file_name) const {
    ofstream file(file_name);
    if (!file.is_open()) {
        throw GraphException("Unable to open file for writing");
    }

    file << number_of_vertices << " " << number_of_edges << "\n";

    for (const auto& [vertex, outboundEdges] : outbound_edges) {
        for (int outbound_edge : outboundEdges) {
            file << vertex << " " << outbound_edge << " " << costs.at({vertex, outbound_edge}) << "\n";
        }
    }
}




