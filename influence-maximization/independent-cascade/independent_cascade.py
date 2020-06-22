from copy import deepcopy
import numpy as np

def runIC (G, S, probability_fixed=True) -> list:
    ''' 
    Input: 
    G: 無向 or 有向グラフ
    S: 最も影響を与えた(最も多く 他のユーザーを活性化させた)ユーザーの集合  
    probability_fixed: 自分の友人に影響を与えることに成功する確率pを全ユーザーに共通にするかどうか(True:共通にする.False:しない)
    
    Output
    T: インフルエンサーによって影響を受けたユーザー数
    '''

    T = deepcopy(S) 
    
    # 各ユーザーが他のユーザーの活性化に成功する確率 を一様乱数で決める
    if probability_fixed:
        p = 0.01
        for u in T: 
            for v in G[u]: 
                w = G[u][v]['weight']
                if v not in T and np.random.random() < 1 - (1-p)**w: # 新たなユーザーvがインフルエンサーuによって影響を受けるか判断
                    T.append(v)  
    else:
        p = dict()
        for u in G:
            p[u] = np.random.uniform(0, 1) # ユーザーごとに自分の友人に影響を与えることに成功する確率pを一様乱数で設定
        
        for u in T: 
            for v in G[u]: 
                w = G[u][v]['weight']
                if v not in T and np.random.random() < 1 - (1-p[u])**w: # 新たなユーザーvがインフルエンサーuによって影響を受けるか判断
                    T.append(v)
    return T

def avgIC(G, S, iterations) -> float:
    avg = 0
    for i in range(iterations):
        avg += len(runIC(G,S))/iterations
    return avg