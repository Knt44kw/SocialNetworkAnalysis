from independent_cascade import avgIC
from greedy import generalGreedy
from degree_discount import degreeDiscount
from generate_graph import generateGraph
from extract_filename import extract_dataset_name
from tqdm import tqdm # 進捗バーの表示ができる
from joblib import Parallel, delayed
from collections import Counter
from time import time
import networkx as nx
import click
import numpy as np


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--influencer', '-k', type=int, default=10, help='Set Number of influencers')
@click.option('--iteration', '-i', type=int, default=10, help='Set Number of iterations')
# 自分の友人に影響を与えることに成功する確率pを全ユーザー共通にするかどうか(True: 共通にする．False:しない．デフォルトは共通)
@click.option('--probability_fixed', '-p', type=bool, default=True, help='Set whether influence probablity is fixed among all users') 


def main(filename, influencer, iteration, probability_fixed):
    each_influencer_list = np.array([]) 
    for i in tqdm(range(iteration)):
        print("Round {}".format(i+1)) # シミュレーション回数を表示
        start = time()
        G = Parallel(n_jobs=-1,backend="threading",verbose=0)([delayed(generateGraph)(filename)])
    
        print("Calculating the set of most influential Users k={}".format(influencer))
        S = Parallel(n_jobs=-1,backend="threading",verbose=0)([delayed(degreeDiscount)(G[0], k=influencer, probability_fixed=probability_fixed)])
        print("Set of most influential Users {} at round {}".format(S[0][:], i+1)) # それぞれのシミュレーション中のインフルエンサーを抽出
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
    
