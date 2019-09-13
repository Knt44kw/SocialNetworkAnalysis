import networkx as nx
from independent_cascade import avgIC
from greedy import generalGreedy
from joblib import Parallel, delayed

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
    S = Parallel(n_jobs=-1, verbose=5)([delayed(generalGreedy)(G, k=10, iterations=1)]) 
    print("Set of most influential Users {}".format(S[0][:]))

    # calculate average activated set size
    influenced_users =  Parallel(n_jobs=-1, verbose=5)([delayed(avgIC)(G, S[0][:], iterations=1)]) 
    print('Activated Users by S (Average) {:.3f} out of {}'.format(influenced_users[0], len(G)))
    
if __name__ == '__main__':
    main()
    
