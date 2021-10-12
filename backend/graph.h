#include <bits/stdc++.h>

using namespace std;

class Graph
{
protected:
    int V;
    int E;
    int sink;
    int source;
    int maxFlow;
    vector<bool> done;
    vector<unordered_map<int, int>> adjList;

public:
    Graph()
    {
        maxFlow = 0;
        cin >> V >> E;
        cin >> source >> sink;
        done = vector<bool>(V, false);
        adjList = vector<unordered_map<int, int>>(V);
    }

    void readInput()
    {
        for (int i = 0; i < E; i++)
        {
            int u, v, w;
            cin >> u >> v >> w;
            u--, v--;

            if (adjList[u].find(v) == adjList[u].end())
            {
                adjList[u][v] = 0;
            }
            adjList[u][v] += w;
            if (adjList[v].find(u) == adjList[v].end())
            {
                adjList[v][u] = 0;
            }
        }
    }
};
