## NER API について

使用可能な NER API Server のAPI仕様を示します。

```
swagger: "2.0"
basePath: /
produces:
  - application/json
paths:
  /ner:
    get:
      summary: NER Server Status
      description: The NER get endpoint returns information about the NER server status.
      responses:
        200:
          description: An array of products
          schema:
            type: object
            properties:
              status:
                type: string
                description: 'available' or 'unavailable'.
              current:
                type: string
                description: other information.
              message:
                type: string
                description: other messages.
    post:
      summary: NER tokens
      description: The NER post endpoint returns tokens and named entities.
      parameters:
        - name: text
          in: query
          description: text including sentences to do NER.
          required: true
          type: string
      responses:
        200:
          description: An array of products
          schema:
            type: object
            properties:
              tokens:
                type: array
                items:
                  type: object
                    properties:
                      text:
                        type: string
                        description: one tokenized token.
                      label:
                        type: string
                        description: label specifying named entity
```

具体的には次のようなレスポンスを返すものです。

```
$ curl localhost:9000/ner  -s | jq
{
  "status": "available",
  "current": "english.all.3class.distsim.crf.ser.gz",
  "message": "you can use these classifiers: english.all.3class.distsim.crf.ser.gz, english.conll.4class.distsim.crf.ser.gz, english.muc.7class.distsim.crf.ser.gz"
}
$ curl --header "Content-type: application/json" --request POST --data '{"text":"I live in Japan."}' http://localhost:9000/ner -s | jq
{
  "tokens": [
    {
      "text": "I",
      "label": "O"
    },
    {
      "text": "live",
      "label": "O"
    },
    {
      "text": "in",
      "label": "O"
    },
    {
      "text": "Japan",
      "label": "LOCATION"
    },
    {
      "text": ".",
      "label": "O"
    }
  ]
}
```
