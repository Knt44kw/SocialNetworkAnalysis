from linear_threshold import *
from greedy import generalGreedy
from degree_discount import degreeDiscount
from ldag import *
from generate_graph import generateGraph
from extract_filename import extract_dataset_name
from joblib import Parallel, delayed
from tqdm import tqdm # 進捗バーの表示ができる
from collections import Counter
from time import time
import networkx as nx
import numpy as np
import click

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--influencer', '-k', type=int, default=10, help='Set Number of influencers')
@click.option('--iteration', '-i', type=int, default=10, help='Set Number of iterations')

def main(filename, influencer, iteration):
    each_influencer_list = np.array([]) 
    for i in tqdm(range(iteration)):
        print("Round {}".format(i+1)) # シミュレーション回数を表示
        start = time()
        G = Parallel(n_jobs=-1,backend="threading",verbose=0)([delayed(generateGraph)(filename)])
        Ewu = Parallel(n_jobs=-1,backend="threading",verbose=0)([delayed(uniformWeights)(G[0])]) 
     
        print("Calculating the set of most influential Users k={}".format(influencer))
        S = Parallel(n_jobs=-1,backend="threading",verbose=0)([delayed(LDAG_heuristic)(G[0], Ewu[0], k=influencer, theta=1/320)])
        print("Set of most influential Users {} at round {}".format(S[0][:], i)) # それぞれのシミュレーション中のインフルエンサーを抽出
        print("Finished calculating the set of most influential Users k={}\n".format(influencer))
        
        each_influencer_list = np.append(each_influencer_list, S[0][:])
        
    # 全シミュレーションの中で，インフルエンサーに選ばれたユーザーの数を数える
    influencer_counter = Counter(each_influencer_list)
    # ユーザーがインフルエンサーに選ばれた回数を(ユーザーid, 選ばれた回数)の形式で表示
    # print(influencer_counter)
    # インフルエンサーに選ばれた回数が多い順にk人のユーザーを選ぶ
    influencer_name, selected = zip(*influencer_counter.most_common(influencer))

    for name, count in zip(list(influencer_name),list(selected)):
        print("influencer {} is selected {} times".format(name, count))

    print("\nIt took {}".format(time()-start))

    
if __name__ == '__main__':
    main()
