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

## ティレクトリについて
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

`python ./linear-threshold/simplified_main.py ../dataset/{facebook_combined.txt}{twitter_combined.txt}{karate.edgelist} -k 10`<br>

<b>独立カスケードモデル</b>: 

`python ./independent-cascade/simplified_main.py ../dataset/{facebook_combined.txt}{twitter_combined.txt}{karate.edgelist} -k 10`

`{}`はこの文字列の中から好きなものをどれか一つ選ぶ

`-k`はインフルエンサーの数 自分で好きに決めていい 
### 実行結果の例

## 補足
* linear-thereshod/simplified_main.pyを実行する際に生じるエラー

`/home/自分のユーザー名/anaconda3/lib/python3.7/site-packages/networkx/classes/reportviews.py`の
<br>
667行目と744行目の<br>
`for nbr, dd in nbrs.items())` 
を<br>
`for nbr, dd in list(nbrs.items()))`
に変更 
