from copy import deepcopy
import numpy as np
import networkx as nx

def uniformWeights(G) -> dict:
    """
    ユーザー間の影響力を一様分布で設定する．
    各ユーザー間の影響力 = 各ユーザーの次数の逆数 とする．
    """
    Ew = dict()
    for u in G:
        in_edges = G.in_edges([u], data=True)
        dv = sum([edata['weight'] for v1, v2, edata in in_edges])
        for v1,v2,_ in in_edges:
            Ew[(v1,v2)] = 1/dv
    return Ew

def randomWeights(G) -> dict:
    """
    ユーザー間の影響力を[0,1]の一様乱数で設定
    """
    Ew = dict()
    for u in G:
        in_edges = G.in_edges([u], data=True)
        ew = [np.random.random() for e in in_edges] 
        total = 0 
        for num, (v1, v2, edata) in enumerate(in_edges):
            total += edata['weight']*ew[num]
        for num, (v1, v2, _) in enumerate(in_edges):
            Ew[(v1,v2)] = ew[num]/total
    return Ew

def runLT(G, S, Ew) -> list:
    '''
    Input: 
    G: 有向グラフ
    S: インフルエンサーとなるユーザーの初期集合
    Ew : ユーザー間の重み(ユーザー間の影響度)
    Output
    T: 最終的にインフルエンサーだと推定したユーザーの集合．つまり|T| = k
    '''
    T = deepcopy(S)

    # 各ユーザーの閾値を一様乱数で設定
    threshold = dict()  
    for u in G:
        threshold[u] = np.random.random()

    W = dict(zip(G.nodes(), [0]*len(G))) # 隣人となるユーザー間の重み(隣人の影響度)

    for u in T: 
        for v in G[u]: 
            if v not in T:
                W[v] += Ew[(u,v)]*G[u][v]['weight'] # 複数のユーザーがある同じユーザに対して影響を与えようとする状況を考慮
                if W[v] >= threshold[v]:
                    T.append(v)
    return T

def avgLT(G, S, Ew, iterations) -> float:
    avgSize = 0
    for i in range(iterations):
        T = runLT(G, S, Ew)
        avgSize = len(T)/iterations

    return avgSize