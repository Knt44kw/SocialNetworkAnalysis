from copy import deepcopy 
from priority_queue import PriorityQueue as PQ
import numpy as np
import networkx as nx


def bfs(E, S):
    ''' Finds all vertices reachable from subset S in graph E using Breadth-First Search
    Input: E -- networkx graph object
    S -- list of initial vertices
    Output: Rs -- list of vertices reachable from S
    '''
    Rs = []
    for u in S:
        if u in E:
            if u not in Rs: Rs.append(u)
            for v in E[u].keys():
                if v not in Rs: Rs.append(v)
    return Rs

def findCCs(G, Ep):
    # remove blocked edges from graph G
    E = deepcopy(G)
    edge_rem = [e for e in E.edges() if np.random.random() < (1-Ep[e])**(E[e[0]][e[1]]['weight'])]
    E.remove_edges_from(edge_rem)

    # initialize CC
    CCs = dict() # each component is reflection of the number of a component to its members
    explored = dict(zip(E.nodes(), [False]*len(E)))
    c = 0
    # perform BFS to discover CC
    for node in E:
        if not explored[node]:
            c += 1
            explored[node] = True
            CCs[c] = [node]
            component = E[node].keys()
            for neighbor in component:
                if not explored[neighbor]:
                    explored[neighbor] = True
                    CCs[c].append(neighbor)
                    component.extend(E[neighbor].keys())
    return CCs

def newGreedyIC (G, k, Ep, R = 20):
    S = []
    for i in range(k):
        scores = {v: 0 for v in G}
        for j in range(R):
            CCs = findCCs(G, Ep)
            for CC in CCs:
                for v in S:
                    if v in CC:
                        break
                else: # in case CC doesn't have node from S
                    for u in CC:
                        scores[u] += float(len(CC))/R
        max_v, max_score = max(scores.items(), key = lambda dv: dv[1])
        S.append(max_v)
    return S