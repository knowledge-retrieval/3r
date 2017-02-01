# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
app = Flask(__name__)

setattr(app, "is_training", False)


@app.route("/")
def hello():
    return jsonify(is_training=app.is_training)


@app.route("/docs", methods=["POST"])
def docs():
    print request.json

    try:
        text = request.json["text"]
        print text

        # TODO
        # text をインできシング

        return jsonify(status="ok")
    except Exception as e:
        print e.message
        return jsonify(status="error", message=e.message)


@app.route("/start", methods=["POST"])
def start():
    print request.json

    try:
        max_iter = request.json.get("max_iter", 10)
        print max_iter

        app.is_training = True

        # TODO
        # BREADS で学習

        # app.is_training = False

        return jsonify(status="ok", message="Training begins")
    except Exception as e:
        print e.message
        return jsonify(status="error", message=e.message)


@app.route("/relations")
def relations():
    print request.args

    try:
        query = rrequest.args.get("query", None)
        if not query:
            raise Exception("parameters not includes query")

        # TODO
        # query から検索

        return jsonify(status="ok")
    except Exception as e:
        print e.message
        return jsonify(status="error", message=e.message)


def run():
    app.run()
