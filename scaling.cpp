#include <bits/stdc++.h>
#include "graph.h"

using namespace std;

class Scaling : public Graph
{
public:
    int dfs(int u, int cutoff, int flow = INT_MAX)
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
            if (!done[v] and w >= cutoff)
            {
                int curFlow = dfs(v, cutoff, min(flow, w));
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
        int cutoff = 1000;
        while (cutoff)
        {
            int flow = dfs(source, cutoff);
            if (flow)
            {
                maxFlow += flow;
                done = vector<bool>(V, false);
            }
            else
            {
                cutoff /= 2;
            }
        }
        return maxFlow;
    }
};

int main()
{
    Scaling s = Scaling();
    s.readInput();

    clock_t start, end;
    start = clock();
    s.findMaxFlow();
    s.findForeGround();
    end = clock();

    double duration = double(end - start) / double(CLOCKS_PER_SEC);
    cout << duration;
}