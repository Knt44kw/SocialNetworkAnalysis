import networkx as nx
import click
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from linear_threshold import *
from greedy import generalGreedy
from degree_discount import degreeDiscount
from ldag import *
from generate_graph import generateGraph
from extract_filename import extract_dataset_name
from joblib import Parallel, delayed
from time import time

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--influencer', '-k', type=int, default=10, help='Set Number of influencers')

def main(filename, influencer):
    influenced_users_list = []
    start = time()

    print("Generating Graph")
    G = Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(generateGraph)(filename)])
    print("Finished Generating Graph")

    print("Generating Weight")
    Ewu = Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(uniformWeights)(G[0])]) 
    print("Finished Generating Weight")
    
    print("Calculating the set of most influential Users k={}".format(influencer))
    S = Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(LDAG_heuristic)(G[0], Ewu[0], k=influencer, theta=1/320)])
    print("Set of most influential Users {}".format(S[0][:]))
    print("Finished calculating the set of most influential Users k={}".format(influencer))
    print("Calculating influenced Users k={}".format(influencer))
        
    if extract_dataset_name(filename) == "twitter":
        influenced_users =  Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(avgLT)(G[0], S[0][:], Ewu[0], iterations=10)])

    elif extract_dataset_name(filename) == "facebook":
        influenced_users =  Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(avgLT)(G[0], S[0][:], Ewu[0], iterations=50)])    

    elif extract_dataset_name(filename) == "karate":
        influenced_users =  Parallel(n_jobs=-1,backend="threading",verbose=10)([delayed(avgLT)(G[0], S[0][:], Ewu[0], iterations=50)]) 

    influenced_users_list.append(influenced_users)
    print('Influened Users by S (Average) {:.3f} out of {} when S = {}'.format(influenced_users[0], len(G[0]), influencer))
    print("Finished calculating influenced Users k={}".format(influencer))
        
    print("It took {}".format(time()-start))
    
if __name__ == '__main__':
    main()
