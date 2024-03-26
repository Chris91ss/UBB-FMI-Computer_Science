#pragma once
#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <memory>
#include <random>
#include <ctime>
#include <fstream>
#include <sstream>

using namespace std;

class DirectedGraph {

private:
    int number_of_vertices; // The number of vertices in the graph
    int number_of_edges; // The number of edges in the graph
    map<int, vector<int>> inbound_edges; // The map of inbound edges
    map<int, vector<int>> outbound_edges; // The map of outbound edges
    map<pair<int, int>, int> costs; // The map of costs

public:
    DirectedGraph(int number_of_vertices); // constructor for the DirectedGraph class

    string toString(); // convert the graph to a string representation

    int GetNumberOfVertices() const; // returns the number of vertices in the graph

    void SetNumberOfVertices(int numberOfVertices); // sets the number of vertices in the graph

    bool CheckIfEdgeExists(int source, int destination) const; // checks if an edge exists between two vertices, returns true if it exists, false otherwise

    int GetCostOfAnEdge(int source, int destination) const; // returns the cost of an edge between two vertices

    void SetCostOfAnEdge(int source, int destination, int cost); // sets the cost of an edge between two vertices

    vector<int> GetInboundEdges(int vertex) const; // returns the inbound edges of a vertex

    vector<int> GetOutboundEdges(int vertex) const; // returns the outbound edges of a vertex

    vector<int> GetVertices() const; // returns the vertices of the graph

    bool CheckIfGraphIsEmpty() const; // checks if the graph is empty, returns true if it is empty, false otherwise

    void AddVertex(int vertex); // adds a vertex to the graph

    void RemoveVertex(int vertex); // removes a vertex from the graph

    void AddEdge(int source, int destination, int cost); // adds an edge between two vertices with a specified cost

    void RemoveEdge(int source, int destination); // removes an edge between two vertices

    shared_ptr<DirectedGraph> GetCopyOfGraph() const; // returns a copy of the graph

    void CreateRandomGraph(int numberOfVertices, int numberOfEdges); // creates a random graph with a specified number of vertices and edges

    void ReadGraphFromFile(const string& file_name); // reads a graph from a file

    void WriteGraphToFile(const std::string& file_name) const; // writes the graph to a file
};