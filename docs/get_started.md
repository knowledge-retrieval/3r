<link href="https://cdn.rawgit.com/knsv/mermaid/7.0.0/dist/mermaid.css" rel="stylesheet" type="text/css">
<script src="https://cdn.rawgit.com/knsv/mermaid/7.0.0/dist/mermaid.min.js"></script>
<script>
  console.log("initialize mermaid");
  mermaid.initialize({startOnLoad:true});
</script>

## はじめに

本システム (`relretrieval`) と必要となる関連システム (`Elasticsearch`、`NER API Server`) 、及びそれらを利用する``アプリケーション``の関係を示します。

<center>
<div class="mermaid">
graph TD
    subgraph ""
        app[fa:fa-user アプリケーション]
    end
    app -.-> 3r
    subgraph 本システム及び関連システム
        3r[relretrieval]
        es[fa:fa-database Elasticsearch]
        ner[fa:fa-scissors NER API Server]
        3r -.-> es
        3r -.-> ner
    end
</div>
</center>


図に示すように本システムは、バックエンドで固有表現抽出 (NER) をするためのサーバーと、データベースとしてElasticsearchを使用します。

## ダウンロードとセットアップ

### Elasticsearch

データベースとして[Elasticsearch](https://www.elastic.co/products/elasticsearch)を利用します。
すでに起動している場合は必要ありませんが、以下のインデックス名及びプラグインを使用します。

* インデックス : `relretrieval`
* プラグイン : `lang-javascript`

#### インストール例

```
$ mkdir ./data
$ wget -P ./data/ https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/2.3.4/elasticsearch-2.3.4.zip
$ unzip -d ./data/ ./data/elasticsearch-2.3.4.zip
$ echo "script.inline: true" >> ./data/elasticsearch-2.3.4/config/elasticsearch.yml
$ echo "script.indexed: true" >> ./data/elasticsearch-2.3.4/config/elasticsearch.yml
$ ./data/elasticsearch-2.3.4/bin/plugin install lang-javascript
$ ./data/elasticsearch-2.3.4/bin/elasticsearch
...
```

### NER API Server

本システムでは固有表現を外部のAPIを用いて抽出を行うことで、固有表現抽出 (NER) に用いるツールの変更を容易にしています。
固有表現抽出用のAPIが満たすべき仕様については[こちら](api/ner_api.md)。

#### インストール例

上記のAPI仕様を満たす固有表現抽出サーバー (`Play NER Server`) を本システムとは別に提供しています。
`Play NER Server` の使用には [`activator`](https://www.lightbend.com/activator/download) のインストールが必要です。

##### ソースコードのダウンロード

```
$ git clone https://github.com/sosuke-k/ner-play-server
```


##### CRF モデルのダウンロード

```
$ cd ner-play-server
$ wget -P ./data/ http://nlp.stanford.edu/software/stanford-ner-2015-12-09.zip
$ unzip -d ./data/ ./data/stanford-ner-2015-12-09.zip
$ cp -r ./data/stanford-ner-2015-12-09/classifiers/ ./apps/play/public/classifiers/
```

##### Play NER Server の起動

最初はCRFモデルの読み込みに少し時間がかかります。

```
$ cd apps/play
$ ./bin/activator run
...
--- (Running the application, auto-reloading is enabled) ---

[info] p.c.s.NettyServer - Listening for HTTP on /0:0:0:0:0:0:0:0:9000

(Server started, use Ctrl+D to stop and go back to the console...)
```


### relretrieval

#### 環境変数の追加

* `ELASTICSEARCH_URL` : Elasticsearch のエンドポイント
* `NER_API_URL` : 固有表現抽出サーバーのエンドポイント


環境変数の設定例：

```
export ELASTICSEARCH_URL "http://localhost:9200"
export NER_API_URL "http://localhost:9000"
```

#### インストール

```
pip install relretrieval
```

#### インデックスの初期化

```
$ python -m relretrieval --init True
Elasticsearch(2.3.4) ENDPOINT : http://localhost:9200
Initializing ...
done
```

#### 起動

```
$ python -m relretrieval
Elasticsearch(2.3.4) ENDPOINT : http://localhost:9200
NER API ENDPOINT : http://localhost:9000
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
...
```

### 簡単な使い方

#### 文を保存

`article_id=1` で `I live in Japan.` を保存する例です。

```
$ curl --header "Content-type: application/json" --request POST --data '{"article_id": 1, "text":"I live in Japan."}' http://localhost:5000/docs -s | jq
{
  "status": "ok"
}
```
