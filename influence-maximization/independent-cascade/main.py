import networkx as nx
import numpy as np
from independent_cascade import avgIC
from greedy import generalGreedy

def main():
    # read in graph
    G = nx.Graph()
    with open("./dataset/facebook_combined.txt") as f:
        n, m = f.readline().split()
        for line in f:
            u, v = map(int, line.split())
            try:
                G[u][v]['weight'] += 1
            except:
                G.add_edge(u,v, weight=1)

    # calculate the set of most influential users
    S = generalGreedy(G, k=10)
    print("Set of most influential Users {}".format(S))
  
    # calculate average activated set size
    print('Activated Users by S (Average) {} out of {}'.format(avgIC(G, S, iterations=200), len(G)))
    
if __name__ == '__main__':
    main()
    