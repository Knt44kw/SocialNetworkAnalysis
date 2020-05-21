from priority_queue import PriorityQueue as PQ
from copy import deepcopy
import networkx as nx



def find_ldag(G, v, theta, Ew) -> nx.DiGraph:
    '''
    有向非巡回グラフとなるような部分グラフを作る
    INPUT:
        G -- networkの 有向グラフ
        v -- 有向グラフのノード 
        theta -- 閾値θ
        Ew -- グラフG内のエッジ間の重要度
    OUTPUT:
        D -- 有向グラフとなるような部分グラフ(network DiGraph)
    '''
    
    Inf = PQ()
    Inf.add_task(v, -1)
    x, priority = Inf.pop_item()
    M = -priority
    X = [x]

    D = nx.DiGraph()
    while M >= theta: # あるノードの影響度が閾値θを超えるまで繰り返す
        out_edges = G.out_edges([x], data=True) # 終点がノードxとなるエッジを求める[(hoge, x),(fuga, x), …()]のように求められる
        for (v1,v2,edata) in out_edges:
            if v2 in X:
                D.add_edge(v1, v2, weight=edata['weight']) # ノードxが有向非巡回グラフの中に含まれていないが，最も影響度が大きい場合は有向非巡回グラフに追加
        in_edges = G.in_edges([x]) # 始点がノードxとなるエッジを求める[(x, hoge), (x, fuga), …]のように求められる．
        for (u,_) in in_edges:
            if u not in X:
                try:
                    [pr, _, _] = Inf.entry_finder[u]
                except KeyError:
                    pr = 0
                # ノードu,v間に複数のエッジがあることを想定し，エッジの数×重み = Inf(u,v) = Σ w(u,x)* Inf(x,v)としている．
                Inf.add_task(u, pr - G[u][x]['weight']*Ew[(u,x)]*M) 
        try:
            x, priority = Inf.pop_item()
        except KeyError:
            return D
        M = -priority
        X.append(x) # ノードxを有向非巡回グラフのインフルエンサーとして追加

    return D

def tsort(Dc, u, reach):
    '''
     Topological sort of DAG D with vertex u first.
     Input:
     Dc -- directed acyclic graph (nx.DiGraph)
      u -- root node (int)
    reach -- direction of topological sort (considered either incoming or outgoing edges) (string)
    Output:
    L -- topological sort of nodes in Dc (list)
    '''
    assert (reach == "in" or reach == "out"), "reach argument can be either 'in' or 'out'."
    L = [u]
    if reach == "in":
        for node in L:
            in_nodes = list(map(lambda v1: v1, Dc.in_edges([node])))
            Dc.remove_edges_from(Dc.in_edges([node]))
            for v in in_nodes:
                if len(Dc.out_edges([v])) <= 1: # for self loops number of out_edges is 1, for other nodes is 0
                    L.append(v)
    elif reach == "out": # the same just for outgoing edges
        for node in L:
            out_nodes = list(map(lambda v2: v2, Dc.out_edges([node])))
            Dc.remove_edges_from(Dc.out_edges([node]))
            for v in out_nodes:
                if len(Dc.in_edges([v])) <= 1:
                    L.append(v)
    if len(Dc.edges()):
        raise ValueError("D has cycles. No topological order.")
    return L

def bfs_reach (D, u, reach):
    ''' 
    Breadth-First search of nodes in D starting from node u.
    Input:
    D -- directed acyclic graph (nx.DiGraph)
    u -- starting node (int)
    reach -- direction for which perform BFS
    Note:
        reach == "in" -- nodes that can reach u
        reach == "out" -- nodes that are reachable from u
    Output:
    Dc -- directed acyclic graph with edges in direction reach from u (nx.DiGraph)
    '''
    Dc = nx.DiGraph()
    if reach == "in":
        Dc.add_edges_from(D.in_edges([u], data=True))
        in_nodes = list(map(lambda v1: v1, D.in_edges([u])))
        for node in in_nodes:
            Dc.add_edges_from(D.in_edges([node], data=True))
            in_nodes.extend(filter(lambda v: v not in in_nodes, list(map(lambda v1: v1, D.in_edges([node])))))
    elif reach == "out": # the same just for outgoing edges
        Dc.add_edges_from(D.out_edges([u], data=True))
        out_nodes = list(map(lambda v2: v2, D.out_edges([u])))
        for node in out_nodes:
            Dc.add_edges_from(D.out_edges([node], data=True))
            out_nodes.extend(filter(lambda v: v not in out_nodes, list(map(lambda v2: v2, D.out_edges([node])))))
    return Dc

