from priority_queue import PriorityQueue as PQ 
import numpy as np

def degreeDiscount(G, k, probability_fixed=True):
    """
    Input: 
    G: 無向 or 有向グラフ
    k: 求めたいインフルエンサーの数
    probability_fixed: 自分の友人に影響を与えることに成功する確率pを全ユーザーに一緒の値にするかどうか(True: 固定する．False:固定しない)
    
    Output
    S: インフルエンサーの集合 |S| = k
    """
    S = []
    dd = PQ() # degree discount
    t = dict() # number of adjacent vertices that are in S
    d = dict() # degree of each vertex
    
    # initialize degree discount
    for u in G.nodes():
        d[u] = sum([G[u][v]['weight'] for v in G[u]]) # each edge adds degree 1
        dd.add_task(u, -d[u]) # add degree of each node
        t[u] = 0
    
    if probability_fixed:
        p = 0.01
        # add vertices to S greedily
        for i in range(k):
            u, priority = dd.pop_item() # extract node with maximal degree discount
            S.append(u)
            for v in G[u]:
                if v not in S:
                    t[v] += G[u][v]['weight'] # increase number of selected neighbors
                    priority = d[v] - 2*t[v] - (d[v] - t[v])*t[v]*p # discount of degree
                    dd.add_task(v, -priority)
        return S
    
    else:
        p = dict() # propagation probability in each user
        for u in G:
            p[u] = np.random.uniform()

        # add vertices to S greedily
        for i in range(k):
            u, priority = dd.pop_item() # extract node with maximal degree discount
            S.append(u)
            for v in G[u]:
                if v not in S:
                    t[v] += G[u][v]['weight'] # increase number of selected neighbors
                    priority = d[v] - 2*t[v] - (d[v] - t[v])*t[v]*p[v]  # discount of degree
                    dd.add_task(v, -priority)
        return S