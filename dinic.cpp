#include <bits/stdc++.h>
#include "graph.h"

using namespace std;

class Dinic : public Graph
{
    vector<int> level;

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
            if (w and level[v] == level[u] + 1)
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

    int bfs()
    {
        level = vector<int>(V, -1);

        queue<int> q;
        q.push(source);

        level[source] = 0;

        while (!q.empty())
        {
            int u = q.front();
            q.pop();

            for (pair<int, int> edge : adjList[u])
            {
                int v = edge.first;
                int w = edge.second;
                if (w and level[v] == -1)
                {
                    q.push(v);
                    level[v] = level[u] + 1;
                }
            }
        }

        return level[sink] != -1;
    }

    int findMaxFlow()
    {
        while (bfs())
        {
            while (true)
            {
                int flow = dfs(source);
                if (flow)
                {
                    maxFlow += flow;
                    continue;
                }
                break;
            }
        }
        return maxFlow;
    }
};

int main()
{
    Dinic d = Dinic();
    d.readInput();

    clock_t start, end;
    start = clock();
    d.findMaxFlow();
    d.findForeGround();
    end = clock();

    double duration = double(end - start) / double(CLOCKS_PER_SEC);
    cout << duration;
}