import networkx as nx
import click
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from independent_cascade import avgIC
from greedy import generalGreedy
from generate_graph import generateGraph
from extract_filename import extract_dataset_name
from joblib import Parallel, delayed

@click.command()
@click.argument('filename', type=click.Path(exists=True))

def main(filename):
    k = [5, 10, 15, 20, 25]
    influenced_users_list = []

    G = Parallel(n_jobs=-1, verbose=5)([delayed(generateGraph)(filename)])
    
    for index, _ in enumerate(k):
        S = Parallel(n_jobs=-1, verbose=5)([delayed(generalGreedy)(G[0], k=k[index], iterations=10)]) 
        print("Set of most influential Users {}".format(S[0][:]))
    
        influenced_users =  Parallel(n_jobs=-1, verbose=5)([delayed(avgIC)(G[0], S[0][:], iterations=10)]) 
        influenced_users_list.append(influenced_users)
        print('Influened Users by S (Average) {:.3f} out of {} when S = {}'.format(influenced_users[0], len(G[0]), k[index]))
        
    plt.title("Result of influence maximization in {} Graph".format(extract_dataset_name(filename)))
    plt.xlabel("Set of most influential Users (S)")
    plt.ylabel("Influenced Users by S")
    plt.grid(True)
    plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    plt.gca().get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))
   
    if extract_dataset_name(filename) == "karate":
        plt.ylim([0, 40])
    elif extract_dataset_name(filename) == "facebook":
        plt.ylim([0, 5000])
    elif extract_dataset_name(filename) == "twitter":
        plt.ylim([0, 90000])
    
    plt.plot(k, influenced_users_list)
    plt.show()
    
if __name__ == '__main__':
    main()
    
