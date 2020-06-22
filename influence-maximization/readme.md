# インフルエンサーを推定するスクリプト

## はじめに

`git clone https://github.com/Knt44kw/SocialNetworkAnalysis.git`

とターミナルに打つことで，このリポジトリ(フォルダのようなもの)を取り込む

* このコマンドがターミナル上で実行できるようにするためにはgithubに公開鍵を登録する必要がある そのやり方は
https://qiita.com/tnatsume00/items/e147662368d02e6416d2<br>
とかを参照
* gitの使い方:
https://qiita.com/nnahito/items/565f8755e70c51532459 <br>
とかを参照
* プログラムの変更した部分だけ，自分の環境に取り入れたいとき<br>
→　`git pull origin master`とターミナルに打つことで，取り込む

## ディレクトリについて
`linear-threshold`: 線形閾値モデルに関する処理をまとめたスクリプト<br>
`independent-cascade`:  独立カスケードモデルに関する処理をまとめたスクリプト
## 実行環境
anacondaが入っている python3.4以上ならば実行可能．
anacondaに含まれていないライブラリも使っている．

そのライブラリをインストールするために<br>
`pip install -r requirements.txt`<br>を実行する必要がある

## 実行方法と実行結果
### 実行方法
カレントディレクトリが influence-maximaizationの場合<br>

<b>線形閾値モデル</b>: 

`python ./linear-threshold/simplified_main.py ../dataset/{facebook_combined.txt}{twitter_combined.txt}{karate.edgelist} -k 10 -i 10`<br>

<b>独立カスケードモデル</b>: 

`python ./independent-cascade/simplified_main.py ../dataset/{facebook_combined.txt}{twitter_combined.txt}{karate.edgelist} -k 10 -i 10 -p False`

`{}`はこの文字列の中から好きなものをどれか一つ選ぶ

`-k`はインフルエンサーの数 自分で好きに決めていい<br> 
`-i`はシミュレーションの繰り返し回数 自分で好きに決めていい<br>

#### 独立カスケードモデルのみ

`-p`は 自分の友人に影響を与えることに成功する確率pを全ユーザー共通するかどうか(True: 共通にする．False:しない．デフォルトは固定)

独立カスケードモデルのほうが情報拡散のモデルとして，まとも．(一人が複数の人に一気に情報を伝えている様子を表現しているから)<br>
どっちの結果を信用したらいいか迷った場合は，独立カスケードモデル結果をもとに今後の分析を進めるといいと思う

### 実行結果の例
* -p Trueの場合(自分の友人に影響を与えることに成功する確率pが全ユーザー共通)
→ 全シミュレーション中，必ず同じ人が同じ回数だけインフルエンサーに選ばれる．(詳しくは実行結果を参照)

```
python independent-cascade/simplified_main.py -k 5 -i 10  ../dataset/karate.edgelist

Round 1
Calculating the set of most influential Users k=5
Set of most influential Users [34, 1, 33, 2, 3] at round 1
Finished calculating the set of most influential Users k=5

Round 2
Calculating the set of most influential Users k=5
Set of most influential Users [34, 1, 33, 2, 3] at round 2
Finished calculating the set of most influential Users k=5

(中略)

Round 9
Calculating the set of most influential Users k=5
Set of most influential Users [34, 1, 33, 2, 3] at round 9
Finished calculating the set of most influential Users k=5

Round 10
Calculating the set of most influential Users k=5
Set of most influential Users [34, 1, 33, 2, 3] at round 10
Finished calculating the set of most influential Users k=5

influencer 34.0 is selected 10 times
influencer 1.0 is selected 10 times
influencer 33.0 is selected 10 times
influencer 2.0 is selected 10 times
influencer 3.0 is selected 10 times

It took 0.0036416053771972656
```

* -p Falseの場合(自分の友人に影響を与えることに成功する確率pをユーザーごとに設定する)<br>
→ インフルエンサーと選ばれた回数がプログラムの実行のたびに毎回変化する．

```
python independent-cascade/simplified_main.py -k 5 -i 10 -p False ../dataset/karate.edgelist

Round 1
Calculating the set of most influential Users k=5
Set of most influential Users [34, 1, 33, 4, 26] at round 1
Finished calculating the set of most influential Users k=5

Round 2
Calculating the set of most influential Users k=5
Set of most influential Users [34, 1, 2, 26, 33] at round 2
Finished calculating the set of most influential Users k=5

(中略)

Round 9
Calculating the set of most influential Users k=5
Set of most influential Users [34, 1, 33, 26, 4] at round 9
Finished calculating the set of most influential Users k=5

Round 10
Calculating the set of most influential Users k=5
Set of most influential Users [34, 1, 33, 26, 17] at round 10
Finished calculating the set of most influential Users k=5

influencer 34.0 is selected 10 times
influencer 1.0 is selected 10 times
influencer 26.0 is selected 10 times
influencer 33.0 is selected 8 times
influencer 4.0 is selected 4 times

It took 0.0041658878326416016
```

## 補足
* linear-thereshod/simplified_main.pyを実行する際に生じるエラー

`/home/自分のユーザー名/anaconda3/lib/python3.7/site-packages/networkx/classes/reportviews.py`の
<br>
667行目と744行目の<br>
`for nbr, dd in nbrs.items())` 
を<br>
`for nbr, dd in list(nbrs.items()))`
に変更 
