from networkx.algorithms.community import LFR_benchmark_graph
from draw_centrality import draw_centrality_headmap
import os
import networkx as nx
import click

TOPOLOGY_LIST = ['scale_free', 'small_world', 'random_network', "lfr_benchmark", 'facebook', 'twitter', 'lesmis', 'karate']
CENTRALITY_LIST = ['DC', "CC", 'BC', 'EC', "KATZ", "PR"]
IS_REAL_LIST = ["True", "False"]

@click.command()
@click.option('--user_num', '-n', type=int, default=100, help='Set Number of Agents')
@click.option("--topology", '-t', type=click.Choice(TOPOLOGY_LIST), help="Set network topology", default='scale_free')
@click.option('--centrality', '-c', type=click.Choice(CENTRALITY_LIST), help="Set centrality algorithm", default="DC")
@click.option('--isreal', '-r', type=click.Choice(IS_REAL_LIST), help="Set whether you use real-world network", default="False")


def main(user_num, topology, centrality, isreal):
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
            G = nx.barabasi_albert_graph(n=user_num, m=40, seed=0)
            network_object.append(G)

        elif topology == "small_world":
            G = nx.newman_watts_strogatz_graph(n=user_num, k=40, p=0.20, seed=0)
            network_object.append(G)

        elif topology == "random_network":
            G = nx.fast_gnp_random_graph(n=user_num, p=0.20, seed=0)
            network_object.append(G)

        elif topology == "lfr_benchmark":
            G = LFR_benchmark_graph(n=user_num, tau1=3, tau2=1.5, mu=0.1, average_degree=40, min_community=50, seed=0)
            network_object.append(G)
        else:
            raise NameError("{} cannot be used because specified topology is real-world network".format(topology)) 

    pos = nx.spring_layout(network_object[0])
    if centrality == "DC":
        draw_centrality_headmap(G=network_object[0], pos=pos, topology=topology, centrality=nx.degree_centrality(network_object[0]), centrality_name=centrality)
    elif centrality == "CC":
        draw_centrality_headmap(G=network_object[0], pos=pos, topology=topology, centrality=nx.closeness_centrality(network_object[0]), centrality_name=centrality)
    elif centrality == "BC":
        draw_centrality_headmap(G=network_object[0], pos=pos, topology=topology, centrality=nx.betweenness_centrality(network_object[0]), centrality_name=centrality)
    elif centrality == "EC":
        draw_centrality_headmap(G=network_object[0], pos=pos, topology=topology, centrality=nx.eigenvector_centrality(network_object[0]), centrality_name=centrality)
    elif centrality == "KATZ":
        draw_centrality_headmap(G=network_object[0], pos=pos, topology=topology, centrality=nx.katz_centrality(network_object[0]), centrality_name=centrality)
    elif centrality == "PR":
        draw_centrality_headmap(G=network_object[0], pos=pos, topology=topology, centrality=nx.pagerank(network_object[0]), centrality_name=centrality)


if __name__ == "__main__":
    main()