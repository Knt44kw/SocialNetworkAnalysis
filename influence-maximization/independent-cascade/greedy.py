from independent_cascade import avgIC

def generalGreedy(G, k=10, iterations=20) -> list:
    S = []
    for i in range(k):
        Inf = dict() # influence for nodes not in S
        for v in G:
            if v not in S:
                Inf[v] = avgIC(G, S + [v], iterations)
        user, influence_value = max(Inf.items(),key=lambda influence_value: influence_value[1])
        S.append(user)
    return S