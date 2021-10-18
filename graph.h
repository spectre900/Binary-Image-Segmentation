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
        freopen("data.txt", "r", stdin);
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

    void findObj()
    {
        queue<int> q;
        vector<int> visited(V, false);

        q.push(source);
        visited[source] = true;

        while (!q.empty())
        {
            int u = q.front();
            q.pop();

            for (pair<int, int> p : adjList[u])
            {
                int v = p.first;
                int w = p.second;
                if (!visited[v] and w)
                {
                    visited[v] = true;
                    q.push(v);
                }
            }
        }

        for (int i = 0; i < visited.size(); i++)
        {
            if (i != source && visited[i])
            {
                cout << i << " ";
            }
        }
    }
};
