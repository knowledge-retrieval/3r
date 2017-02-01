#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests

import application

if __name__ == "__main__":
    # Check NER API Server
    ner_endpoint = os.getenv("NER_API_URL")

    headers = {"Content-type": "application/json"}
    res = requests.get(ner_endpoint + "/ner", headers=headers)

    if res.status_code != 200:
        raise Exception("Somthing wrong with %s" % ner_endpoint)

    res_json = res.json()

    status = res_json.get("status", None)

    if not status:
        raise Exception("Not satisfied NER API server")

    if status != "available":
        raise Exception("NER API Server is not available")

    print "NER API ENDPOINT : %s" % ner_endpoint

    # Check Elasticsearch
    es_endpoint = os.getenv("ELASTICSEARCH_URL")

    headers = {"Content-type": "application/json"}
    res = requests.get(es_endpoint, headers=headers)

    if res.status_code != 200:
        raise Exception("Somthing wrong with %s" % es_endpoint)

    es_version = res.json()["version"]["number"]

    print "Elasticsearch(%s) ENDPOINT : %s" % (es_version, es_endpoint)

    application.run()
