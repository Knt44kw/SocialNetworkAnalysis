from linear_threshold import avgLT

def generalGreedy(G, Ew, k, iterations) -> list:
    S = []
    for i in range(k):
        Inf = dict() # S(インフルエンサー)に含まれていないユーザーの集合 この中から，影響力が最大となるユーザーをインフルエンサーとしてSに追加
        for v in G:
            if v not in S:
                Inf[v] =  avgLT(G, S + [v], Ew, iterations=iterations)
        user, influence_value = max(Inf.items(),key=lambda influence_value: influence_value[1])
        S.append(user)
    return S