def computeAlpha(D, Ew, S, u, val=1):
    ''' 
    Computing linear coefficients alphas between activation probabilities.
    Input:
    D -- directed acyclic graph (nx.DiGraph)
    Ew -- influence weights of edges (eg. uniform, random) (dict)
    S -- set of activated nodes (list)
    u -- starting node (int)
    val -- initialization value for u (int)
    Output:
    A -- linear coefficients alphas for all nodes in D (dict)
    '''
    A = dict()
    for node in D:
        A[(u,node)] = 0
    A[(u,u)] = val

    Dc = bfs_reach(D, u, reach="in") # ノードu(インフルエンサー)とリンクを持つユーザーの集合を表すグラフDcを求める
    order = tsort(Dc, u, reach="in") # グラフDcに対してトポロジカルソート(一方向にして，グラフの内容は変わらないようにソート)を行う

    for node in order[1:]: # はじめのノードはα=1と設定しているから
        if node not in S + [u]: # 選ばれたノードがインフルエンサーではないとき
            out_edges = D.out_edges([node], data=True) # 該当ノードを終点とするエッジを求める
            for (v1,v2, edata) in out_edges:
                assert v1 == node, 'First node should be the same'
                # 該当ノードとエッジを持ち，グラフDc内にあるノードv2との重みを求める．
                # これをα_{v}(u) (ノードvがインフルエンサーuによって影響を受ける確率に対する係数)とする.
                if v2 in order: 
                    A[(u,node)] += edata['weight']*Ew[(node, v2)]*A[(u,v2)]
    return A

def computeActProb(D, Ew, S, u, val=1):
    ''' 
    Computing activation probabilities for nodes in D.
    Input:
    D -- directed acyclic graph (nx.DiGraph)
    Ew -- influence weights of edges (eg. uniform, random) (dict)
    S -- set of activated nodes (list)
    u -- starting node (int)
    val -- initialization value for u (int)
    Output:
    ap -- activation probabilities of nodes in D (dict)
    '''
    ap = dict()
    for node in D:
        ap[(u,node)] = 0
    ap[(u,u)] = val
    Dc = bfs_reach(D, u, "out")
    order = tsort(Dc, u, "out")
    for node in order:
        if node not in S + [u]:
            in_edges = D.in_edges([node], data=True)
            for (v1, v2, edata) in in_edges:
                assert v2 == node, 'Second node should be the same'
                if v1 in order:
                    ap[(u,node)] += ap[(u,v1)]*Ew[(v1, node)]*edata['weight']
    return ap

def LDAG_heuristic(G, Ew, k, theta):
    ''' 
    LDAG algorithm for seed selection.
    Input:
    G -- directed graph (nx.DiGraph)
    Ew -- inlfuence weights of edges (eg. uniform, random) (dict)
    k -- size of seed set (int)
    t -- parameter theta for finding LDAG (0 <= t <= 1; typical value: 1/320) (int)
    Output:
    S -- seed set (list)
    '''
    # define variables
    S = []
    IncInf = PQ()
    for node in G:
        IncInf.add_task(node, 0)
    # IncInf = dict(zip(G.nodes(), [0]*len(G))) # in case of usage dict instead of PQ
    LDAGs = dict()
    InfSet = dict()
    ap = dict()
    A = dict()

    for v in G:
        LDAGs[v] = find_ldag(G, v, theta, Ew) 
        # update influence set for each node in LDAGs[v] with its root
        for u in LDAGs[v]:
            InfSet.setdefault(u, []).append(v)
        alpha = computeAlpha(LDAGs[v], Ew, S, v)
        A.update(alpha) # add new linear coefficients to A
        # update incremental influence of all nodes in LDAGs[v] with alphas
        for u in LDAGs[v]:
            ap[(v, u)] = 0 # additionally set initial activation probability (line 7)
            priority, _, _ = IncInf.entry_finder[u] # find previous value of IncInf
            IncInf.add_task(u, priority - A[(v, u)]) # and add alpha
            # IncInf[u] += A[(v, u)] # in case of using dict instead of PQ

    for it in range(k):
        s, priority = IncInf.pop_item() # 活性化させたノード数の多かったインフルエンサーs(α_v(u)の総和が最も多くなるようなノードv)を求める
        for v in InfSet[s]: # インフルエンサーsによって活性化したノードv
            if v not in S: # ノードvがインフルエンサーの集合Sに存在しなければ
                # ノードvを前処理で求めたグラフの中に入れて，係数を更新
                D = LDAGs[v] 
                alpha_v_s = A[(v,s)]
                dA = computeAlpha(D, Ew, S, s, val=-alpha_v_s)
                for (s,u) in dA:
                    if u not in S + [s]: # don't update IncInf if it's already in S
                        A[(v,u)] += dA[(s,u)]
                        priority, _, _ = IncInf.entry_finder[u] # find previous value of incremental influence of u
                        IncInf.add_task(u, priority - dA[(s,u)]*(1 - ap[(v,u)])) # and update it accordingly
                # update ap_v_u for all u reachable from s in D 
                dap = computeActProb(D, Ew, S + [s], s, val=1-ap[(v,s)])
                for (s,u) in dap: # ノードのsがノードuに影響を及ぼす確率dapに対して
                    if u not in S + [s]: # ノードuがインフルエンサーでなければ
                        ap[(v,u)] += dap[(s,u)] 
                        priority, _, _ = IncInf.entry_finder[u] # find previous value of incremental influence of u
                        IncInf.add_task(u, priority + A[(v,u)]*dap[(s,u)]) # and update it accordingly
        S.append(s)
    return S