from copy import deepcopy
import numpy as np
import networkx as nx

def uniformWeights(G) -> dict:
    '''
    Every incoming edge of v with degree dv has weight 1/dv.
    '''
    Ew = dict()
    for u in G:
        in_edges = G.in_edges([u], data=True)
        dv = sum([edata['weight'] for v1, v2, edata in in_edges])
        for v1,v2,_ in in_edges:
            Ew[(v1,v2)] = 1/dv
    return Ew

def randomWeights(G) -> dict:
    '''
    Every edge has random weight.
    After weights assigned,
    we normalize weights of all incoming edges so that they sum to 1.
    '''
    np.random.seed(0)
    Ew = dict()
    for u in G:
        in_edges = G.in_edges([u], data=True)
        ew = [np.random.random() for e in in_edges] # random edge weights
        total = 0 # total sum of weights of incoming edges (for normalization)
        for num, (v1, v2, edata) in enumerate(in_edges):
            total += edata['weight']*ew[num]
        for num, (v1, v2, _) in enumerate(in_edges):
            Ew[(v1,v2)] = ew[num]/total
    return Ew

def checkLT(G, Ew, eps = 1e-4) -> bool:
    ''' To verify that sum of all incoming weights <= 1
    '''
    for u in G:
        in_edges = G.in_edges([u], data=True)
        total = 0
        for (v1, v2, edata) in in_edges:
            total += Ew[(v1, v2)]*G[v1][v2]['weight']
        if total >= 1 + eps:
            return('For node {} LT property is incorrect. Sum equals to {}').format(u,total)
    return True

def runLT(G, S, Ew) -> list:
    '''
    Input: G -- networkx directed graph
    S -- initial seed set of nodes
    Ew -- influence weights of edges
    NOTE: multiple k edges between nodes (u,v) are
    considered as one node with weight k. For this reason
    when u is activated the total weight of (u,v) = Ew[(u,v)]*k
    '''

    np.random.seed(0)

    T = deepcopy(S) # targeted set
    threshold = dict() # threshold for nodes
    
    for u in G:
        threshold[u] = np.random.random()

    W = dict(zip(G.nodes(), [0]*len(G))) # weighted number of activated in-neighbors
    Sj = deepcopy(S)

    while len(Sj): # while we have newly activated nodes
        Snew = []
        for u in Sj:
            for v in G[u]:
                if v not in T:
                    W[v] += Ew[(u,v)]*G[u][v]['weight']
                    if W[v] >= threshold[v]:
                        Snew.append(v)
                        T.append(v)
        Sj = deepcopy(Snew)
    return T

def avgLT(G, S, Ew, iterations) -> float:
    avgSize = 0
    for i in range(iterations):
        T = runLT(G, S, Ew)
        avgSize += len(T)/iterations

    return avgSize