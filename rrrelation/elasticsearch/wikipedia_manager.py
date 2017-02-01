# coding=utf-8
"""
文書と文の各データベース用のマネージャー
"""

import math
from elasticsearch_manager import ElasticsearchManager


class ArticleManager(ElasticsearchManager):

    def __init__(self, host="localhost:9200"):
        ElasticsearchManager.__init__(self, host)
        self.index = "wikipedia-en-articles"
        self.doc_type = "wikipedia-en-articles-type"
        self.properties = {
            "title": {
                "type": "string",
                "store": "true",
                "index": "analyzed",
                "term_vector": "with_positions_offsets",
            },
            "text": {
                "type": "string",
                "store": "true",
                "index": "analyzed",
                "term_vector": "with_positions_offsets",
            },
        }

    def get_text_tfidf(self, doc_id):
        term_vectors = self.termvectors(doc_id)["text"]["terms"].items()
        sum_tf = float(sum([values["term_freq"] for term, values in term_vectors]))
        doc_count = float(self.doc_count())
        return {term: values["term_freq"] / sum_tf * math.log(doc_count / values["doc_freq"] + 1)
                for term, values in term_vectors}


class SentenceManager(ElasticsearchManager):
    """
    文単位でのデータベースマネージャー

    プロパティの説明

        * article_id : 所属する文書のID
        * order : 所属する文書内での文の連続番号
        * tokens : ステミング済のトークンの配列
        * entities : 文に含まれるエンティティの情報

    """

    def __init__(self, host="localhost:9200"):
        ElasticsearchManager.__init__(self, host)
        # article と index を同じにした場合のメリットとデメリットは要調査
        self.index = "knowledge-retrieval"
        self.doc_type = "sentences"
        self.properties = {
            "article_id": {
                "type": "integer",
                "store": "true",
            },
            "order": {
                "type": "integer",
                "store": "false",
            },
            "tokens": {
                "type": "nested",
                "properties": {
                    "token": {
                        "type": "string",
                        "store": "true",
                        "index": "analyzed",
                    },
                },
            },
            "entities": {
                "type": "nested",
                "properties": {
                    "token_index": {
                        "type": "integer",
                        "store": "false",
                    },
                    "token": {
                        "type": "string",
                        "store": "true",
                        "index": "not_analyzed",
                    },
                    "label": {
                        "type": "string",
                        "store": "true",
                        "index": "not_analyzed",
                    },
                },
            },
        }

    def get_by_article_id(self, article_id, **kwargs):
        body = {
            "query": {
                "match": {
                    "article_id": article_id
                }
            }
        }
        body.update(kwargs)
        return self.search(body)


    def find_sentences_by_entities(self, entities):
        """
        This needs Javascript language plugin.

            ```
            path/to/elasticsearch/bin/plugin install lang-javascript
            ```
        """

        should_tokens = [{"term": {"entities.token": entity}} for entity in entities]
        body = {
            "query": {
                "nested": {
                    "path": "entities",
                    "filter": {
                        "bool": {
                            "should": should_tokens
                        }
                    }
                }
            },
            "filter": {
                "script": {
                    "script": {
                        "lang": "javascript",
                        "inline": "_source.entities.length > 1"
                    }
                }
            }
        }
        return self.search(body)

    def get_sentences_having_more_than_two_entities(self, size=size):
        # TODO
        # elasticsearchのページネーション的なやつのイテレータを返したい
        body = {
            "size": size,
            "filter": {
                "script": {
                    "script": {
                        "lang": "javascript",
                        "inline": "_source.entities.length > 1"
                    }
                }
            }
        }
        return self.search(body)
