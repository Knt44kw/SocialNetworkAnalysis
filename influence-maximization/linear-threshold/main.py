import networkx as nx
import click
from linear_threshold import *
from greedy import generalGreedy
from generate_graph import generateGraph
from copy import deepcopy
from joblib import Parallel, delayed

@click.command()
@click.argument('filename', type=click.Path(exists=True))

def main(filename):
    G = Parallel(n_jobs=-1, verbose=5)([delayed(generateGraph)(filename)])
    Ewu = Parallel(n_jobs=-1, verbose=5)([delayed(uniformWeights)(G[0])]) 
    # Ewr = Parallel(n_jobs=-1, verbose=5)([delayed(randomWeights)(G[0])])

    S = Parallel(n_jobs=-1, verbose=5)([delayed(generalGreedy)(G[0], Ewu[0], k=10, iterations=20)]) 
    print("Set of most influential Users {}".format(S[0][:]))

    influenced_users =  Parallel(n_jobs=-1, verbose=5)([delayed(avgLT)(G[0], S[0][:], Ewu[0], iterations=200)]) 
    print('Activated Users by S (Average) {:.3f} out of {}'.format(influenced_users[0], len(G[0])))

if __name__ == "__main__":
    main()
   