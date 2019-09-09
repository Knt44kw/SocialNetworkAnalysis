from copy import deepcopy
import numpy as np

def runIC (G, S):
    ''' 
    Input: 
    G: 有向グラフ
    S: 最も影響力を与えた(最も多く 他のユーザーを活性化させた)ユーザーの集合  
    Output
    T: あるユーザーuによって活性化したユーザーの数
    '''
    np.random.seed(0)

    T = deepcopy(S) # copy already selected nodes
    p = dict() # probability that succeeds in activating

    # 各ユーザーが他のユーザーの活性化に成功する確率
    for u in G:
        p[u] = np.random.random()

    for u in T: # T may increase size during iterations
        for v in G[u]: # check whether new node v is influenced by chosen node u
             w = G[u][v]['weight']
             if v not in T and np.random.random() < 1 - (1-p[v])**w:
                 T.append(v)
    return T

def avgIC(G, S, iterations):
    avg = 0
    for i in range(iterations):
        avg += len(runIC(G,S))/iterations
    return avg