#include <bits/stdc++.h>
#include "graph.h"

using namespace std;

class FordFulkerson : public Graph
{
public:
    int dfs(int u, int flow = INT_MAX)
    {
        if (u == sink)
        {
            return flow;
        }
        done[u] = true;
        for (pair<int, int> edge : adjList[u])
        {
            int v = edge.first;
            int w = edge.second;
            if (!done[v] and w)
            {
                int curFlow = dfs(v, min(flow, w));
                if (curFlow)
                {
                    adjList[u][v] -= curFlow;
                    adjList[v][u] += curFlow;
                    return curFlow;
                }
            }
        }
        return 0;
    }
    int findMaxFlow()
    {
        while (true)
        {
            int flow = dfs(source);
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
    FordFulkerson ff = FordFulkerson();
    ff.readInput();

    clock_t start, end;
    start = clock();
    ff.findMaxFlow();
    ff.findForeGround();
    end = clock();

    double duration = double(end - start) / double(CLOCKS_PER_SEC);
    cout << duration;
}