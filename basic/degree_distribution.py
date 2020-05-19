from networkx.algorithms.community import LFR_benchmark_graph
import os
import networkx as nx
import click
import matplotlib.pyplot as plt

TOPOLOGY_LIST = ['scale_free', 'small_world', 'random_network', "lfr_benchmark", 'facebook', 'twitter', 'lesmis', 'karate']
IS_REAL_LIST = ["True", "False"]

@click.command()
@click.option('--user_num', '-n', type=int, default=100, help='Set Number of Agents')
@click.option("--topology", '-t', type=click.Choice(TOPOLOGY_LIST), help="Set network topology", default='scale_free')
@click.option('--isreal', '-r', type=click.Choice(IS_REAL_LIST), help="Set whether you use real-world network", default="False")


def main(user_num, topology, isreal):
    network_object = []

    if isreal == "True":
        if topology == "karate":
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            G = nx.read_edgelist("../dataset/karate.edgelist")
            network_object.append(G)

        elif topology == "lesmis":
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            G = nx.readwrite.gml.read_gml("../dataset/lesmis.gml")
            network_object.append(G)
        
        elif topology == "facebook":
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            G = nx.read_edgelist("../dataset/facebook_combined.txt", nodetype=int)
            network_object.append(G) 
        
        elif topology == "twitter":
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            G = nx.read_edgelist("../dataset/facebook_combined.txt", nodetype=int) 
            network_object.append(G)
        else:
            raise NameError("{} cannot be used because specified topology is artificial network".format(topology))

    elif isreal == "False":
        if topology == "scale_free":
            G = nx.barabasi_albert_graph(n=user_num, m=12, seed=0)
            network_object.append(G)

        elif topology == "small_world":
            G = nx.newman_watts_strogatz_graph(n=user_num, k=12, p=0.20, seed=0)
            network_object.append(G)

        elif topology == "random_network":
            G = nx.fast_gnp_random_graph(n=user_num, p=0.20, seed=0)
            network_object.append(G)

        elif topology == "lfr_benchmark":
            G = LFR_benchmark_graph(n=user_num, tau1=3, tau2=1.5, mu=0.1, average_degree=12, min_community=20, seed=0)
            network_object.append(G)
        else:
            raise NameError("{} cannot be used because specified topology is real-world network".format(topology)) 
    
    print("{} infomation {}".format(topology, nx.info(network_object[0])))
    print("shortest path length {}".format(nx.average_shortest_path_length(network_object[0])))
    print("clustering coefficient {}".format(nx.average_clustering(network_object[0])))

    plt.subplot(211)
    plt.title("{} degree distribution".format(topology))
    plt.xlabel("degree")
    plt.ylabel("the number of nodes ")
    plt.plot(nx.degree_histogram(network_object[0]))
    if topology == "scale_free":
        plt.subplot(212)
        plt.xscale("log")
        plt.yscale("log")
        plt.grid("both")
        plt.xlabel("log-scale degree")
        plt.ylabel("log-scale the number of nodes ")
        plt.plot(nx.degree_histogram(network_object[0]))
    plt.show()

if __name__ == "__main__":
    main()