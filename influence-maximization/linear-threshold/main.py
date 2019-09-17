import networkx as nx
import click
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from linear_threshold import *
from greedy import generalGreedy
from generate_graph import generateGraph
from extract_filename import extract_dataset_name
from copy import deepcopy
from joblib import Parallel, delayed
from time import time

@click.command()
@click.argument('filename', type=click.Path(exists=True))

def main(filename):
    k = [5, 10, 15, 20, 25]
    influenced_users_list = []
    start = time()

    print("Generating Graph")
    G = Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(generateGraph)(filename)])
    print("Finished Generating Graph")
    
    print("Generating Weight")
    Ewu = Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(uniformWeights)(G[0])]) 
    # Ewr = Parallel(n_jobs=-1, verbose=5)([delayed(randomWeights)(G[0])])
    print("Finished Generating Weight")

    for index, _ in enumerate(k):
        print("Calculating the set of most influential Users k={}".format(k[index]))
        S = Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(generalGreedy)(G[0], Ewu[0], k=k[index], iterations=10)])
        print("Set of most influential Users {}".format(S[0][:]))
        print("Finished calculating the set of most influential Users k={}".format(k[index]))   

        print("Calculating influenced Users k={}".format(k[index]))
        influenced_users =  Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(avgLT)(G[0], S[0][:], Ewu[0], iterations=10)])
        influenced_users_list.append(influenced_users)
        print('Influened Users by S (Average) {:.3f} out of {} when S = {}'.format(influenced_users[0], len(G[0]), k[index]))
        print("Finished calculating influenced Users k={}".format(k[index]))

    print("It took {}".format(time()-start))

    plt.title("{} Graph Influence Maximization in Linear Threshold".format(extract_dataset_name(filename)))
    plt.xlabel("Set of most influential Users (S)")
    plt.ylabel("Influenced Users by S")
    plt.grid(True)
    plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True)) # x軸に小数点が表示されることを防ぐ
    plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True)) # y軸に小数点が表示されることを防ぐ 
    
    plt.xticks([i * 5 for i in range(0, 6)])
    if extract_dataset_name(filename) == "karate":
        plt.ylim([0, 40])
        plt.yticks([i * 5 for i in range(0, 9)])
    elif extract_dataset_name(filename) == "facebook":
        plt.ylim([0, 5000])
        plt.yticks([i * 1000 for i in range(0, 6)])
    elif extract_dataset_name(filename) == "twitter":
        plt.ylim([0, 90000])
        plt.yticks([i * 10000 for i in range(0, 10)])
    
    plt.plot(k, influenced_users_list)
    plt.savefig("result_linear_threshold_{}.png".format(extract_dataset_name(filename)))
    #plt.show()

if __name__ == "__main__":
    main() 
