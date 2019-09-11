from linear_threshold import avgLT

def generalGreedy(G, Ew, k, iterations):
    S = []
    for i in range(k):
        Inf = dict() # influence for nodes not in S
        for v in G:
            if v not in S:
                Inf[v] = avgLT(G, S + [v], Ew, iterations=iterations)
        user, influence_value = max(Inf.items(),key=lambda influence_value: influence_value[1])
        S.append(user)
    return S