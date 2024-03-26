#include "ui.h"

UI::UI(): graph(0), originalGraph(0){
}

void UI::run() {
    cout << "\"~~~ Graph Algorithms in C++! ~~~ \n";

    map<string, function<void()>> inputOptions = {
            {"1", [this] { this->GetNumberOfVertices(); }},
            {"2", [this] { this->PrintTheGraph(); }},
            {"3", [this] { this->PrintTheVerticesOfTheGraph(); }},
            {"4", [this] { this->CheckIfEdgeExistsBetweenTwoVertices(); }},
            {"5", [this] { this->GetInDegreeAndOutDegreeOfAVertex(); }},
            {"6", [this] { this->PrintTheInboundEdgesOfAVertex(); }},
            {"7", [this] { this->PrintTheOutboundEdgesOfAVertex(); }},
            {"8", [this] { this->GetCostOfAnEdge(); }},
            {"9", [this] { this->ModifyCostOfAnEdge(); }},
            {"10", [this] { this->AddVertex(); }},
            {"11", [this] { this->RemoveVertex(); }},
            {"12", [this] { this->AddEdge(); }},
            {"13", [this] { this->RemoveEdge(); }},
            {"copy", [this] { this->CreateACopyOfTheCurrentGraph(); }},
            {"restore", [this] { this->RestoreTheGraphToTheCopy(); }},
            {"create", [this] { this->CreateARandomGraph(); }},
            {"read", [this] { this->ReadFromFile(); }},
            {"write", [this] { this->WriteToFile(); }},
            {"exit", [] { UI::ExitApp(); }},
    };

    while (true) {
        PrintMenu();
        cout << "\nEnter a command: ";
        string command;
        cin >> command;
        try {
            inputOptions.at(command)();
        } catch (const out_of_range&) {
            cout << "Invalid command\n";
        }
    }
}

void UI::PrintMenu() {
    cout << "1. Get the number of vertices" << endl;
    cout << "2. Print the graph" << endl;
    cout << "3. Print the vertices of the graph" << endl;
    cout << "4. Given two vertices, find out whether there is an edge from the first one to the second one" << endl;
    cout << "5. Get the in degree and out degree of a vertex" << endl;
    cout << "6. Print the inbound edges of a vertex" << endl;
    cout << "7. Print the outbound edges of a vertex" << endl;
    cout << "8. Get the cost of an edge" << endl;
    cout << "9. Modify the cost of an edge" << endl;
    cout << "10. Add a vertex" << endl;
    cout << "11. Remove a vertex" << endl;
    cout << "12. Add an edge" << endl;
    cout << "13. Remove an edge" << endl;
    cout << "copy. Create a copy of the current graph" << endl;
    cout << "restore. Restore the graph to the copy" << endl;
    cout << "create. Create a random graph" << endl;
    cout << "read. Read a graph from a file" << endl;
    cout << "write. Write the graph to a file" << endl;
    cout << "exit. Exit the application" << endl;
}

void UI::GetNumberOfVertices() {
    cout << "The number of vertices is: " << graph.GetNumberOfVertices() << endl;
}

void UI::PrintTheGraph() {
    cout << "The graph is: \n" << graph.toString() << endl;
}

void UI::PrintTheVerticesOfTheGraph() {
    cout << "The vertices of the graph are: ";
    for (int vertex : graph.GetVertices()) {
        cout << vertex << " ";
    }
    cout << endl;
}

