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
        int cutoff = INT_MAX;
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
    cout << s.findMaxFlow();
}