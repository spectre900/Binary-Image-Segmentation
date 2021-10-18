#include <bits/stdc++.h>
#include "graph.h"

using namespace std;

class EdmondKarp : public Graph
{
public:
    int bfs()
    {
        int flow = INT_MAX;
        vector<int> parent(V, -1);

        queue<int> q;
        q.push(source);

        while (!q.empty())
        {
            int u = q.front();
            q.pop();

            for (pair<int, int> edge : adjList[u])
            {
                int v = edge.first;
                int w = edge.second;
                if (v != source and parent[v] == -1 and w > 0)
                {
                    q.push(v);
                    parent[v] = u;
                }
            }
        }

        if (parent[sink] == -1)
            return 0;

        int v = sink;
        int u = parent[v];

        while (u != -1)
        {
            flow = min(flow, adjList[u][v]);
            v = u;
            u = parent[u];
        }

        v = sink;
        u = parent[v];

        while (u != -1)
        {
            adjList[u][v] -= flow;
            adjList[v][u] += flow;

            v = u;
            u = parent[u];
        }

        return flow;
    }
    int findMaxFlow()
    {
        while (true)
        {
            int flow = bfs();
            if (flow)
            {
                maxFlow += flow;
                done = vector<bool>(V, false);
                continue;
            }
            break;
        }
        return maxFlow;
    }
};

int main()
{
    EdmondKarp ek = EdmondKarp();
    ek.readInput();
    ek.findMaxFlow();
    ek.findObj();
}