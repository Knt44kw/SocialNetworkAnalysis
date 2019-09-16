import networkx as nx

def generateGraph(filename) -> nx.Graph:
     with open('{}'.format(filename)) as f:
        n, m = map(int, f.readline().split())
        G = nx.DiGraph()
        for line in f:
            u, v = map(int, line.split())
            try:
                G[u][v]['weight'] += 1
            except KeyError:
                G.add_edge(u,v,weight=1)
            try:
                G[v][u]['weight'] += 1
            except KeyError:
                G.add_edge(v,u,weight=1)
        return G