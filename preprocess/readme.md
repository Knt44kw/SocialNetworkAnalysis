## 実データからソーシャルグラフを生成
1. あるtwitterユーザーのフォロワーの情報をMongoDBというデータベースに格納．
2. そのデータベース内で相互フォローしているユーザーを見つける.
3. 相互フォローしているユーザー間のソーシャルグラフを作り，そのつながりをテキストファイルで出力し，可視化

という処理を行うプログラムをまとめたディレクトリ

## MongoDBに必要なライブラリのインストール方法やその使い方について
### ライブラリ:  
  pythonで使えるようにするためにはpymongoというライブラリが必要 `pip install pymongo`でインストールできる

### MongoDBのインストール方法と使い方
* windows:
https://qiita.com/Syoitu/items/db192385a4b2e4884ed5
* linux: 
https://qiita.com/FukuharaYohei/items/d109f5c3f5dce0d972e4

## プログラムの内容と実行方法
### プログラムの内容
 * `get_follower_info.py`: 自分で指定したユーザーのフォロワーの情報を取得
 
 * `create_socialgraph.py`: 
    `get_follower_info.py`で取得したフォロワーのうち，相互フォローとなっているユーザーを見つけ，そのユーザーのソーシャルグラフを可視化し，その関係性をテキストファイルで出力
 
 * `config.py`: Twitter APIの APIキーの設定を記述
 
 * `mongo_dao.py`: pythonでMongoDBを使えるようにあれこれ設定してあるプログラム．これはいじらない．
### プログラムの実行方法
 1. `config.py`に自分のTwitter APIキーを書く
 2. `python get_follower_info.py`で`get_follower_info.py`を実行
 3. `python create_socialgraph.py`で`create_socialgraph.py`を実行
 
## 実行結果
* mutual_follow.png: 
相互フォローとなっているユーザーのソーシャルグラフを可視化したもの

* test.edgelist: 
相互フォローとなっているユーザーの関係性を出力したテキストファイル

## 参考にした(ほぼパクった)元サイト
https://qiita.com/bc_yuuuuuki/items/964efd17dae53d855c8b
