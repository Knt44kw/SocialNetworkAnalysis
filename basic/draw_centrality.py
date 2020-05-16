import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def draw_centrality_headmap(G, pos, topology, centrality, centrality_name):
    nodes = nx.draw_networkx_nodes(G, pos, node_size=250,
                                  cmap=plt.cm.plasma,
                                  node_color=list(centrality.values()),
                                  nodelist=list(centrality.keys()))
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))
    edges = nx.draw_networkx_edges(G, pos)

    plt.title(topology + centrality_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()