void UI::CheckIfEdgeExistsBetweenTwoVertices() {
    int source, destination;
    cout << "Enter the source vertex: ";
    cin >> source;
    cout << "Enter the destination vertex: ";
    cin >> destination;

    try {
        if (graph.CheckIfEdgeExists(source, destination)) {
            cout << "There is an edge from " << source << " to " << destination << endl;
        } else {
            cout << "There is no edge from " << source << " to " << destination << endl;
        }
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::GetInDegreeAndOutDegreeOfAVertex() {
    int vertex;
    cout << "Enter the vertex: ";
    cin >> vertex;

    try {
        int in_degree = graph.GetInboundEdges(vertex).size();
        int out_degree = graph.GetOutboundEdges(vertex).size();
        cout << "The in degree of " << vertex << " is " << in_degree << " and the out degree of " << vertex << " is " << out_degree << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::PrintTheInboundEdgesOfAVertex() {
    int vertex;
    cout << "Enter the vertex: ";
    cin >> vertex;

    try {
        vector<int> inboundEdges = graph.GetInboundEdges(vertex);
        cout << "The inbound edges of " << vertex << " are: ";
        for (int edge : inboundEdges) {
            cout << edge << " ";
        }
        cout << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::PrintTheOutboundEdgesOfAVertex() {
    int vertex;
    cout << "Enter the vertex: ";
    cin >> vertex;

    try {
        vector<int> outboundEdges = graph.GetOutboundEdges(vertex);
        cout << "The outbound edges of " << vertex << " are: ";
        for (int edge : outboundEdges) {
            cout << edge << " ";
        }
        cout << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::GetCostOfAnEdge() {
    int source, destination;
    cout << "Enter the source vertex: ";
    cin >> source;
    cout << "Enter the destination vertex: ";
    cin >> destination;

    try {
        int cost = graph.GetCostOfAnEdge(source, destination);
        cout << "The cost of the edge from " << source << " to " << destination << " is " << cost << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::ModifyCostOfAnEdge() {
    int source, destination, cost;
    cout << "Enter the source vertex: ";
    cin >> source;
    cout << "Enter the destination vertex: ";
    cin >> destination;
    cout << "Enter the new cost: ";
    cin >> cost;

    try {
        graph.SetCostOfAnEdge(source, destination, cost);
        cout << "The cost of the edge from " << source << " to " << destination << " has been modified to " << cost << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::AddVertex() {
    int vertex;
    cout << "Enter the vertex: ";
    cin >> vertex;

    try {
        graph.AddVertex(vertex);
        cout << "The vertex " << vertex << " has been added to the graph" << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::RemoveVertex() {
    int vertex;
    cout << "Enter the vertex: ";
    cin >> vertex;

    try {
        graph.RemoveVertex(vertex);
        cout << "The vertex " << vertex << " has been removed from the graph" << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::AddEdge() {
    int source, destination, cost;
    cout << "Enter the source vertex: ";
    cin >> source;
    cout << "Enter the destination vertex: ";
    cin >> destination;
    cout << "Enter the cost of the edge: ";
    cin >> cost;

    try {
        graph.AddEdge(source, destination, cost);
        cout << "The edge from " << source << " to " << destination << " with cost " << cost << " has been added to the graph" << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::RemoveEdge() {
    int source, destination;
    cout << "Enter the source vertex: ";
    cin >> source;
    cout << "Enter the destination vertex: ";
    cin >> destination;

    try {
        graph.RemoveEdge(source, destination);
        cout << "The edge from " << source << " to " << destination << " has been removed from the graph" << endl;
    } catch (const GraphException& e) {
        cout << e.what() << endl;
    }
}

void UI::CreateACopyOfTheCurrentGraph() {
    if (!originalGraph.CheckIfGraphIsEmpty()) {
        cout << "There is already a copy of the graph" << endl;
        return;
    }

    originalGraph = graph;
    shared_ptr<DirectedGraph> copied_graph = graph.GetCopyOfGraph();
    graph = *copied_graph;
    cout << "The current graph has been copied" << endl;
}

void UI::RestoreTheGraphToTheCopy() {
    if (originalGraph.CheckIfGraphIsEmpty()) {
        cout << "There is no copy of the graph" << endl;
        return;
    }

    graph = originalGraph;
    originalGraph.SetNumberOfVertices(0);
    cout << "The graph has been restored to the copy" << endl;
}

void UI::CreateARandomGraph() {
    int number_of_vertices, number_of_edges;
    cout << "Enter the number of vertices: ";
    cin >> number_of_vertices;
    cout << "Enter the number of edges: ";
    cin >> number_of_edges;

    try {
        graph.CreateRandomGraph(number_of_vertices, number_of_edges);
        cout << "A random graph with " << number_of_vertices << " vertices and " << number_of_edges << " edges has been created" << endl;
    } catch (const GraphException& ge) {
        cout << ge.what() << endl;
    }
}

void UI::ReadFromFile() {
    string file_name, file_path;
    cout << "Enter the file name: ";
    cin >> file_name;

    file_path = "../data/" + file_name;

    try {
        graph.ReadGraphFromFile(file_path);
        cout << "The graph has been read from the file " << file_name << endl;
    } catch (const GraphException& ge) {
        cout << ge.what() << endl;
    }
}

void UI::WriteToFile() {
    string file_name, file_path;
    cout << "Enter the file name: ";
    cin >> file_name;

    file_path = "../data/" + file_name;

    graph.WriteGraphToFile(file_path);
    cout << "The graph has been written to the file " << file_name << endl;
}

void UI::ExitApp() {
    cout << "Goodbye!" << endl;
    exit(EXIT_SUCCESS);
}


