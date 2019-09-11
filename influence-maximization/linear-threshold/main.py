import networkx as nx
from linear_threshold import *
from greedy import generalGreedy
from copy import deepcopy
from joblib import Parallel, delayed

def main():
    with open('./dataset/karate.edgelist') as f:
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

    Ewu = Parallel(n_jobs=-1, verbose=5)([delayed(uniformWeights)(G)]) 
    # Ewr = Parallel(n_jobs=-1, verbose=5)([delayed(randomWeights)(G)])

    S = Parallel(n_jobs=-1, verbose=5)([delayed(generalGreedy)(G, Ewu[0], k=10, iterations=20)]) 
    print("Set of most influential Users {}".format(S[0][:]))

    influenced_users =  Parallel(n_jobs=-1, verbose=5)([delayed(avgLT)(G, S[0][:], Ewu[0], iterations=200)]) 
    print('Activated Users by S (Average) {:.3f} out of {}'.format(influenced_users[0], len(G)))

if __name__ == "__main__":
    main()
   