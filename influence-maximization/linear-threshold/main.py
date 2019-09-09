import networkx as nx
from linear_threshold import *
from greedy import generalGreedy
from copy import deepcopy

def main():
    with open('./dataset/facebook_combined.txt') as f:
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

    Ewu = uniformWeights(G)
    # Ewr = randomWeights(G)

    S = generalGreedy(G, Ewu, k=10, iterations=20)
    print('S:(Set of the most influential Users)  is {}'.format(S))
    print('Activated Users by S (Average) {:.3f} out of {}'.format(avgLT(G, S, Ewu, 200), len(G)))

if __name__ == "__main__":
    main()
   