from copy import deepcopy
import numpy as np

def runIC (G, S) -> list:
    ''' 
    Input: 
    G: 有向グラフ
    S: 最も影響力を与えた(最も多く 他のユーザーを活性化させた)ユーザーの集合  
    Output
    T: インフルエンサーによって影響を受けたユーザー数
    '''

    T = deepcopy(S) 
    
    # 各ユーザーが他のユーザーの活性化に成功する確率 を一様乱数で決める
    p = dict()
    for u in G:
        p[u] = np.random.random()
    
    for u in T: 
        for v in G[u]: 
            w = G[u][v]['weight']
            if v not in T and np.random.random() < 1 - (1-p[u])**w: # 新たなユーザーvがインフルエンサーuによって影響を受ける(活性化する)か判断
                T.append(v)
    return T

def avgIC(G, S, iterations) -> float:
    avg = 0
    for i in range(iterations):
        avg += len(runIC(G,S))/iterations
    return avg