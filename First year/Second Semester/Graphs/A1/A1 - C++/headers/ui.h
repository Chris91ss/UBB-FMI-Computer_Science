#include "directed_graph.h"
#include "graph_exceptions.h"
#include <functional>

class UI{

private:
    DirectedGraph graph;
    DirectedGraph originalGraph;

public:
    UI();

    void run();

    static void PrintMenu();

    void GetNumberOfVertices();

    void PrintTheGraph();

    void PrintTheVerticesOfTheGraph();

    void CheckIfEdgeExistsBetweenTwoVertices();

    void GetInDegreeAndOutDegreeOfAVertex();

    void PrintTheInboundEdgesOfAVertex();

    void PrintTheOutboundEdgesOfAVertex();

    void GetCostOfAnEdge();

    void ModifyCostOfAnEdge();

    void AddVertex();

    void RemoveVertex();

    void AddEdge();

    void RemoveEdge();

    void CreateACopyOfTheCurrentGraph();

    void RestoreTheGraphToTheCopy();

    void CreateARandomGraph();

    void ReadFromFile();

    void WriteToFile();

    static void ExitApp();
};